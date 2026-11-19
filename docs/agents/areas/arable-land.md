# Arable land

State-region `arable_land` (map_data/state_regions) follows real cropland, not vanilla's 1836 values.

- **Source:** World Bank / FAO cropland per country = arable land (AG.LND.ARBL.HA) + permanent crops (AG.LND.CROP.ZS x land area), 1961 or the earliest year. Ex-USSR republics (1992 data) are scaled to the 1950 USSR sown area (146.3M ha), with Kazakhstan before the Virgin Lands (10M ha). Taiwan 0.87M ha (1961). Sudan 9M ha (1961, without the south). Data: `tools/arable/cropland.json`.
- **Scale:** 80 arable units per million hectares, the same everywhere (world total about 100k units, vanilla 61k).
- **Within a country:** the country total is split half by vanilla's relative weights and half by the 1946 rural workforce (subsistence workers plus jobless, from a 1946.11 observer save), as a stand-in for sub-national cropland data.
- **Floors:** a region never gets less than its 1946 commercial farm and plantation levels plus room for its rural workforce (+10%). 80 regions are floored, mostly Japan, Korea, Borneo, Puerto Rico and the Caribbean; together they add under 1% to the total.
- **Rice paddies** hold 62,500 peasants per level (other subsistence farms 25,000), and the same output per peasant: wet-rice farming used far more labour per hectare, which is how monsoon Asia fits on its real land without changing its food output. Baden, Wallonia, Guangdong and Gabon are raised by hand so their split states hold their 1946 farms.
- Per-region mapping to modern countries and the final values: `tools/arable/regions.json`. `tools/arable/alloc_reference.py` is the script that produced them (reads saves from Forge paths).
