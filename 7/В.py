import requests
import xml.etree.ElementTree as ET
import statistics
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

currency = config["currency"]
start_date = config["start"]
end_date = config["end"]

url = f"https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.{currency}.EUR.SP00.A?startPeriod={start_date}&endPeriod={end_date}"
headers = {"Accept": "application/xml"}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    raise Exception(f"Помилка запиту: {response.status_code}")

root = ET.fromstring(response.content)
ns = {"ns": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"}

rates = []
for series in root.findall(".//ns:Series", ns):
    for obs in series.findall("ns:Obs", ns):
        date = obs.find("ns:ObsDimension", ns).attrib["value"]
        rate = float(obs.find("ns:ObsValue", ns).attrib["value"])
        rates.append((date, rate))

if not rates:
    raise Exception("Дані не знайдено.")

rates.sort(key=lambda x: x[0])

values = [r[1] for r in rates]
average_rate = sum(values) / len(values)
min_date, min_rate = min(rates, key=lambda x: x[1])
max_date, max_rate = max(rates, key=lambda x: x[1])
std_dev = statistics.stdev(values)

print(f"Exchange rate of {currency} to EUR from {start_date} to {end_date}:")
print(f"Average rate: {average_rate:.4f}")
print(f"Min rate: {min_rate:.4f} (date: {min_date})")
print(f"Max rate: {max_rate:.4f} (date: {max_date})")
print(f"Standard deviation: {std_dev:.4f}")
