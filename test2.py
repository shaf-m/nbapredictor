from nba_api.stats.static import teams
# get_teams returns a list of 30 dictionaries, each an NBA team.
nba_teams = teams.get_teams()
print('Number of teams fetched: {}'.format(len(nba_teams)))

for team in nba_teams:
    print(f"The {team['full_name']} also go by {team['abbreviation']}"
          f" and they were founded in the year {team['year_founded']}.")
