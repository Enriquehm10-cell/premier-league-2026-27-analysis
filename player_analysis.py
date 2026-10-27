
import pandas as pd

# Load player statistics from FBref
# Read the downloaded FBref table
tables = pd.read_html("sportsref_download.xls")

df = tables[0]

print("PREMIER LEAGUE 2026/27 - PLAYER STATISTICS")

print("\nTOTAL PLAYERS/ROWS:")
print(len(df))

print("\nAVAILABLE COLUMNS:")
print(df.columns.tolist())

print("\nFIRST 10 ROWS:")
print(df.head(10).to_string(index=False))


# ------------------------------------
# CLEAN PLAYER DATA
# ------------------------------------

# Simplify column names
df.columns = [
    "Rank", "Player", "Nation", "Position",
    "Team", "Age", "Born", "Matches",
    "Starts", "Minutes", "90s", "Goals",
    "Assists", "Goals_Assists", "NonPenaltyGoals",
    "Penalties", "PenaltyAttempts",
    "YellowCards", "RedCards",
    "GoalsPer90", "AssistsPer90",
    "GoalsAssistsPer90", "NonPenaltyGoalsPer90",
    "NonPenaltyGoalsAssistsPer90", "MatchReports"
]

# Convert statistics to numbers
for col in ["Goals", "Assists", "Minutes"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove repeated header rows
df = df[df["Player"] != "Player"].copy()


# Fix player names with incorrect text encoding
def fix_name(name):
    if not isinstance(name, str):
        return name

    try:
        if "Ã" in name or "Â" in name:
            return name.encode("latin-1").decode("utf-8")
    except (UnicodeError, ValueError):
        pass

    return name

df["Player"] = df["Player"].apply(fix_name)

# ------------------------------------
# TOP 10 GOAL SCORERS
# ------------------------------------

top_scorers = df.sort_values(
    by=["Goals", "Assists", "Minutes"],
    ascending=[False, False, True]
).head(10)

print("\nTOP 10 GOAL SCORERS:")
print(
    top_scorers[
        ["Player", "Team", "Goals", "Assists", "Minutes"]
    ].to_string(index=False)
)

# Save results
top_scorers.to_csv("top_scorers.csv", index=False)


# ------------------------------------
# TOP SCORERS VISUALIZATION
# ------------------------------------

import matplotlib.pyplot as plt

# Reverse order so the top scorer appears first
chart_data = top_scorers.iloc[::-1]

fig, ax = plt.subplots(figsize=(12, 7))

# Highlight Haaland in gold
colors = [
    "#D4A64A" if player == "Erling Haaland" else "#24476A"
    for player in chart_data["Player"]
]

bars = ax.barh(
    chart_data["Player"],
    chart_data["Goals"],
    color=colors,
    height=0.65
)

# Add goal totals
for bar in bars:
    goals = bar.get_width()

    ax.text(
        goals + 0.15,
        bar.get_y() + bar.get_height() / 2,
        f"{int(goals)} goals",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

ax.set_title(
    "PREMIER LEAGUE | TOP GOAL SCORERS",
    fontsize=18,
    fontweight="bold",
    loc="left",
    pad=25
)

ax.text(
    0,
    1.02,
    "2026/27 Season | Top 10 Players",
    transform=ax.transAxes,
    fontsize=11,
    color="#666666"
)

ax.set_xlabel("Total Goals", fontsize=11)
ax.set_xlim(0, chart_data["Goals"].max() + 2)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(axis="both", length=0)
ax.xaxis.grid(True, linestyle="--", alpha=0.2)
ax.set_axisbelow(True)

fig.patch.set_facecolor("white")
ax.set_facecolor("white")

plt.tight_layout()

plt.savefig(
    "premier_league_top_scorers.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------
# GOALS PER 90 MINUTES ANALYSIS
# ------------------------------------

# Only players with at least 300 minutes played
qualified = df[df["Minutes"] >= 300].copy()

# Calculate goals per 90 minutes
qualified["GoalsPer90_Calculated"] = (
    qualified["Goals"] / qualified["Minutes"] * 90
)

# Rank the top 10 players
top_per90 = qualified.sort_values(
    by=["GoalsPer90_Calculated", "Goals"],
    ascending=False
).head(10)

print("\nTOP 10 PLAYERS - GOALS PER 90 MINUTES:")
print(
    top_per90[
        ["Player", "Team", "Goals", "Minutes", "GoalsPer90_Calculated"]
    ].round(2).to_string(index=False)
)

# Save the results
top_per90.to_csv("goals_per90.csv", index=False)


# ------------------------------------
# GOALS PER 90 VISUALIZATION
# ------------------------------------

chart_per90 = top_per90.iloc[::-1]

fig, ax = plt.subplots(figsize=(12, 7))

colors = [
    "#D4A64A" if player == "Erling Haaland" else "#24476A"
    for player in chart_per90["Player"]
]

bars = ax.barh(
    chart_per90["Player"],
    chart_per90["GoalsPer90_Calculated"],
    color=colors,
    height=0.65
)

for bar in bars:
    value = bar.get_width()

    ax.text(
        value + 0.02,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

ax.set_title(
    "PREMIER LEAGUE | GOALS PER 90 MINUTES",
    fontsize=18,
    fontweight="bold",
    loc="left",
    pad=25
)

ax.text(
    0,
    1.02,
    "2026/27 Season | Minimum 300 Minutes Played",
    transform=ax.transAxes,
    fontsize=11,
    color="#666666"
)

ax.set_xlabel("Goals per 90 Minutes")
ax.set_xlim(0, chart_per90["GoalsPer90_Calculated"].max() + 0.2)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(axis="both", length=0)
ax.xaxis.grid(True, linestyle="--", alpha=0.2)
ax.set_axisbelow(True)

fig.patch.set_facecolor("white")
ax.set_facecolor("white")

plt.tight_layout()

plt.savefig(
    "premier_league_goals_per90.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
