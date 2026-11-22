# Explainer – Research & Technology

Companion to `CWP Economy Rework Proposal.md`, section 13. Numbers are starting values.

## 1. Aims

- Rich countries that invest in research should be able to **stay ahead**; there is no hard ceiling on innovation.
- Countries can **specialise** (e.g. pushing semiconductors early) without an artificial penalty.
- Each new era should cost **much more** than the last, reflecting the growing effort behind each step.
- Countries that follow should find it **easier** than the pioneer, and should be able to **buy** knowledge.

## 2. Changes at a glance

| # | Change | Mechanism |
|---|---|---|
| 1 | Remove ahead-of-era penalty | Set the define for the later-era cost penalty to 0 (define name to verify) |
| 2 | Steeper era costs | `technology_cost` per era (table below) |
| 3 | Raise innovation cap | Large `country_weekly_innovation_max_add` base |
| 4 | University focus | Per-tree speed/spread modifiers by PM |
| 5 | Company HQ innovation | Innovation per HQ level, boosted by prosperity |
| 6 | Followers research faster | `country_tech_group_research_speed_mult` base modifier |
| 7 | Technology Licensing | New treaty article + monthly `add_technology_progress` |

## 3. Era costs

Current costs rise by a flat ~2,500 per era. Proposed: the multiplier between eras grows from ×1.5 to ×2.

| Era | Period (mod comments) | Current | Multiplier | Proposed |
|---|---|---|---|---|
| era_1 | pre-1940 | 5,000 | — | 5,000 |
| era_2 | 1940–50 | 7,500 | ×1.5 | 7,500 |
| era_3 | 1950–60 | 10,000 | ×1.5 | 11,250 |
| era_4 | 1960–70 | 12,500 | ×1.5 | 16,875 |
| era_5 | 1970–80 | 15,000 | ×1.6 | 27,000 |
| era_6 | 1980–90 | 17,500 | ×1.6 | 43,200 |
| era_7 | 1990–2000 | 20,000 | ×1.7 | 73,440 |
| era_8 | 2000–10 | 22,250 | ×1.7 | 124,848 |
| era_9 | 2010–20 | 25,000 | ×1.8 | 224,726 |
| era_10 | 2020–30 | 27,500 | ×1.9 | 426,980 |
| era_11 | 2030–40 | 30,000 | ×2.0 | 853,960 |
| era_12 | post-2040 | 35,000 | ×2.0 | 1,707,920 |

**Consequence:** innovation output must grow with the economy, or late eras stall. A leading economy's innovation should grow roughly in line with these costs (×1.5–2 per decade). That comes from more and better universities, Company HQs growing with companies, and the raised cap. Calibrate so the **leading** country researches each era in roughly its historical decade, and a mid-ranked country lags 1–2 eras by 2000.

**Progress bonuses:** the era file comments say progress bonuses use about a third of the era cost. Those event/JE values need rescaling to the new costs.

## 4. University focus PMs

| Focus | Modifiers (per level, starting values) | IG |
|---|---|---|
| General Research | highest `country_weekly_innovation_add` | Intelligentsia +approval |
| Qualifications | lower innovation; qualifications growth in the state | Intelligentsia |
| Industrial & Applied Science | `country_production_tech_research_speed_mult` +0.2%, `country_production_tech_spread_mult` +0.5% | Industrialists |
| Social Sciences | `country_society_tech_research_speed_mult` +0.2%, `_spread_mult` +0.5% | Intelligentsia / Trade Unions |
| Defence Research | `country_military_tech_research_speed_mult` +0.2%, `_spread_mult` +0.5% | Armed Forces |

Per-level values are small because they add up across all university levels in the country. A cap or diminishing returns may be needed (e.g. a maximum of +50% per tree) to verify.

## 5. Company HQ innovation

- Each Company HQ level gives a small `country_weekly_innovation_add`, so innovation scales with company size.
- While the company has its **prosperity bonus**, HQ innovation is doubled (via the company type's prosperity modifier or a scripted check, to verify).
- Regional HQs give none.

This rewards building large, profitable companies, which in the mod represent major national firms.

## 6. Followers research faster

`country_tech_group_research_speed_mult` gives research speed that scales with **how many countries already have the technology**. A base country modifier (starting value +50%, to verify semantics) means:

- The **pioneer** pays full cost.
- Once a technology is widespread, latecomers research it much faster: less risk, known path.
- This works alongside the existing tech spread.

## 7. Technology Licensing (treaty article)

| Aspect | Design |
|---|---|
| Parties | Licensor (has techs) and licensee (lacks them) |
| Licensee gets | Each month, `add_technology_progress` equal to **5% of the tech's cost** toward a chosen tech the licensor has (licensee picks; default is the cheapest missing tech) |
| Licensor gets | A weekly fee from the licensee; small relations increase |
| Fee (starting value) | Per year ≈ tech cost × £2, paid weekly; scales with era, so modern licences are expensive |
| Restrictions | **Military** technologies only between countries in an alliance, defensive pact or the same power bloc |
| Duration | Like other treaty articles; ends when the licensee has no more eligible techs |
| Implementation | The weekly or monthly hook on treaty articles, if it exists; otherwise a monthly on_action over countries with the article |

At 5% per month, licensing a tech takes ~20 months. It's slower than a strong country's own research but faster than a weak country's, and costs money instead of innovation. This is the systemic version of "buying research": it applies to any country pair, with no historical scripting.

## 8. AI

- University focus: weighted by AI strategy (militarist → Defence; industrial → Industrial & Applied Science; otherwise General).
- Licensing: AI seeks licences when far behind in a tree and able to pay the fee; offers licences to friendly countries; won't license military techs to rivals.
