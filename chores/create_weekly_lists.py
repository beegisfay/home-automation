# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests, os, json
from trello import TrelloClient

def set_url(url_level):
   the_url = "https://api.trello.com/1/" + url_level
   return the_url

def set_list_position():
   list_pos = int(os.environ.get("DAYS_OUT")) + 2

   return list_pos

def set_api_tokens():
   the_api_key = os.environ.get("TRELLO_KEY")
   the_api_token = os.environ.get("TRELLO_TOKEN")
   the_api_board = os.environ.get("TRELLO_BOARD")

   return the_api_key, the_api_token, the_api_board

def set_list_title():   
   list_title = os.environ.get("FORMATTED_DATE")
   return list_title

def set_list_template():   
   list_template = os.environ.get("TRELLO_DAILYTEMPLATE_LIST")
   return list_template

#init global scope variables
list_pos = set_list_position()
my_api_key, my_api_token, my_api_board = set_api_tokens()
list_title = set_list_title()
list_template = set_list_template()

# Get Lists
def get_lists():
   lists_url=set_url("board/" + my_api_board)

   query = {
      'key': my_api_key,
      'token': my_api_token,
      #'idBoard': my_api_board,
      'lists': 'open'
   }

   print(query)

   response = requests.request(
      "GET",
      lists_url,
      params=query
   )
   
   print(response.text)
   return response

def check_list_exists():
   trello_lists = get_lists()
   the_lists = json.loads(trello_lists.text)

   print("Checking if new list [" + list_title + "] exists before creating.")
   print(" ")
   print(trello_lists)
   print(" ")
   print("*****************************************************************************")
   list_found = False

   # Loop through all lists to see if matching name is found
   # This is inefficient as there is no rhyme nor reason to how the search order is performed
   # It also does not stop upon a match
   # Assumption is number of lists is very small (i.e. 10) and does not include archived lists
   for keyval in trello_lists:
      print("Checking if list is already created from list of list.")
      print("Current data is of type" + str(type(keyval)))
      print("Content of current data is:")
      print(keyval)
      print(" ")
      print("Performing equality test now")
      if list_title == keyval:
         print("List [" + list_title + "] already exists, not creating duplicate.")
         list_found = True

   return list_found

# Create new list for a day of the week
def create_dow_list():
   print("List [" + list_title + "] not found so proceeding with creation.") 

   lists_url=set_url("lists")

   query = {
      'key': my_api_key,
      'token': my_api_token,
      'name': list_title,
      'idBoard': my_api_board,
      'idListSource': list_template,
      'pos': list_pos
   }

   print(query)

   response = requests.request(
      "POST",
      lists_url,
      params=query
   )
   new_list_id = response.json()["id"]
   new_list_pos = response.json()["pos"]

   print(response.text)
   return new_list_id, new_list_pos

if not check_list_exists():
   new_list_id, new_list_pos = create_dow_list()
   print("New List Titled [" + list_title + "] successfully created with ID " + str(new_list_id) + ".")

#import datetime
#(datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days