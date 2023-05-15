import requests
from datetime import datetime
from bs4 import BeautifulSoup
import csv
import os
from time import sleep
from tqdm import tqdm

global count=0
def sendTG(to, client, tgid, key):
  global count
  #https://www.nationstates.net/cgi-bin/api.cgi?a=sendTG&client=abcd1234&to=testlandia&tgid=1234&key=abcdef1234567890
  url1 = "https://www.nationstates.net/cgi-bin/api.cgi"
  headers1 = {"User-Agent": user_agent}
  data1 = {
    "a": "sendTG",
    "client": client,
    "to": to,
    "tgid": tgid,
    "key": key,
  }
  print(to)
  response1 = requests.post(url1, headers=headers1, data=data1)
  print(response1.status_code)
  #print(url1, headers1, data1)
  print("sleeping for 30 secounds to be extra safe")
  #must be atleast 30!!!
  #for i in tqdm(range(30)):
  #  count=count+1
    sleep(30)


#client,tgid,key


def sendTGday(day, to):
  day = str(day)
  print(day)
  #adds the , MSG, client, tgid, key to the TG for the next step.
  print(f"sending day {day} TG to {to}")
  TG_data = {}
  with open("TGs.csv", "r") as csvfile:
    # Create a reader object using the csv module
    reader1 = csv.reader(csvfile)
    # Skip the header row
    next(reader1)
    # Loop through the rows in the CSV file
    for row1 in reader1:
      # input(row)
      # Get the key and value from the row
      key1 = row1[0]
      value1 = row1[1:]
      # Add the key-value pair to the dictionary
      TG_data[key1] = value1
  try:
    TG_data[day]
    #input(TG_data[day])
    sendTG(to, TG_data[day][0], TG_data[day][1], TG_data[day][2])
  except KeyError:

    print("no TG for today")
    pass


# Get user-agent from user input
user_agent = input("UserAgent: ")

# Make a request to the NationStates API using the user-agent
region="the north pacific"
response = requests.get(
  f"https://www.nationstates.net/cgi-bin/api.cgi?region={region.lower.()strip()}",
  headers={"User-Agent": user_agent},
)

if response.status_code == 200:
  soup = BeautifulSoup(response.content, "lxml")
  links = soup.find("nations")
listOfNations = links.text.split(":")

current_date = datetime.now()

# Get the day, month, and year from the current date
day = current_date.day
month = current_date.month
year = current_date.year

csv_data = {}
if not os.path.isfile("output.csv"):
  with open("output.csv", "w") as x:
    x.write("Name, days in TW, LR Day, LR Month, LR Year")
with open("output.csv", "r") as csvfile:
  # Create a reader object using the csv module
  reader = csv.reader(csvfile)

  # Skip the header row
  next(reader)

  # Loop through the rows in the CSV file
  for row in reader:
    # input(row)
    # Get the key and value from the row
    key = row[0]
    value = row[1:]
    # Add the key-value pair to the dictionary
    csv_data[key] = value

with open("output.csv", "w") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(["Name", "days in TW", "LR Day", "LR Month", "LR Year"])
  for each in listOfNations:
    if each in csv_data and (str(csv_data[each][1]) != str(day)
                             or str(csv_data[each][2]) != str(month)
                             or str(csv_data[each][3]) != str(year)):
      writer.writerow([each, int(csv_data[each][0]) + 1, day, month, year])
      sendTGday(str(int(csv_data[each][0]) + 1), each)
    elif each not in csv_data:
      writer.writerow([each, "0", day, month, year])
      sendTGday("0", each)
    else:
      writer.writerow([each, csv_data[each][0], day, month, year])

  # writer.writerow(["John", 25, "Male"])

csvfile.close()
print("Done making Database time to send TGs")
print("Sent TGS")
