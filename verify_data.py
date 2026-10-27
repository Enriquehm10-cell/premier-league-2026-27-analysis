
import pandas as pd
import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

# Load an independent data source
url = "https://www.football-data.co.uk/mmz4281/2627/E0.csv"

df = pd.read_csv(url)

print("PREMIER LEAGUE 2026/27")
print("Total records:", len(df))

print("\nFIRST 10 MATCHES:")
print(df[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]].head(10))

print("\nTEAMS:")
print(sorted(df["HomeTeam"].dropna().unique()))


# ------------------------------------
# COMPARE BOTH DATASETS
# ------------------------------------

original = pd.read_csv("premier_league_2026_27.csv")

# Standardize team names
original["home"] = original["home"].replace({
    "Man Utd": "Man United",
    "Spurs": "Tottenham"
})

original["away"] = original["away"].replace({
    "Man Utd": "Man United",
    "Spurs": "Tottenham"
})

# Standardize dates
original["date"] = pd.to_datetime(original["date"]).dt.date
df["Date"] = pd.to_datetime(
    df["Date"], dayfirst=True
).dt.date

# Compare matches
comparison = original.merge(
    df,
    left_on=["date", "home", "away"],
    right_on=["Date", "HomeTeam", "AwayTeam"],
    how="outer",
    indicator=True
)

matched = comparison[comparison["_merge"] == "both"]

different_scores = matched[
    (matched["ft_home"] != matched["FTHG"])
    | (matched["ft_away"] != matched["FTAG"])
]

print("\nDATA VERIFICATION RESULTS")
print("Matches found in both datasets:", len(matched))
print("Matches with different scores:", len(different_scores))
print("Matches without a match:", len(comparison) - len(matched))
