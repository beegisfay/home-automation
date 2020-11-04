# This code sample uses the 'requests' library:
# http://docs.python-requests.org
#!/usr/bin/env python3

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests, os, json
from trello import TrelloClient

#init global scope variables

def set_url(url_level):
   the_url = "https://api.trello.com/1/" + url_level
   return the_url

def set_api_tokens():
   the_api_key = os.popen("lpass show TRELLO_KEY --format=""%fv"" | tail -1").read()
   the_api_token = os.popen("lpass show TRELLO_TOKEN --format=""%fv"" | tail -1").read()
   the_api_board = os.popen("lpass show TRELLO_BOARD --format=""%fv"" | tail -1").read()

   return the_api_key, the_api_token, the_api_board
   
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
