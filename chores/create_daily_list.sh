#!/bin/sh

if [ $# -ne 2 ]
then
    echo "SYNTAX: $0 <<MIN_DAYS_OUT>> <<MAX_DAYS_OUT>>"
    echo "Where MIN_DAYS_OUT is Today + X Days to start the first daily list"
    echo "And MAX_DAYS_OUT is the Farthest Day Out for the last daily list"
    exit 1
fi

#. ./trello_keys

FROM_DAY=$1
TO_DAY=$2

the_day=${FROM_DAY}
for i in `echo "for (i=${FROM_DAY};i<=${TO_DAY};i++) i" | bc`
do
    echo "Creating list for $i days out"
    ./fancy_date.sh $i; . ./new_list.env; python3 create_weekly_lists.py
    #echo "List created"
done

echo "All done"
