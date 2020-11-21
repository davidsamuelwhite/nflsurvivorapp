url = "https://projects.fivethirtyeight.com/2020-nfl-predictions/games/"
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}

teams_class_string = "td text team"
probs_class_string = "td number chance"

num_byes = [0] * 10 + [4, 0, 2] + [0] * 4
num_teams = [32] * 17
num_teams = [x1 - x2 for (x1, x2) in zip(num_teams, num_byes)]

weeks = list(range(1, 18))

week_string = "week"
prob_string = "prob"
team_string = "team"

category = "Binary"

