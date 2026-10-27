# Premier League Performance Analysis
# Season 2026/2027
# Real football data

import pandas as pd

import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

# Load real Premier League data
url = (
    "https://raw.githubusercontent.com/"
    "oladeeayo/open-matchday/master/data/"
    "ENG_1_premier-league/results_2627.csv"
)

df = pd.read_csv(url)

# Display dataset information
print("PREMIER LEAGUE 2026/2027")
print("Matches recorded:", len(df))

# Display available columns
print("\nAVAILABLE COLUMNS:")
print(df.columns.tolist())

# Display first 10 matches
print("\nFIRST 10 MATCHES:")
print(df.head(10).to_string(index=False))

# Save a local copy
df.to_csv("premier_league_2026_27.csv", index=False)

print("\nDataset saved successfully!")


# ------------------------------------
# LEAGUE TABLE ANALYSIS
# ------------------------------------

teams = sorted(set(df["home"]) | set(df["away"]))

standings = []

for team in teams:

    home_games = df[df["home"] == team]
    away_games = df[df["away"] == team]

    wins = (
        (home_games["ft_home"] > home_games["ft_away"]).sum()
        + (away_games["ft_away"] > away_games["ft_home"]).sum()
    )

    draws = (
        (home_games["ft_home"] == home_games["ft_away"]).sum()
        + (away_games["ft_away"] == away_games["ft_home"]).sum()
    )

    losses = len(home_games) + len(away_games) - wins - draws

    goals_for = home_games["ft_home"].sum() + away_games["ft_away"].sum()
    goals_against = home_games["ft_away"].sum() + away_games["ft_home"].sum()

    points = wins * 3 + draws

    standings.append({
        "Team": team,
        "Played": len(home_games) + len(away_games),
        "Wins": wins,
        "Draws": draws,
        "Losses": losses,
        "GF": goals_for,
        "GA": goals_against,
        "GD": goals_for - goals_against,
        "Points": points
    })

table = pd.DataFrame(standings)

table = table.sort_values(
    by=["Points", "GD", "GF"],
    ascending=False
)

print("\nCALCULATED LEAGUE TABLE:")
print(table.to_string(index=False))

table.to_csv("league_table.csv", index=False)


# ------------------------------------
# DATA VISUALIZATION
# ------------------------------------


# ------------------------------------
# PROFESSIONAL DATA VISUALIZATION
# ------------------------------------

import matplotlib.pyplot as plt

# Select the top 10 teams
top_10 = table.head(10).iloc[::-1]

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

# Create horizontal bars
bars = ax.barh(
    top_10["Team"],
    top_10["Points"],
    color="#24476A",
    height=0.65
)


# Highlight Manchester City in gold
for bar, team in zip(bars, top_10["Team"]):
    if team == "Man City":
        bar.set_color("#D4A64A")

# Add points next to each bar
for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 0.3,
        bar.get_y() + bar.get_height() / 2,
        f"{int(width)} pts",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

# Title and subtitle
ax.set_title(
    "PREMIER LEAGUE | TEAM PERFORMANCE",
    fontsize=18,
    fontweight="bold",
    loc="left",
    pad=25
)

ax.text(
    0,
    1.02,
    "2026/27 Season | Top 10 Teams by Points",
    transform=ax.transAxes,
    fontsize=11,
    color="#666666"
)

# Remove unnecessary borders
for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(axis="both", length=0)
ax.set_xlabel("Total Points", fontsize=11)
ax.set_xlim(0, top_10["Points"].max() + 5)

# Subtle grid
ax.xaxis.grid(True, linestyle="--", alpha=0.2)
ax.set_axisbelow(True)

# White background
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

plt.tight_layout()

# Save professional chart
plt.savefig(
    "premier_league_professional_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
