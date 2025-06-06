import pandas as pd
from ics import Calendar, Event
from ics.grammar.parse import ContentLine
from datetime import datetime
from dateutil.tz import gettz

data = pd.read_csv("data.csv", sep=";")
teams = pd.concat([data["Team 1"], data["Team 2"]]).unique()
with open("counter", "r") as file:
    counter = file.read()
print(counter)
for team in teams:
    games = data[(data["Team 1"] == team) | (data["Team 2"] == team)]
    c = Calendar()
    c.creator = "JensHeise/bowling-calendar"
    c.method = "PUBLISH"
    c.extra.append(ContentLine(name="NAME", value=team))
    c.extra.append(ContentLine(name="X-WR-CALNAME", value=team))
    c.extra.append(ContentLine(name="TIMEZONE-ID", value="Europe/Berlin"))
    c.extra.append(ContentLine(name="X-WR-TIMEZONE", value="Europe/Berlin"))
    c.extra.append(ContentLine(name="X-PUBLISHED-TTL", value="PT120M"))
    c.extra.append(ContentLine(name="REFRESH-INTERVAL",
                   value="PT120M", params={"VALUE": ["DURATION"]}))
    for game in games.iterrows():
        e = Event()
        e.created = datetime.now()
        if game[1]["Team 1"] == team:
            e.name = "🎳 " + game[1]["Team 1"] + " vs. " + \
                game[1]["Team 2"] + " | " + game[1]["Lanes"]
        else:
            e.name = "🎳 " + game[1]["Team 2"] + " vs. " + \
                game[1]["Team 1"] + " | " + game[1]["Lanes"]
        e.begin = datetime.strptime(
            game[1]["Date"] + " " + game[1]["Time"], "%d.%m.%Y %H:%M").replace(tzinfo=gettz(game[1]["Timezone"]))
        e.duration = {"hours": 2, "minutes": 30}
        e.location = game[1]["Alley"]
        e.uid = team + "-" + \
            e.begin.strftime("%Y%m%d%H%M%S") + "@bowling-calendar"
        e.extra.append(ContentLine(name="SERIES", value=counter))
        c.events.add(e)
    with open("calendars/" + team.replace(" ", "_") + ".ics", "w") as my_file:
        my_file.writelines(c)
with open("counter", "w") as file:
    file.write(str(int(counter) + 1))
