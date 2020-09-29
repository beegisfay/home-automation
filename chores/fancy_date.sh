#!/bin/sh

# Make this a python function

if [ $# -ne 1 ]
then
  echo "An input for the number of days out you want is required:"
  echo "SYNTAX: $0 <DAYS_OUT>"
  exit 1
fi

DAYS_OUT=$1

DaySuffix() {
  case `date -d "+${DAYS_OUT} days"` in
    1|21|31) echo "st";;
    2|22)    echo "nd";;
    3|23)    echo "rd";;
    *)       echo "th";;
  esac
}
THE_SFX=`DaySuffix`
FORMATTED_DATE="`date -d "+${DAYS_OUT} days" "+%A, %B %-d${THE_SFX}"`"

echo "export DAYS_OUT=${DAYS_OUT}" >| new_list.env
echo "export FORMATTED_DATE=\"${FORMATTED_DATE}\"" >> new_list.env

