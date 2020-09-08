# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import os

url = "https://api.trello.com/1/lists"
board_pos = int(os.environ.get("DAYS_OUT")) + 2

query = {
   'key': os.environ.get("TRELLO_KEY"),
   'token': os.environ.get("TRELLO_TOKEN"),
   'name': os.environ.get("FORMATTED_DATE"),
   'idBoard': os.environ.get("TRELLO_BOARD"),
   'idListSource': os.environ.get("TRELLO_DAILYTEMPLATE_LIST"),
   'pos': board_pos
}

print(query)

response = requests.request(
   "POST",
   url,
   params=query
)

print(response.text)
