# Explainer – Urbanization Model

Companion to `CWP Economy Rework Proposal.md`, section 5. All numbers are illustrative.

## 1. The problem

Vic3 gives each building group a fixed `urbanization` per level. A wheat farm level and a car plant level differ only by that one number, regardless of who works there or what they make. Urban centers, which this rework uses to drive public service demand, need a measure that reflects the real economic structure of a state.

The engine can't add urbanization to a state from script. It can change **how much urbanization each urban center level needs**. The model uses that lever.

## 2. Three steps

```
 (1) Calculate X           (2) Smooth X              (3) Convert to levels
 workers + goods  ──►  stored value moves   ──►  set urbanization-per-level
 in the state          toward X each month       so levels = floor(X / 100)
```

### Step 1 – Calculate X

```
X = (WorkforceScore / 40) + InputScore + OutputScore + ((InputScore + OutputScore) / 5)
```

- **WorkforceScore** = Σ employed workforce × job-type value
  + Σ unemployed workforce × job-type value × 0.5
  + Σ dependants (pop size − workforce) × job-type value × 0.25
- **InputScore** = Σ over goods: consumption in the state × input value (includes pop consumption: shops, supermarkets and distribution are urban)
- **OutputScore** = Σ over goods: production in the state × output value

Job-type and goods values: the tables in `Service Economy.md`.

### Step 2 – Smooth

Stored urbanization moves toward X each month:
- by **5% of the gap** when X is higher (growth)
- by **2% of the gap** when X is lower (decline)

Half-life: growth ≈ 13.5 months; decline ≈ 34 months. A new industrial zone fills out within a couple of years; a city that loses its industry shrinks over many years, like real urban decline.

### Step 3 – Convert to levels

With **Y** = the urbanization the game itself calculates for the state:

```
urbanization needed per level  T = 100 × Y / X        (rounded to 0.001, minimum 0.001)
urban center levels            = floor(Y / T) = floor(X / 100)
```

Implemented as a state modifier `state_urbanization_per_level_add = −(100 − T)` (assuming a base of 100 per level, to be verified, and offsetting any other modifiers to the same value).

Y doesn't matter to the result as long as it's above zero. Building-group urbanization values can be retuned freely.

## 3. Worked example A – industrial city

| Employed pops | Workforce | Value | Score |
|---|---|---|---|
| Machinists | 300,000 | 10 | 3,000,000 |
| Clerks | 150,000 | 8 | 1,200,000 |
| Shopkeepers | 100,000 | 7 | 700,000 |
| Engineers | 50,000 | 9 | 450,000 |
| Laborers | 200,000 | 2 | 400,000 |
| **Employed total** | **800,000** | | **5,750,000** |

- Unemployed: 40,000 Machinists × 10 × 0.5 = **200,000**
- Dependants: pop size twice the workforce, so 800,000 dependants. Their average job value is 5,750,000 / 800,000 ≈ 7.19, giving 800,000 × 7.19 × 0.25 ≈ **1,437,500**
- WorkforceScore = 7,387,500 → / 40 = **184,688**

| Goods | Quantity | Value | Score |
|---|---|---|---|
| *Output:* steel | 2,000 | 8 | 16,000 |
| *Output:* automobiles | 500 | 10 | 5,000 |
| *Output:* electricity | 3,000 | 9 | 27,000 |
| **OutputScore** | | | **48,000** |
| *Input:* iron | 2,500 | 3 | 7,500 |
| *Input:* coal | 3,000 | 4 | 12,000 |
| *Input:* electricity | 3,000 | 9 | 27,000 |
| *Input:* groceries (mostly pops) | 4,000 | 6 | 24,000 |
| *Input:* services (pops) | 3,000 | 9 | 27,000 |
| **InputScore** | | | **97,500** |

- Bonus term: (97,500 + 48,000) / 5 = **29,100**
- **X = 184,688 + 97,500 + 48,000 + 29,100 = 359,288 → 3,592 urban center levels**
- If the game's own urbanization Y = 4,000: T = 100 × 4,000 / 359,288 ≈ 1.113, and 4,000 / 1.113 ≈ 3,593 levels. Rounding T to 0.001 introduces at most a level or two of error.

## 4. Worked example B – agrarian state

| Employed pops | Workforce | Value | Score |
|---|---|---|---|
| Farmers | 500,000 | 0.5 | 250,000 |
| Peasants (subsistence) | 1,000,000 | 0 | 0 |
| Shopkeepers | 20,000 | 7 | 140,000 |
| Bureaucrats | 10,000 | 6 | 60,000 |
| **Total** | **1,530,000** | | **450,000** |

- Dependants: 1,530,000 × (450,000 / 1,530,000) × 0.25 = 112,500
- WorkforceScore = 562,500 → / 40 = **14,063**
- InputScore (grain, groceries, services consumed) ≈ 9,700; OutputScore (wood, fruit/grain at 0–1) ≈ 1,000; bonus ≈ 2,140
- **X ≈ 26,900 → 269 urban center levels**, despite having almost twice the workforce of example A

Ratio A : B ≈ 13 : 1 per state, or ≈ 25 : 1 per worker.

## 5. What this produces in play

| Change in the state | Effect on urban center |
|---|---|
| New car plant (Machinists, Engineers; steel and electricity in, automobiles out) | Large, fast increase |
| Farm mechanisation (Farmers released, unemployed) | Small decrease. Farmers were worth little; migrants raise urbanization in the cities they move to once employed |
| Factory closes (Machinists unemployed) | Machinists drop to half value, goods scores fall; levels shrink slowly over ~3 years |
| Population boom in a working city | Dependants raise urbanization modestly (25% weight) |
| Pops get richer and buy more | Input score rises: more consumption = more retail infrastructure |

## 6. Performance

Per state per month: one loop over pops, about 60 goods × 2 lookups, and a few arithmetic steps. Run in the same monthly pass as public service coverage. If testing shows lag: update quarterly, or skip states whose workforce and production changed less than ~1% since last month.

## 7. To verify in a test build

1. The base urbanization per urban center level, and whether `state_urbanization_per_level_add` accepts values down to 0.001.
2. That `sg:<good>` production/consumption and pop workforce can be summed into script values (expected: yes; comparison triggers can usually be used as values).
3. That urban center levels update promptly when the modifier changes.
