# Density tiers by vanilla strategic region, with state overrides.
# Target px per province: tier 1 55, tier 2 110, tier 3 165, tier 4 unchanged (all times a scale).
from pd_common import *
BASE = {1: 55.0, 2: 110.0, 3: 165.0, 4: None}
REGION = dict(
    region_central_europe=2, region_western_europe=2, region_eastern_europe=2, region_balkans=2, region_near_east=2,
    region_indochina=2, region_greater_persia=2, region_north_india=2, region_south_china=2, region_north_china=2,
    region_southern_europe=3, region_atlantic_coast=3, region_south_india=3, region_indonesia=3, region_east_africa=3,
    region_southern_africa=3, region_central_america=3, region_gran_colombia=3, region_andes=3, region_west_africa=3,
    region_equatorial_africa=3, region_nile_basin=3, region_russia=3, region_northern_europe=3, region_la_plata=3,
    region_brazil=3, region_north_africa=3, region_northeast_asia=3,
    region_siberia=4, region_canada=4, region_pacific_coast=4, region_oceania=4, region_central_asia=4, region_arabia=4,
    region_himalayas=4, region_great_plains=4)
STATE = {}


def _put(t, names):
    for n in names.split():
        STATE["STATE_" + n] = t


_put(1, "PALESTINE LEBANON SINAI LOWER_EGYPT KASHMIR PUNJAB HILL_PUNJAB BRANDENBURG CYPRUS FORMOSA KHUZESTAN BASRA")
_put(2, "PYONGYANG SARIWON SEOUL YANGHO BUSAN SHENGJING SOUTHERN_MANCHURIA WESTERN_CUBA CENTRAL_CUBA EASTERN_CUBA "
        "NICARAGUA SAN_SALVADOR ERITREA SOMALILAND AMHARA OROMIA GONDER "
        "NORTH_ANGOLA SOUTH_ANGOLA EAST_ANGOLA KATANGA BAS_CONGO MIDDLE_EGYPT UPPER_EGYPT ALGIERS ORAN CONSTANTINE TUNISIA "
        "MOSCOW INGRIA SMOLENSK PSKOV NORTH_CAUCASUS DAGESTAN KUBAN ROSTOV UUSIMAA WEST_KARELIA")
_put(3, "GANSU NINGXIA HOKKAIDO NORTHERN_MANCHURIA OUTER_MANCHURIA FERGANA UZBEKIA TAJIKISTAN CALIFORNIA WASHINGTON OREGON "
        "VICTORIA NEW_SOUTH_WALES NORTH_ISLAND SOUTH_ISLAND TASMANIA YEMEN OMAN ABU_DHABI TEXAS LOUISIANA")
_put(4, "ALXA ULIASTAI URGA HINGGAN AMUR KAMCHATKA OKHOTSK SAKHALIN NENETSIA VOLOGDA ARKHANGELSK GREENLAND ICELAND NORRLAND "
        "NORTHERN_NORWAY KOLA OULU EAST_KARELIA AMAZONAS PARA MATO_GROSSO GOIAS PATAGONIA RIO_NEGRO ARAUCANIA EAST_SAHARA SAHARA "
        "LIBYAN_DESERT WEST_SAHARA LIBYA DONGOLA DARFUR EGYPTIAN_DESERT INNER_MAURITANIA MAURITANIA TIMBUKTU NIGER CHAD BOTSWANA "
        "HEREROLAND NAMAQUALAND GUAVIARE BALUCHISTAN SISTAN")


def province_tiers(S):
    sr = {}
    for f in sorted(glob.glob(VAN + "/common/strategic_regions/*.txt")):
        t = nocomment(read(f))
        for m in re.finditer(r"^(region_[a-z0-9_]+)\s*=\s*\{(.*?)^\}", t, flags=re.M | re.S):
            sm = re.search(r"states\s*=\s*\{([^}]*)\}", m.group(2))
            for s in re.findall(r"STATE_[A-Z0-9_]+", sm.group(1) if sm else ""):
                sr[s] = m.group(1)
    missing = [s for s in STATE if s not in S]
    assert not missing, missing
    out = {}
    unknown = set()
    for s, v in S.items():
        if v["sea"]:
            continue
        r = sr.get(s)
        if s not in STATE and r not in REGION:
            unknown.add((s, r))
        t = STATE.get(s, REGION.get(r, 4))
        for p in v["provinces"]:
            out[p] = t
    if unknown:
        print("states without a tier (left unchanged):", sorted(unknown))
    return out


def scale_for_cap(tier_of, area, splittable, total_now, cap):
    """Smallest scale (densest map) whose predicted total stays at or under cap."""
    def total(scale):
        n = total_now
        for p in splittable:
            b = BASE[tier_of.get(p, 4)]
            if b:
                n += max(1, int(area[p] / (b * scale) + 0.5)) - 1
        return n
    lo, hi = 0.2, 3.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if total(mid) > cap:
            lo = mid
        else:
            hi = mid
    return hi, total(hi)
