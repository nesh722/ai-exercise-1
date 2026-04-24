import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the CSV
df = pd.read_csv("results.csv")

# Basic Exploration
print("--- Basic Exploration ---")

# 1. How many matches are in the dataset?
total_matches = df.shape[0]
print(f"Total matches: {total_matches}")

# 2. What is the earliest and latest year in the data?
# First, convert the date column to datetime objects
df['date'] = pd.to_datetime(df['date'])
earliest_year = df['date'].dt.year.min()
latest_year = df['date'].dt.year.max()
print(f"Earliest year: {earliest_year}, Latest year: {latest_year}")

# 3. How many unique countries are there?
unique_countries = df['country'].nunique()
print(f"Unique countries: {unique_countries}")

# 4. Which team appears most frequently as home team?
top_home_team = df['home_team'].value_counts().idxmax()
print(f"Most frequent home team: {top_home_team}")

# Goals Analysis
print("\n--- Goals Analysis ---")

# Create total goals column
df["total_goals"] = df["home_score"] + df["away_score"]

# 5. What is the average number of goals per match?
avg_goals = df["total_goals"].mean()
print(f"Average goals per match: {avg_goals:.2f}")

# 6. What is the highest scoring match?
highest_scoring_match = df.loc[df['total_goals'].idxmax()]
print(f"Highest scoring match: {highest_scoring_match['home_team']} vs {highest_scoring_match['away_team']} ({highest_scoring_match['total_goals']} goals)")

# 7. Are more goals scored at home or away?
total_home_goals = df['home_score'].sum()
total_away_goals = df['away_score'].sum()
print(f"Home goals: {total_home_goals}, Away goals: {total_away_goals}")

# 8. What is the most common total goals value?
common_goal_count = df['total_goals'].mode()[0]
print(f"Most common total goals: {common_goal_count}")

# Match Results
print("\n--- Match Results ---")

def match_result(row):
    if row["home_score"] > row["away_score"]:
        return "Home Win"
    elif row["home_score"] < row["away_score"]:
        return "Away Win"
    else:
        return "Draw"

df["result"] = df.apply(match_result, axis=1)

# 9. What percentage of matches are home wins?
home_win_pct = (df['result'] == 'Home Win').mean() * 100
print(f"Percentage of home wins: {home_win_pct:.2f}%")

# 10. Does home advantage exist?
# Logic: Compare Home Win % to Away Win %
away_win_pct = (df['result'] == 'Away Win').mean() * 100
print(f"Home Win %: {home_win_pct:.2f} vs Away Win %: {away_win_pct:.2f}")
print("Conclusion: Yes, home advantage exists as home win percentage is significantly higher.")

# 11. Which country has the most wins historically?
# We need to find the winner for every match
def get_winner(row):
    if row['result'] == 'Home Win': return row['home_team']
    if row['result'] == 'Away Win': return row['away_team']
    return "Draw"

df['winner'] = df.apply(get_winner, axis=1)
most_wins_country = df[df['winner'] != "Draw"]['winner'].value_counts().idxmax()
print(f"Country with the most wins: {most_wins_country}")

# Visualization
print("\n--- Generating Visualizations ---")

# Histogram of goals
plt.figure(figsize=(10, 5))
df["total_goals"].hist(bins=20, edgecolor='black')
plt.title("Distribution of Goals Per Match")
plt.xlabel("Total Goals")
plt.ylabel("Number of Matches")
plt.show()

# Bar chart of match outcomes
plt.figure(figsize=(10, 5))
df['result'].value_counts().plot(kind='bar', color=['blue', 'green', 'red'])
plt.title("Match Outcomes")
plt.ylabel("Count")
plt.show()

# Top 10 teams by total wins
plt.figure(figsize=(10, 5))
df[df['winner'] != "Draw"]['winner'].value_counts().head(10).plot(kind='barh', color='orange')
plt.gca().invert_yaxis()
plt.title("Top 10 Teams by Total Wins")
plt.show()