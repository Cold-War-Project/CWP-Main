# Explainer – Public Services Funding, Coverage and Outcomes

Companion to `CWP Economy Rework Proposal.md`, section 6. Applies to Healthcare, Education and Public Security (and optional Housing). All numbers are illustrative.

## 1. The moving parts

| Part | Role |
|---|---|
| **Law** | Sets the *kind* of system (Universal, Mixed, Private…), which modifiers it gives, and the allowed funding range |
| **Funding PM** on the state's Urban Center (0–200%) | Sets how much the *government* buys in that state: 0.25 × step units per urban center level |
| **Providers** (Hospitals, Schools, Police Stations) | Make the good and sell it on the national market |
| **Pops** (mid/high SoL) | Buy some of the good privately |
| **Monthly script** | Measures coverage, works out how much of the funded effect is actually delivered, and applies the modifiers |

## 2. Why the script is needed

Production method modifiers in Vic3 apply in full whether or not the building gets its inputs. If the outcomes sat on the funding PMs, a state at 200% funding would get the full mortality bonus with no hospitals at all. Instead the funding PMs only create **demand**, and the script applies the **outcomes**, scaled by what was actually supplied.

## 3. The monthly calculation

For each state and each service:

```
Fn  = min(1, sell orders / buy orders)                national fulfilment
Fl  = min(1, state production / state consumption)    local fulfilment
C   = 0.5 × Fn + 0.5 × Fl                             coverage
E   = funding step × C                                effective funding
S*  = curve(E) / value at 100%                        target strength, per modifier
S   = S + 0.25 × (S* − S)                             smoothed strength
apply modifier "<law>_<modifier>" with multiplier S
```

**Why the local term:** with one national good, every state would otherwise get identical coverage. A state with no hospitals of its own would be as well served as one with many. The 50/50 blend means national supply still helps, but building providers where people live matters.

**Why smoothing:** outcomes respond over a few months, as real services do, and one bad month doesn't make modifiers flicker.

## 4. Worked example – a capital under Universal Public Healthcare

- Urban center: 3,592 levels (see the urbanization explainer)
- Law: Universal Public Healthcare (allowed range 75–200%)
- Funding PM: **150%** → demand 0.25 × 6 = 1.5 per level → **5,388 healthcare per week**
- At a base price of 50, the government spends about **£269,000/week** on this state

Supply this month:
- National: sell 900,000 / buy 1,000,000 → Fn = 0.90
- Local: state production 3,800 / state consumption 5,430 (urban center plus pops) → Fl = 0.70
- **Coverage C = 0.80**
- **Effective funding E = 150% × 0.80 = 120%**

Universal's `state_mortality_mult` curve (from `Service Economy.md`): 100% → −0.30, 125% → −0.34. At 120%, interpolate: −0.30 + (20/25) × (−0.04) = **−0.332**.
Target strength S* = 0.332 / 0.30 = **1.107**.

Last month the state was fully supplied at 150% (−0.37, S = 1.233). Smoothed:
S = 1.233 + 0.25 × (1.107 − 1.233) = **1.202** → modifier applied this month: −0.30 × 1.202 = **−0.361**.

If the shortage persists, the effect settles at −0.332 within a few months. Meanwhile the shortage pushes healthcare's price up, so the government pays more per unit. The fix is to build hospitals in this state, which raises Fl, or nationally, which raises Fn.

Tooltip shown to the player: *"Healthcare coverage: 80% of funded level (national 90%, local 70%). Effective funding 120%."*

## 5. Laws and ranges

| System | Law | Range |
|---|---|---|
| Healthcare | No Public / Basic / Universal / Mixed / Private | 0 / 25–100 / 75–200 / 50–150 / 0–75 |
| Education | No Schools / Religious / Public / Mixed / Private | 0 / 25–100 / 75–200 / 50–150 / 0–75 |
| Policing | No Police / Local / Dedicated / Militarized | 0 / 25–150 / 50–200 / 75–200 |

Changing law: states whose funding is outside the new range are moved to the nearest allowed step, with a notification.

## 6. One modifier per law per modifier type

Your tables don't scale every modifier of a law in proportion. Mixed Healthcare, for example, goes from −0.18 to −0.24 flat (×1.33) but −0.0010 to −0.0014 wealth-weighted (×1.40) between 100% and 150%. So each modifier gets its own static modifier and its own multiplier:

| System | Static modifiers per law | Total (all laws) |
|---|---|---|
| Healthcare | 2 (flat, wealth) | 10 |
| Education | 3 (access, wealth access, literacy growth) | 15 |
| Policing | up to 6 | 24 |

These are created once, and the script only changes the multipliers.

## 7. Open decision D1 – No Public Healthcare

No Public Healthcare locks funding at 0%, but its table row gives a wealth-weighted mortality benefit at 100% (private provision). With funding at 0, the benefit would never appear.

**Proposal:** for healthcare, the **flat** modifier scales with public effective funding (as above), while the **wealth** modifier scales with national healthcare fulfilment Fn only, since it represents what better-off pops buy privately. This keeps the identity of every law in the table:

- No Public: wealth effect only, if the private market is supplied
- Private: large wealth effect plus a small public element
- Universal: flat effect only, fully dependent on public funding

## 8. Who pays and where the money goes

```
Government budget ──► Urban Center purchases ──┐
Pops' private spending ────────────────────────┼──► national market ──► providers
                                               │
Government-owned providers: wages + inputs; losses from / profits to the treasury
Private providers: wages + inputs; profits to owners; unprofitable levels downsize
```

## 9. AI

- Picks the highest allowed funding step it can afford; raises funding in populous states first when in surplus, and cuts in small states first when in deficit.
- Builds providers where coverage is lowest, preferring the states with the largest local gap.
