#! python3
# APSstats.py - Extracts statistics data from ASP NP14 log files.

import csv
import re
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta

datastat = []  # main stats data list of dictionaries
files = [x for x in os.listdir() if x.endswith('.log')]
num_regex = re.compile(r'(\d*),(\d*),(\d*)')
for f in files:
    with open(f, newline='') as csvfile:
        importdata = csv.reader(csvfile, delimiter=';')
        # 'dttimeeventcreated'  # date and time when log event was created
        # 'outflag'             # 1 for exit, 0 for entrance
        # 'carID'               # number of APS position (card number)
        # 'dttimeswipe'         # date and time card was swiped over card reader ???
        # 'vehiclesF0'          # number of occupied places on platform 0 at the time of event creation
        # 'vehiclesF1'          # same as vehiclesF0, but for platform 1
        # 'vehiclesF2'          # same as vehiclesF0, but for platform 2
        # 'dtinentranceclosed'  # ???
        # 'dttimeoutcommandstart'  # ???
        # 'dttimeoutexitopen'   # time when exit gate roller shuter opens for exit
        # 'dttimeoutexitclose'  # time when exit gate roller shutter closes after car left
        # 'user_timeout'        # calculated time between user check inside entrance box and entrance box door closes
        # 'user_timein'         # calculated time between exit door opens and user lefts exit box
        # 'user_parkout'        # calculated time between user calls car and exit box door opens

        for row in importdata:
            # Structure of row list items if outflag is 1 (index - meaning)
            # 0 - dttimeeventcreated
            # 1 - outflag
            # 2 - carID
            # 3 - dttimeswipe
            # 4 - vehicles
            # 5 - dtinentranceclosed
            # 6 - dttimeoutcommandstart
            # 7 - dttimeoutexitopen
            # 8 - dttimeoutexitclose
            #
            # Structure of row list items if outflag is 0 (index - meaning)
            # 0 - dttimeeventcreated
            # 1 - outflag
            # 2 - carID
            # 3 - dttimeswipe
            # 4 - vehicles
            # 5 - dttimeoutcommandstart
            # 6 - dttimeoutexitclose

            if row[1] == '1':  # exit event
                datastat.append({
                    'dttimeeventcreated': datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
                    'outflag': row[1],
                    'carID': row[2],
                    'dttimeswipe': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'vehiclesF0': int(num_regex.search(row[4]).group(1)),  # first number from comma-separated row[4]
                    'vehiclesF1': int(num_regex.search(row[4]).group(2)),  # second number from comma-separated row[4]
                    'vehiclesF2': int(num_regex.search(row[4]).group(3)),  # third number from comma-separated row[4]
                    'dtinentranceclosed': '',
                    'dttimeoutcommandstart': datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S'),
                    'dttimeoutexitopen': datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S'),
                    'dttimeoutexitclose': datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S'),
                    'user_timein': datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S'),
                    'user_parkout': datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'user_timeout': ''
                })
            else:  # entrance event if row[1] == '0'
                datastat.append({
                    'dttimeeventcreated': datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
                    'outflag': row[1],
                    'carID': row[2],
                    'dttimeswipe': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'vehiclesF0': '',  # TODO - extract first number from comma-separated row[4]
                    'vehiclesF1': '',  # TODO - extract second number from comma-separated row[4]
                    'vehiclesF2': '',  # TODO - extract third number from comma-separated row[4]
                    'dtinentranceclosed': '',
                    'dttimeoutcommandstart': datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'),
                    'dttimeoutexitopen': '',
                    'dttimeoutexitclose': datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S'),
                    'user_timeout': datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'user_timein': '',
                    'user_parkout': ''
                })
            # print('1 entry (event) appended to list')
            # print(datastat[-1])

num3 = len(files)
print('Import of data from', num3, 'source file(s)', ', '.join(files), 'done!')

if input('Should I check and remove duplicate entries? (y/n)').lower() == 'y':
    num1 = len(datastat)
    # datastat = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in datastat)]
    # remove duplicate records considering only certain keys (columns)
    i = 0
    while i < len(datastat)-1:
        j = i + 1
        while j < len(datastat):
            if (datastat[j]['outflag'] == datastat[i]['outflag'] and
                    datastat[j]['carID'] == datastat[i]['carID'] and
                    datastat[j]['dttimeswipe'] == datastat[i]['dttimeswipe']):
                del datastat[j]
            else:
                j += 1
        i += 1
    num2 = len(datastat)
    print('Total number of', num1, 'entries have been imported from log files. After removal of', num1 - num2,
          'duplicate(s) there are', num2, 'entries in database.')
else:
    num1 = len(datastat)
    print('Total number of', num1, 'entries have been imported from log files.')


def export_log():
    fname = input('Enter file name (extension ".data" will be added automatically"): ') + '.data'
    with open(fname, 'w') as fout:
        entry = []
        for row in datastat:
            if row['outflag'] == '1':  # exit event
                entry.append(
                    row['dttimeeventcreated'], #: datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
                    'outflag': row[1],
                    'carID': row[2],
                    'dttimeswipe': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'vehiclesF0': int(num_regex.search(row[4]).group(1)),  # first number from comma-separated row[4]
                    'vehiclesF1': int(num_regex.search(row[4]).group(2)),  # second number from comma-separated row[4]
                    'vehiclesF2': int(num_regex.search(row[4]).group(3)),  # third number from comma-separated row[4]
                    'dtinentranceclosed': '',
                    'dttimeoutcommandstart': datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S'),
                    'dttimeoutexitopen': datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S'),
                    'dttimeoutexitclose': datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S'),
                    'user_timein': datetime.strptime(row[8], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S'),
                    'user_parkout': datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'user_timeout': ''
                })
            else:  # entrance event if row[1] == '0'
                datastat.append({
                    'dttimeeventcreated': datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
                    'outflag': row[1],
                    'carID': row[2],
                    'dttimeswipe': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'vehiclesF0': '',  # TODO - extract first number from comma-separated row[4]
                    'vehiclesF1': '',  # TODO - extract second number from comma-separated row[4]
                    'vehiclesF2': '',  # TODO - extract third number from comma-separated row[4]
                    'dtinentranceclosed': '',
                    'dttimeoutcommandstart': datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'),
                    'dttimeoutexitopen': '',
                    'dttimeoutexitclose': datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S'),
                    'user_timeout': datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'),
                    'user_timein': '',
                    'user_parkout': ''
                })
            entry.append()
    print('Database of entries has been saved as file', fname, 'in current working directory.')


def list_by_user(userid, since=datetime(2015, 1, 1), till=datetime.now(), data=datastat):
    """Return a list of entries from given list of dictionaries for selected user (card ID) and within selected time period.
    Default time period is between 1.1.2015 and today."""
    result = []
    for item in data:
        # print(item)
        if (item['carID'] == userid) and (since <= item['dttimeeventcreated'] <= till):
            result.append(item)
    return result


def date_range(start, end):
    r = (end - start).days + 1
    datelist = [start + timedelta(days=i) for i in range(r)]
    return datelist


def plot_events_for_period(since=date(2015, 1, 1), till=date.today(), data=datastat):
    """Creates (bar) chart showing number of operations per day during selected time period.
    Default time period is between 1.1.2015 and today."""
    dates = date_range(since, till)  # list of all days in range - for axis x
    eventsnum = [0] * len(dates)  # list with number of events for each day in range - for axis y
    for item in data:
        if since <= datetime.date(item['dttimeeventcreated']) <= till:
            eventsnum[(datetime.date(item['dttimeeventcreated']) - since).days] += 1
    # print(dates)
    # print(eventsnum)
    plt.bar(dates, eventsnum, label='Number of operations per day')
    plt.xlabel('dates')
    plt.ylabel('no. of operations')
    plt.title('No. of operations per day\nbetween ' + since.strftime('%d.%m.%y') + ' and ' + till.strftime('%d.%m.%y'))
    plt.legend()
    plt.xticks(rotation=90)
    plt.show()
    return len(dates)


def plot_occupancy_for_period(since=date(2015, 1, 1), till=date.today(), data=datastat):
    """Creates chart showing max number of occupied parking places per day during selected time period.
    Default time period is between 1.1.2015 and today."""
    dates = date_range(since, till)  # list of all days in range - for axis x
    occup_f0 = [0] * len(dates)  # list with number of occupied places in F0 layer for each day in range - for axis y
    occup_f1 = [0] * len(dates)  # list with number of occupied places in F1 layer for each day in range - for axis y
    occup_f2 = [0] * len(dates)  # list with number of occupied places in F2 layer for each day in range - for axis y
    for item in data:
        if since <= datetime.date(item['dttimeeventcreated']) <= till:
            if occup_f0[(datetime.date(item['dttimeeventcreated']) - since).days] < item['vehiclesF0']:
                occup_f0[(datetime.date(item['dttimeeventcreated']) - since).days] = item['vehiclesF0']
            if occup_f1[(datetime.date(item['dttimeeventcreated']) - since).days] < item['vehiclesF1']:
                occup_f1[(datetime.date(item['dttimeeventcreated']) - since).days] = item['vehiclesF1']
            if occup_f2[(datetime.date(item['dttimeeventcreated']) - since).days] < item['vehiclesF2']:
                occup_f2[(datetime.date(item['dttimeeventcreated']) - since).days] = item['vehiclesF2']
    occup_tot = [occup_f0[i]+occup_f1[i]+occup_f2[i] for i in range(len(occup_f0))]  # list with number of occupied places total for each day in range - for axis y
    # print(dates)
    # print(eventsnum)
    plt.bar(dates, occup_tot, label='Number of operations per day')
    plt.xlabel('dates')
    plt.ylabel('no. of operations')
    plt.title('No. of operations per day\nbetween ' + since.strftime('%d.%m.%y') + ' and ' + till.strftime('%d.%m.%y'))
    plt.legend()
    plt.show()
    return len(dates)


print('What do you want to do?')
print('1 = plot graph with number of parking operations for time period')
print('2 = print list of all operations of selected user during time period')
print('export = save database of entries as log file')
print('q = quit program')

do = ''
while do.lower() != 'q':
    do = input('Type menu item number and hit Enter: ')
    if do == '1':
        plot_events_for_period(date(2016, 5, 26), date(2016, 6, 2))
    elif do == '2':
        id_ = input('Enter user (car) ID number: ')
        print('List of operations by user ID:', id_)
        lst = sorted(list_by_user(id_), key=lambda k: k['dttimeswipe'])  # returns sorted list of dicts
        for item in lst:
            print('\t', item['dttimeswipe'])
    elif do == 'export':
        export_log()
print('Thank you for using APS stats, bye bye!')
