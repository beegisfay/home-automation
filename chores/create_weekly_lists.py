#!/usr/bin/env python3
verbose=True

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests, json, subprocess, os, argparse
from trello import TrelloClient

#init global scope variables

def parse_args():
   parser = argparse.ArgumentParser(description='Manage Trello Board')
   parser.add_argument('-f', 
      '--from_days_out', 
      metavar='from_days_out',
      default='0',
      help='Beginning of range of days from today to build new daily lists')
   parser.add_argument('-t', 
      '--to_days_out', 
      metavar='to_days_out',
      default='0',
      help='Ending of range of days from today to build new daily lists')
   parser.add_argument('-a', 
      '--auto_assign', 
      metavar='auto_assign',
      default='N',
      help='Auto-assign daily/weekly/quarterly chores based on defined algorithm')
   parser.add_argument('-d', 
      '--day_of_week_chore_autoadd', 
      metavar='day_of_week_chore_autoadd',
      default='N',
      help='Automatically add chores for each day of the week using defined logic')
   parser.add_argument('-w', 
      '--weekly_chore_autoadd', 
      metavar='weekly_chore_autoadd',
      default='N',
      help='Automatically add weekly chores using defined logic')
   args = parser.parse_args()
   return args

def set_url(url_level):
   the_url = "https://api.trello.com/1/" + url_level
   return the_url

def get_api_secret(the_api_key):
   the_command='lpass show '+the_api_key+' --format="%fv" | tail -1'
   print("Getting secret from last pass using following command:")
   print("[" + the_command + "]")
   the_api_secret = os.popen(the_command).read().strip()

   return the_api_secret
   
def set_api_tokens():
   the_api_key = get_api_secret("TRELLO_KEY")
   print("The API Key from LP is [" + the_api_key + "]")
   the_api_token = get_api_secret("TRELLO_TOKEN")
   the_api_board = get_api_secret("TRELLO_BOARD")

   return the_api_key, the_api_token, the_api_board

def set_list_title():   
   list_title = os.environ.get("FORMATTED_DATE")
   return list_title

def set_list_template():   
   list_template = get_api_secret("TRELLO_DAILYTEMPLATE_LIST")
   return list_template

def set_list_completed():   
   list_completed = get_api_secret("TRELLO_COMPLETED_LIST")
   print("Set list_completed to [" + list_completed + "]")
   return list_completed

# setup client
def setup_client(the_api_key, the_api_token):
   the_client = TrelloClient(
      api_key=the_api_key,
      token=the_api_token
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

def get_list(the_lists, the_list_name):
   for counter, this_list in enumerate(the_lists):
      print(counter, this_list.id, this_list.name, this_list.pos)
      if the_list_name in this_list.name:
         print("List found!  Setting List ID to ", counter)
         the_list = this_list
      
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
# def get_lists_url(the_api_key, the_api_token, the_api_board):
#    lists_url=set_url("board/" + the_api_board + "/lists")

#    query = {
#       'key': the_api_key,
#       'token': the_api_token
#    }
#       #'idBoard': my_api_board,
#       #'lists': 'open'

#    print(query)

#    response = requests.request(
#       "GET",
#       lists_url,
#       params=query
#    )
   
#    print(response.text)
#    return response

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
### Convert to use API
###
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

# Make these global for now
# They will become part of a class in the future
#my_api_key, my_api_token, my_api_board = None

def setup_trello():
   board_name_left="Pinchhitter"

   my_api_key, my_api_token, my_api_board = set_api_tokens()

   the_client = setup_client(my_api_key, my_api_token)
   my_board = set_board(the_client, board_name_left)
   my_lists = get_lists_api(my_board)

#do something
def main():
   args = parse_args()

   setup_trello()

   #list_all_boards(the_client)

   #Get Completed List
   #the_completed_list_name = set_list_completed()
   #the_completed_list = get_list(my_lists, the_completed_list_name)

   #list_title = set_list_title()
   #list_template = set_list_template()
   #list_pos = set_list_position(the_completed_list)

   #list_pos = set_list_position()
   #list_title = set_list_title()
   #list_template = set_list_template()

if __name__ == '__main__':
   main()