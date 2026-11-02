# =========================================================
# IPL DATA ANALYST V2 - CORRECTED VERSION
# PROFESSIONAL IPL ANALYTICS DASHBOARD
# =========================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
    State
)

# =========================================================
# LOAD DATASETS
# =========================================================

matches = pd.read_csv("matches.csv")
delivery = pd.read_csv("deliveries.csv")
ipl = pd.read_csv("IPL.csv")
players = pd.read_csv("players-data-updated.csv")
teams = pd.read_csv("teams_data.csv")
aliases = pd.read_csv("team_aliases.csv")
winners = pd.read_csv("season_winners.csv")
bowler_stats = pd.read_csv("bowler_stats.csv")

# =========================================================
# CLEAN DATA
# =========================================================

matches.fillna("Unknown", inplace=True)
delivery.fillna(0, inplace=True)
matches["id"] = matches["id"].astype(int)
delivery["match_id"] = delivery["match_id"].astype(int)

# =========================================================
# CREATE DASH APP
# =========================================================

app = Dash(__name__)
app.title = "IPL Data Analyst"

# =========================================================
# KPI CARDS
# =========================================================

TOTAL_MATCHES = matches.shape[0]
TOTAL_PLAYERS = len(delivery["batter"].unique())
TOTAL_TEAMS = len(
    pd.concat([
        matches["team1"],
        matches["team2"]
    ]).unique()
)
TOTAL_SEASONS = len(matches["season"].unique())

# =========================================================
# MATCHES PER SEASON
# =========================================================

season_matches = (
    matches
    .groupby("season")
    .size()
    .reset_index(name="Matches")
)

fig_matches = px.bar(
    season_matches,
    x="season",
    y="Matches",
    color="Matches",
    title="IPL Matches Per Season"
)

# =========================================================
# WINNING TEAMS
# =========================================================

winner_count = (
    matches["winner"]
    .value_counts()
    .reset_index()
)

winner_count.columns = ["Team", "Wins"]

fig_winner = px.pie(
    winner_count,
    names="Team",
    values="Wins",
    hole=0.5,
    title="Most Successful IPL Teams"
)

# =========================================================
# TOP BATSMEN
# =========================================================

top_batsman = (
    delivery
    .groupby("batter")["batsman_runs"]
    .sum()
    .reset_index()
)

top_batsman = top_batsman.sort_values(
    by="batsman_runs",
    ascending=False
).head(10)

fig_batsman = px.bar(
    top_batsman,
    x="batter",
    y="batsman_runs",
    color="batsman_runs",
    title="Top 10 Run Scorers"
)

# =========================================================
# TOP BOWLERS
# =========================================================

top_bowlers = (
    bowler_stats
    .sort_values(by="Wickets", ascending=False)
    .head(10)
)

fig_bowler = px.bar(
    top_bowlers,
    x="Bowler",
    y="Wickets",
    color="Wickets",
    title="Top 10 Wicket Takers"
)

# =========================================================
# TOSS ANALYSIS
# =========================================================

fig_toss = px.pie(
    matches,
    names="toss_decision",
    title="Toss Decision Analysis"
)

# =========================================================
# VENUE ANALYSIS
# =========================================================

venue_df = (
    matches["venue"]
    .value_counts()
    .reset_index()
    .head(10)
)

venue_df.columns = ["Venue", "Matches"]

fig_venue = px.bar(
    venue_df,
    x="Venue",
    y="Matches",
    color="Matches",
    title="Top IPL Venues"
)

# =========================================================
# ECONOMY VS WICKETS
# =========================================================

fig_bowling_scatter = px.scatter(
    bowler_stats,
    x="Economy",
    y="Wickets",
    hover_name="Bowler",
    size="Wickets",
    title="Economy vs Wickets"
)

# =========================================================
# AVERAGE VS STRIKE RATE
# =========================================================

fig_avg_sr = px.scatter(
    bowler_stats,
    x="Average",
    y="Strike_Rate",
    hover_name="Bowler",
    size="Wickets",
    title="Average vs Strike Rate"
)

# =========================================================
# APP LAYOUT
# =========================================================

app.layout = html.Div(
    [
        # =====================================================
        # TITLE
        # =====================================================
        html.H1(
            "🏏 IPL DATA ANALYST",
            style={
                "textAlign": "center",
                "color": "#0B3D91",
                "fontSize": "42px",
                "marginBottom": "20px"
            }
        ),
        html.Hr(),

        # =====================================================
        # KPI CARDS
        # =====================================================
        html.Div(
            [
                html.Div(
                    [
                        html.H3("📅 Total Matches"),
                        html.H2(TOTAL_MATCHES)
                    ],
                    style={
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "width": "22%",
                        "textAlign": "center",
                        "boxShadow": "2px 2px 10px lightgrey"
                    }
                ),
                html.Div(
                    [
                        html.H3("🏏 Total Players"),
                        html.H2(TOTAL_PLAYERS)
                    ],
                    style={
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "width": "22%",
                        "textAlign": "center",
                        "boxShadow": "2px 2px 10px lightgrey"
                    }
                ),
                html.Div(
                    [
                        html.H3("👥 Total Teams"),
                        html.H2(TOTAL_TEAMS)
                    ],
                    style={
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "width": "22%",
                        "textAlign": "center",
                        "boxShadow": "2px 2px 10px lightgrey"
                    }
                ),
                html.Div(
                    [
                        html.H3("🏆 IPL Seasons"),
                        html.H2(TOTAL_SEASONS)
                    ],
                    style={
                        "backgroundColor": "#ffffff",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "width": "22%",
                        "textAlign": "center",
                        "boxShadow": "2px 2px 10px lightgrey"
                    }
                )
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "30px"
            }
        ),
        html.Hr(),

        # =====================================================
        # SEARCH ENGINE
        # =====================================================
        html.Div(
            [
                html.H2(
                    "🔍 Smart IPL Search Engine",
                    style={"color": "#0B3D91"}
                ),
                dcc.Input(
                    id="search-box",
                    type="text",
                    placeholder="Search Player / Bowler / Team",
                    style={
                        "width": "500px",
                        "height": "50px",
                        "fontSize": "18px",
                        "borderRadius": "10px",
                        "paddingLeft": "10px"
                    }
                ),
                html.Button(
                    "Search",
                    id="search-button",
                    n_clicks=0,
                    style={
                        "height": "52px",
                        "fontSize": "18px",
                        "marginLeft": "10px",
                        "backgroundColor": "#0B3D91",
                        "color": "white",
                        "border": "none",
                        "padding": "10px 20px",
                        "borderRadius": "10px"
                    }
                )
            ],
            style={"textAlign": "center"}
        ),
        html.Br(),

        # =====================================================
        # SEARCH RESULT AREA
        # =====================================================
        html.Div(
            id="search-output",
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "15px",
                "boxShadow": "2px 2px 10px lightgrey"
            }
        ),
        html.Hr(),

        # =====================================================
        # DASHBOARD ANALYTICS
        # =====================================================
        html.H2(
            "📊 IPL Dashboard Analytics",
            style={"textAlign": "center", "color": "#0B3D91"}
        ),
        dcc.Graph(figure=fig_matches),
        dcc.Graph(figure=fig_winner),
        dcc.Graph(figure=fig_batsman),
        dcc.Graph(figure=fig_bowler),
        dcc.Graph(figure=fig_toss),
        dcc.Graph(figure=fig_venue),
        dcc.Graph(figure=fig_bowling_scatter),
        dcc.Graph(figure=fig_avg_sr)
    ],
    style={
        "backgroundColor": "#F4F6F9",
        "padding": "20px"
    }
)

# =========================================================
# BATTER ANALYTICS
# =========================================================

def get_batter_stats(player_data, player_name):
    """✓ FIX: Added docstring and improved error handling"""
    result = []

    try:
        total_runs = player_data["batsman_runs"].sum()
        total_balls = player_data.shape[0]
        total_fours = player_data[
            player_data["batsman_runs"] == 4
        ].shape[0]
        total_sixes = player_data[
            player_data["batsman_runs"] == 6
        ].shape[0]

        strike_rate = round(
            (total_runs / total_balls) * 100,
            2
        ) if total_balls > 0 else 0

        result.append(html.H1(f"🏏 {player_name}"))
        result.append(html.H2("Batting Analytics"))
        result.append(html.H3(f"Runs : {total_runs}"))
        result.append(html.H3(f"Balls : {total_balls}"))
        result.append(html.H3(f"Strike Rate : {strike_rate}"))
        result.append(html.H3(f"Fours : {total_fours}"))
        result.append(html.H3(f"Sixes : {total_sixes}"))

        merged = pd.merge(
            matches,
            player_data,
            left_on="id",
            right_on="match_id",
            how="inner"
        )

        # ============================================
        # SEASON WISE RUNS
        # ============================================
        season_runs = (
            merged
            .groupby("season")["batsman_runs"]
            .sum()
            .reset_index()
        )

        fig_runs = px.line(
            season_runs,
            x="season",
            y="batsman_runs",
            markers=True,
            title=f"{player_name} Season Wise Runs"
        )

        result.append(dcc.Graph(figure=fig_runs))

        # ============================================
        # STRIKE RATE TREND
        # ============================================
        season_sr = (
            merged
            .groupby("season")
            .agg({
                "batsman_runs": "sum",
                "ball": "count"  # ✓ VERIFY: Is column called "ball"?
            })
            .reset_index()
        )

        season_sr["strike_rate"] = (
            season_sr["batsman_runs"] /
            season_sr["ball"]
        ) * 100

        fig_sr = px.line(
            season_sr,
            x="season",
            y="strike_rate",
            markers=True,
            title=f"{player_name} Strike Rate Trend"
        )

        result.append(dcc.Graph(figure=fig_sr))

        # ============================================
        # BOUNDARY ANALYSIS
        # ============================================
        boundary_df = pd.DataFrame({
            "Type": ["Fours", "Sixes"],
            "Count": [total_fours, total_sixes]
        })

        fig_boundary = px.bar(
            boundary_df,
            x="Type",
            y="Count",
            color="Type",
            title=f"{player_name} Boundary Analysis"
        )

        result.append(dcc.Graph(figure=fig_boundary))

    except KeyError as e:
        result.append(html.H1(f"❌ Column Error: {e}"))
    except Exception as e:
        result.append(html.H1(f"❌ Error: {str(e)}"))

    return result

# =========================================================
# BOWLER ANALYTICS
# =========================================================

def get_bowler_stats(bowler_row):
    """✓ FIX: Added docstring"""
    result = []

    try:
        result.append(html.H2("🎯 Bowling Analytics"))
        result.append(html.H3(f"Matches : {bowler_row['Matches']}"))
        result.append(html.H3(f"Balls : {bowler_row['Balls']}"))
        result.append(html.H3(f"Overs : {bowler_row['Overs']}"))
        result.append(html.H3(f"Runs : {bowler_row['Runs']}"))
        result.append(html.H3(f"Wickets : {bowler_row['Wickets']}"))
        result.append(html.H3(f"Economy : {bowler_row['Economy']}"))
        result.append(html.H3(f"Average : {bowler_row['Average']}"))
        result.append(html.H3(f"Strike Rate : {bowler_row['Strike_Rate']}"))

        # ============================================
        # BOWLING METRICS
        # ============================================
        metrics = pd.DataFrame({
            "Metric": ["Wickets", "Economy", "Average", "Strike Rate"],
            "Value": [
                bowler_row["Wickets"],
                bowler_row["Economy"],
                bowler_row["Average"],
                bowler_row["Strike_Rate"]
            ]
        })

        fig_metrics = px.bar(
            metrics,
            x="Metric",
            y="Value",
            color="Metric",
            title="Bowling Metrics"
        )

        result.append(dcc.Graph(figure=fig_metrics))

    except KeyError as e:
        result.append(html.H1(f"❌ Column Error: {e}"))
    except Exception as e:
        result.append(html.H1(f"❌ Error: {str(e)}"))

    return result

# =========================================================
# TEAM ANALYTICS
# =========================================================

def get_team_stats(team_data, team_name):
    """✓ FIX: Added docstring"""
    result = []

    try:
        total_wins = team_data.shape[0]

        result.append(html.H1(f"🏆 {team_name}"))
        result.append(html.H2(f"Total Wins : {total_wins}"))

        season_win = (
            team_data
            .groupby("season")
            .size()
            .reset_index(name="Wins")
        )

        fig_team = px.bar(
            season_win,
            x="season",
            y="Wins",
            color="Wins",
            title=f"{team_name} Season Wise Wins"
        )

        result.append(dcc.Graph(figure=fig_team))

        fig_trend = px.line(
            season_win,
            x="season",
            y="Wins",
            markers=True,
            title=f"{team_name} Winning Trend"
        )

        result.append(dcc.Graph(figure=fig_trend))

    except KeyError as e:
        result.append(html.H1(f"❌ Column Error: {e}"))
    except Exception as e:
        result.append(html.H1(f"❌ Error: {str(e)}"))

    return result

# =========================================================
# SMART SEARCH CALLBACK
# =========================================================

@app.callback(
    Output("search-output", "children"),
    Input("search-button", "n_clicks"),
    State("search-box", "value")
)
def search_data(n_clicks, value):
    """✓ FIX: Added proper checks for empty dataframes"""
    
    if value is None or value.strip() == "":
        return html.H1("Please Enter Something")

    value = value.strip().lower()
    result = []

    try:
        # =====================================================
        # BATTER SEARCH
        # =====================================================
        batter_data = delivery[
            delivery["batter"]
            .astype(str)
            .str.lower()
            .str.contains(value, na=False)
        ]

        # =====================================================
        # BOWLER SEARCH
        # =====================================================
        bowler_data = bowler_stats[
            bowler_stats["Bowler"]
            .astype(str)
            .str.lower()
            .str.contains(value, na=False)
        ]

        # =====================================================
        # TEAM SEARCH
        # =====================================================
        team_data = matches[
            matches["winner"]
            .astype(str)
            .str.lower()
            .str.contains(value, na=False)
        ]

        # =====================================================
        # TEAM ALIAS SUPPORT
        # =====================================================
        team_aliases = {
            "csk": "Chennai Super Kings",
            "mi": "Mumbai Indians",
            "rcb": "Royal Challengers Bengaluru",
            "kkr": "Kolkata Knight Riders",
            "srh": "Sunrisers Hyderabad",
            "dc": "Delhi Capitals",
            "pbks": "Punjab Kings",
            "rr": "Rajasthan Royals",
            "gt": "Gujarat Titans",
            "lsg": "Lucknow Super Giants"
        }

        if value in team_aliases:
            actual_team = team_aliases[value]
            team_data = matches[
                matches["winner"]
                .astype(str)
                .str.lower()
                .str.contains(actual_team.lower(), na=False)
            ]

        # =====================================================
        # ALL ROUNDER DETECTION
        # =====================================================
        is_batter = not batter_data.empty
        is_bowler = not bowler_data.empty

        # =====================================================
        # ✓ FIX: ALL ROUNDER with proper checks
        # =====================================================
        if is_batter and is_bowler and not batter_data.empty and not bowler_data.empty:
            player_name = batter_data["batter"].iloc[0]

            result.append(
                html.H1(
                    "⭐ ALL-ROUNDER PROFILE",
                    style={"color": "green"}
                )
            )

            result.extend(get_batter_stats(batter_data, player_name))
            result.extend(get_bowler_stats(bowler_data.iloc[0]))

            return result

        # =====================================================
        # ✓ FIX: BATTER ONLY with proper checks
        # =====================================================
        if is_batter and not batter_data.empty:
            player_name = batter_data["batter"].iloc[0]
            result.extend(get_batter_stats(batter_data, player_name))
            return result

        # =====================================================
        # ✓ FIX: BOWLER ONLY with proper checks
        # =====================================================
        if is_bowler and not bowler_data.empty:
            player_name = bowler_data["Bowler"].iloc[0]
            result.append(html.H1(f"🎯 {player_name}"))
            result.extend(get_bowler_stats(bowler_data.iloc[0]))
            return result

        # =====================================================
        # TEAM SEARCH
        # =====================================================
        if not team_data.empty:
            team_name = team_data["winner"].iloc[0]
            result.extend(get_team_stats(team_data, team_name))
            return result

        # =====================================================
        # NO RESULT
        # =====================================================
        return html.H1("❌ No Results Found")

    except KeyError as e:
        return html.H1(f"❌ Column not found: {e}")
    except Exception as e:
        return html.H1(f"❌ Error: {str(e)}")

# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":
    app.run(debug=False, port=8050)
