# IPL-Data-Analyst-Dashboard
# 🏏 IPL Data Analyst

An interactive IPL analytics dashboard built with **Dash**, **Plotly** and **Pandas**. It turns raw ball-by-ball IPL data into KPI cards, season and venue breakdowns, batting and bowling leaderboards, and a **smart search engine** that builds an on-the-fly player or team profile from a single keyword.

Search `kohli` and you get a full batting dashboard. Search `bumrah` and you get bowling metrics. Search a name that exists in both datasets and the app recognises an **all-rounder** and shows both profiles together. Search `csk` and it resolves the alias to *Chennai Super Kings* and charts their season-wise wins.

---

## Table of Contents

- [Features](#features)
- [Dashboard Preview](#dashboard-preview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Datasets Required](#datasets-required)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [How the Smart Search Works](#how-the-smart-search-works)
- [Supported Team Aliases](#supported-team-aliases)
- [KPI Definitions](#kpi-definitions)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Features

### KPI summary strip
Four cards computed at load time: total matches, total players, total teams and total seasons.

### Dashboard analytics (8 charts, rendered on load)

| # | Chart | Type | What it shows |
|---|-------|------|---------------|
| 1 | IPL Matches Per Season | Bar | Match volume across every season |
| 2 | Most Successful IPL Teams | Donut | Share of all match wins by team |
| 3 | Top 10 Run Scorers | Bar | Highest aggregate `batsman_runs` |
| 4 | Top 10 Wicket Takers | Bar | Leading wicket takers |
| 5 | Toss Decision Analysis | Pie | Bat first vs field first split |
| 6 | Top IPL Venues | Bar | Ten grounds that have hosted the most matches |
| 7 | Economy vs Wickets | Scatter | Bowler trade-off, bubble size = wickets |
| 8 | Average vs Strike Rate | Scatter | Bowling consistency vs penetration |

### Smart search engine

A single search box resolves the query in this priority order:

1. **All-rounder** — name matches both a batter in `deliveries.csv` and a bowler in `bowler_stats.csv` → shows batting profile, bowling profile and a green all-rounder banner.
2. **Batter** — name matches a batter → batting profile.
3. **Bowler** — name matches a bowler → bowling profile.
4. **Team** — name (or alias) matches a winning team → team profile.
5. **No match** — a friendly "No Results Found" message.

### Player and team profiles

**Batting profile**
- Headline numbers: runs, balls faced, strike rate, fours, sixes
- Season-wise runs trend (line, with markers)
- Season-wise strike rate trend (line, with markers)
- Boundary breakdown — fours vs sixes (bar)

**Bowling profile**
- Matches, balls, overs, runs, wickets, economy, average, strike rate
- Bowling metrics comparison (bar)

**Team profile**
- Total wins
- Season-wise wins (bar)
- Winning trend over seasons (line)

---

## Dashboard Preview

```
┌──────────────────────────────────────────────────────────────────┐
│                      🏏 IPL DATA ANALYST                         │
├──────────────────────────────────────────────────────────────────┤
│  📅 Total Matches  🏏 Total Players  👥 Total Teams  🏆 Seasons   │
├──────────────────────────────────────────────────────────────────┤
│  🔍 Smart IPL Search Engine                                      │
│  ┌───────────────────────────────┐  ┌────────┐                   │
│  │ Search Player / Bowler / Team │  │ Search │                   │
│  └───────────────────────────────┘  └────────┘                   │
├──────────────────────────────────────────────────────────────────┤
│  (dynamic profile appears here)                                  │
├──────────────────────────────────────────────────────────────────┤
│  📊 IPL Dashboard Analytics                                      │
│  [ Matches/Season ] [ Winning Teams ] [ Top Batsmen ]            │
│  [ Top Bowlers ]    [ Toss Decision ] [ Top Venues ]             │
│  [ Economy vs Wickets ]  [ Average vs Strike Rate ]              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| `dash` | Web framework, layout, callbacks |
| `plotly.express` / `plotly.graph_objects` | All charts |
| `pandas` | Data loading, cleaning, grouping, merging |

No frontend build step is needed — the entire UI is declared in Python and served by Dash's development server.

---

## Project Structure

```
ipl-data-analyst/
│
├── final_ipl_project.py        # The complete application (single file)
│
├── matches.csv                 # Match-level data
├── deliveries.csv              # Ball-by-ball data
├── bowler_stats.csv            # Pre-aggregated bowling career stats
├── IPL.csv                     # Loaded (reserved for future use)
├── players-data-updated.csv    # Loaded (reserved for future use)
├── teams_data.csv              # Loaded (reserved for future use)
├── team_aliases.csv            # Loaded (aliases are currently hard-coded)
├── season_winners.csv          # Loaded (reserved for future use)
│
└── README.md
```

All CSVs must sit in the **same directory** as `final_ipl_project.py`, because the script reads them by bare relative filename.

---

## Datasets Required

### `matches.csv` — one row per match

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Match identifier (cast to int at load) |
| `season` | str/int | IPL season |
| `team1`, `team2` | str | Competing teams |
| `winner` | str | Winning team |
| `toss_decision` | str | `bat` or `field` |
| `venue` | str | Ground name |

### `deliveries.csv` — one row per ball

| Column | Type | Description |
|--------|------|-------------|
| `match_id` | int | Foreign key to `matches.id` (cast to int at load) |
| `batter` | str | Batter on strike |
| `batsman_runs` | int | Runs credited to the batter |
| `ball` | int | Ball number — required for the strike-rate trend |

### `bowler_stats.csv` — one row per bowler (pre-aggregated)

| Column | Description |
|--------|-------------|
| `Bowler` | Bowler name |
| `Matches` | Matches played |
| `Balls` | Balls bowled |
| `Overs` | Overs bowled |
| `Runs` | Runs conceded |
| `Wickets` | Wickets taken |
| `Economy` | Runs per over |
| `Average` | Runs per wicket |
| `Strike_Rate` | Balls per wicket |

> Column names in `bowler_stats.csv` are **case-sensitive** and must match exactly (`Strike_Rate`, not `StrikeRate`), because the code indexes them directly.

### Placeholder files

`IPL.csv`, `players-data-updated.csv`, `teams_data.csv`, `team_aliases.csv` and `season_winners.csv` are read at startup but not yet used by any chart or callback. They are loaded so that extending the app does not require touching the import block. If you don't have them yet, either create empty CSVs with a header row or comment out the corresponding `read_csv` lines.

### Data cleaning applied at load

- `matches`: all nulls filled with `"Unknown"`
- `deliveries`: all nulls filled with `0`
- `matches.id` and `deliveries.match_id` cast to `int` so the merge on match ID is reliable

---

## Installation

Requires **Python 3.8+**.

```bash
# 1. Clone or download the project
git clone <your-repo-url>
cd ipl-data-analyst

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install pandas plotly dash
```

If you prefer pinned versions, create a `requirements.txt`:

```txt
pandas>=2.0
plotly>=5.18
dash>=2.14
```

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
python final_ipl_project.py
```

Then open **http://127.0.0.1:8050** in your browser.

The server starts with `debug=False` on port **8050**. To develop with hot reload, change the final line of the script:

```python
app.run(debug=True, port=8050)
```

---

## How the Smart Search Works

The `search_data` callback listens on the **Search** button and reads the input box as state.

```
User types a keyword
        │
        ▼
  lowercase + strip whitespace
        │
        ├──► match against deliveries.batter        → batter_data
        ├──► match against bowler_stats.Bowler      → bowler_data
        ├──► match against matches.winner           → team_data
        └──► resolve team alias (csk → Chennai Super Kings) if applicable
        │
        ▼
  batter AND bowler?  → All-rounder profile (batting + bowling)
  batter only?        → Batting profile
  bowler only?        → Bowling profile
  team only?          → Team profile
  nothing?            → "No Results Found"
```

Matching is **case-insensitive** and **substring-based**, so partial names work — `kohl` finds *V Kohli*, and `mumbai` finds *Mumbai Indians*. Every callback is wrapped in `try/except`, so a missing column or a bad row renders an inline error message in the results panel instead of crashing the app.

---

## Supported Team Aliases

| Alias | Team |
|-------|------|
| `csk` | Chennai Super Kings |
| `mi` | Mumbai Indians |
| `rcb` | Royal Challengers Bengaluru |
| `kkr` | Kolkata Knight Riders |
| `srh` | Sunrisers Hyderabad |
| `dc` | Delhi Capitals |
| `pbks` | Punjab Kings |
| `rr` | Rajasthan Royals |
| `gt` | Gujarat Titans |
| `lsg` | Lucknow Super Giants |

The alias map lives inside the `search_data` callback as a Python dictionary — edit it there to add new franchises. Note that a bare `dc`, `mi` or `rr` also substring-matches player names, so aliases are checked as exact matches first.

---

## KPI Definitions

| KPI | How it is calculated |
|-----|----------------------|
| **Total Matches** | Row count of `matches.csv` |
| **Total Players** | Unique values in `deliveries.batter` |
| **Total Teams** | Unique values across `matches.team1` and `matches.team2` combined |
| **IPL Seasons** | Unique values in `matches.season` |

Batter strike rate inside a profile is `(total runs ÷ balls faced) × 100`, where balls faced is the row count for that batter.

---

## Configuration

| Setting | Location | Default |
|---------|----------|---------|
| Port | Last line of the file | `8050` |
| Debug mode | Last line of the file | `False` |
| App title (browser tab) | `app.title` | `"IPL Data Analyst"` |
| Page background | `app.layout` style | `#F4F6F9` |
| Brand colour (headings, button) | Inline styles | `#0B3D91` |
| Leaderboard depth | `.head(10)` calls | Top 10 |
| Top venues shown | `venue_df.head(10)` | Top 10 |

---

## Troubleshooting

**`FileNotFoundError: matches.csv`**
The CSVs are not in the working directory. Run the script from the folder that contains them, or switch to absolute paths.

**`KeyError: 'batter'` / `'batsman_runs'` / `'ball'`**
Your `deliveries.csv` uses different column names (for example `batsman` instead of `batter`). Rename the columns to match the table above, or update the column references in the code.

**`KeyError: 'Strike_Rate'` in the bowling profile**
`bowler_stats.csv` is missing a column or has different capitalisation. Headers must match exactly.

**Strike rate trend is flat or wildly high**
The trend divides by `ball` count grouped by season. If your `deliveries.csv` has no `ball` column, or contains rows already aggregated differently, the denominator will be wrong.

**Empty or blank charts**
Usually caused by nulls in the grouping column. The load step fills nulls, but check that `season`, `winner` and `venue` are populated in your source data.

**Port 8050 already in use**
Change the port: `app.run(port=8051)`.

**Search always says "No Results Found"**
Check that `deliveries.batter` and `bowler_stats.Bowler` hold full player names, and that you are not searching with trailing punctuation. Matching is substring-based, so a plain surname is the safest query.

---

## Known Limitations

- **Single-file architecture** — data loading, cleaning, chart building, layout and callbacks all live in one module. Fine for a portfolio project; split into `data/`, `figures/`, `callbacks/` and `layout/` if this grows.
- **Pre-aggregated bowling stats** — bowling figures come from a static `bowler_stats.csv` rather than being computed from `deliveries.csv`, so they will not update when new match data is added.
- **No run-rate, phase or partnership analysis** — powerplay, middle overs and death-overs splits are not implemented.
- **Ambiguous substring matching** — short queries can match several players; the app uses the first match rather than offering a disambiguation list.
- **Aliases are hard-coded** — `team_aliases.csv` is loaded but the callback uses an in-code dictionary.
- **Team history is not normalised** — franchise renames (Delhi Daredevils → Delhi Capitals, Kings XI Punjab → Punjab Kings, Bangalore → Bengaluru) appear as separate teams unless your CSVs are already reconciled.
- **No caching or database layer** — every restart re-reads and recomputes everything.
- **No authentication or deployment config** — this is a local development server.

---

## Roadmap

- Compute bowling stats directly from `deliveries.csv` so everything stays in sync
- Add phase-wise (powerplay / middle / death) batting and bowling splits
- Player-vs-player head-to-head search
- Season and team filters that drive every chart
- Automatic team-name normalisation from `team_aliases.csv`
- Move the alias map and data paths into a config file
- Deploy on Render, Railway or Hugging Face Spaces
- Add a data-refresh script for new seasons

---

## Author

**Raj Ratan Panigrahi**

Built as an end-to-end data analytics portfolio project — raw ball-by-ball data in, an interactive dashboard out.

---

*Data source: publicly available IPL match and ball-by-ball datasets. This project is unaffiliated with the BCCI or the Indian Premier League; team and player names are used for analytical purposes only.*
