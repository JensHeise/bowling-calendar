import pandas as pd
from ics import Calendar, Event

data = pd.read_csv("data.csv", sep=";")
teams = pd.concat([data["Team 1"], data["Team 2"]]).unique()
for team in teams:
    games = data[(data["Team 1"] == team) | (data["Team 2"] == team)]
    c = Calendar()
    for game in games.iterrows():
        e = Event()
        if game[1]["Team 1"] == team:
            e.name = game[1]["Team 1"] + " vs. " + game[1]["Team 2"] + " | " + game[1]["Lanes"]
        else:
            e.name = game[1]["Team 2"] + " vs. " + game[1]["Team 1"] + " | " + game[1]["Lanes"]
        e.begin = game[1]["Date"] + "T" + game[1]["Time"] + game[1]["Timezone"]
        e.duration = {"hours": 2}
        e.location = game[1]["Alley"]
        e.geo = (game[1]["Latitude"], game[1]["Longitude"])
        c.events.add(e)
    with open("calendars/" + team + ".ics", "w") as my_file:
        my_file.writelines(c.serialize_iter())