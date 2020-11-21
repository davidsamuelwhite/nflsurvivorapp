import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from pulp import LpVariable, LpProblem, lpSum, LpMaximize

from config import *


def download_probabilities():
    request = requests.get(url, headers=header).text
    soup = bs(request)
    return soup


def organize_soup(soup, weeks_completed):
    teams = list()
    for team in soup.findAll("td", class_=teams_class_string):
        teams.append(team.text.strip())

    all_weeks = list()
    for week, team in zip(weeks, num_teams[weeks_completed:]):
        all_weeks.extend([week] * team)

    chances = list()
    for chance in soup.findAll("td", class_=probs_class_string):
        chances.append(chance.text.strip().replace("%", ""))
    chances = chances[:len(all_weeks)]

    df = pd.DataFrame
    {team_string: teams, prob_string: chances, week_string: all_weeks}
    return df


def clean_df(df):
    df[week_string] = pd.to_numeric(df[week_string])
    df = df.pivot(index=team_string, columns=week_string, values=prob_string).fillna(-3000)
    return df


def update_df(df, selected_teams):
    return df[~df.index.isin([selected_teams])]


def solve_linear_program(df):
    teams_list = df.index.tolist()
    weeks_list = df.columns.tolist()
    decisions = LpVariable.dicts("",
                                 ((i, j) for i in teams_list for j in weeks_list),
                                 cat=category)
    problem = LpProblem("", LpMaximize)
    for team in teams_list:
        problem += lpSum(decisions[(team, week)] for week in weeks_list) <= 1
    for week in weeks_list:
        problem += lpSum(decisions[(team, week)] for team in teams_list) == 1
    problem += lpSum(
        [float(df.loc[team, week]) * decisions[(team, week)] for team in teams_list for week in weeks_list])
    problem.solve()
    return teams_list, weeks_list, decisions


def output_results(df, teams_list, weeks_list, decisions):
    lineup = []
    for week in weeks_list:
        for team in teams_list:
            if decisions[(team, week)].varValue == 1.0:
                lineup.append([team, week, df.loc[team, week]])
    return lineup
