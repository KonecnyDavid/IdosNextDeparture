import requests
import re
import json
from bs4 import BeautifulSoup

from_stop = "Jungmannova"

lines = {
    "1": ("reckovice", "ecerova"),
    "6": ("kralovo pole, nadrazi", "stary liskovec")
}

week_start = 17


def create_url(line_n, end_stop, day):
    return "https://idos.idnes.cz/brno/zjr/vysledky/?date={}.02.2020&l=Tram%20{}&f={}&t={}&ttn=IDSJMK".format(day, line_n, from_stop, end_stop)


def parse(content):
    print("Parsing previous request")
    soup = BeautifulSoup(content, 'html.parser')
    result = soup.find("table", class_="times")
    body = result.find("tbody")
    rows = body.findAll("tr")

    res = {}

    for idx, row in enumerate(rows):
        tds = row.findAll("td")
        times = list(
            filter(
                lambda el: len(el) == 2,
                re.findall(r"[0-9]+", str(tds[1].prettify().encode("utf-8")))
                )
            )
        res[(idx + 3) % 24] = times

    print("Success")

    return res


def parse_row(row):
    pass


res = {}


for line_n, destinations in lines.items():
    destinations_res = {}
    for destination in destinations:
        days_res = {}
        for day in range(week_start, week_start + 7):
            url = create_url(line_n, destination, day)
            print(
                "Making request to: Line {} | {} -> {} | Day {}"
                .format(line_n, from_stop, destination, day)
                )

            response = requests.get(url)
            data = parse(response.content.decode('utf-8', 'ignore'))
            days_res[day - week_start] = data

        destinations_res[destination] = days_res
    res[line_n] = destinations_res


json_data = json.dumps(res)

with open("./data.json", "w") as file:
    file.write(json_data)
