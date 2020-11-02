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

def set_list_title():   
   list_title = os.environ.get("FORMATTED_DATE")
   return list_title

def set_list_template():   
   list_template = os.environ.get("TRELLO_DAILYTEMPLATE_LIST")
   return list_template

def set_list_completed():   
   list_completed = os.environ.get("TRELLO_COMPLETED_LIST")
   return list_completed

# setup client
def setup_client():
   the_client = TrelloClient(
      api_key=my_api_key,
      token=my_api_token
   )

   return the_client

def list_all_boards(client):
    """
        get list of all boards to determine the ID
        for further functions
    """
    all_boards = client.list_boards()
    for counter, board in enumerate(all_boards):
        print(counter, board.id, board.name)

def set_board(the_client, the_board_str):
   all_boards = the_client.list_boards()
   for counter, board in enumerate(all_boards):
        print(counter, board.id, board.name)
        if the_board_str in board.name:
           print("Board found!  Setting Board ID to ", counter)
           the_board_id = counter

   the_board = all_boards[the_board_id]
   return the_board

def get_list(the_board, the_list_name):
   """
   for counter, this_list in enumerate(the_lists):
      print(counter, this_list.id, this_list.name, this_list.pos)
      if the_list_name in this_list.name:
         print("List found!  Setting List ID to ", counter)
         the_list = this_list[counter]
   """
   the_list = the_board.get_lists(the_list_name)
   
   return the_list

def get_list_position(the_list):
   the_list_pos = the_list.pos

   return the_list_pos
   
def set_list_position(the_list):
   the_list_position = get_list_position(the_list)
   print("Setting list position for List '", the_list.name, "' to [", the_list.pos, "]")
   return the_list_position

def find_values_from_key(key, json_object):
   print("Looking for key [" + key + "]")
   if isinstance(json_object, list):
      print("We have a list!")
      for list_element in json_object:
         yield from find_values_from_key(key, list_element)
   elif isinstance(json_object, dict):
      print("We have a dict!  Oh, behave...")
      if key in json_object:
         yield json_object[key]
      for dict_value in json_object.values():
         yield from find_values_from_key(key, dict_value)
   else:
      print("Um, not sure what type of object our json is...")

# Get Lists
def get_lists_url():
   lists_url=set_url("board/" + my_api_board + "/lists")

   query = {
      'key': my_api_key,
      'token': my_api_token
   }
      #'idBoard': my_api_board,
      #'lists': 'open'

   print(query)

   response = requests.request(
      "GET",
      lists_url,
      params=query
   )
   
   print(response.text)
   return response

def get_lists_api(the_board):
   print("Getting lists for '", the_board.name, "' board" )
   all_lists_on_board = the_board.list_lists()

   for list in all_lists_on_board:
      if not list.closed:
         print("List ID: ", list.id, ": name [", list.name, ']: pos ', list.pos)

   return all_lists_on_board 

def check_list_exists():
   trello_lists = get_lists_url()
   #trello_lists.dumps()

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
   #for keyval in trello_lists:
   for x in find_values_from_key('name', trello_lists): 
      # do something with x
      print("Checking if list is already created from list of list.")
   #   print("Current data is of type" + trello_listskey'][keyval]['name'])
      print("Content of current data is:")
      print(x)
      print(" ")
      print("Performing equality test now")
      if list_title == x:
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
#--

#if not check_list_exists():
#   new_list_id, new_list_pos = create_dow_list()
#   print("New List Titled [" + list_title + "] successfully created with ID " + str(new_list_id) + ".")

#import datetime
#(datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days

#do something
## Boardname begins with this phrase
## Allows for some renaming as long as this word says
board_name_left="Pinchhitter"
my_api_key, my_api_token, my_api_board = set_api_tokens()

the_client = setup_client()
my_board = set_board(the_client, board_name_left)
my_lists = get_lists_api(my_board)

list_all_boards(the_client)

#Get Completed List
the_completed_list_name = set_list_completed()
the_completed_list = get_list(my_board, the_completed_list_name)

list_title = set_list_title()
list_template = set_list_template()
list_pos = set_list_position(the_completed_list)


#list_pos = set_list_position()
#list_title = set_list_title()
#list_template = set_list_template()
