#! python3
# APSstats.py - Extracts statistics data from ASP NP14 log files.

import csv
from datetime import datetime, date

filePath = 'testlog.csv'
with open(filePath, newline='') as csvfile:
    importdata = csv.reader(csvfile, delimiter=';')
    datastat = []  # main stats data list of dictionaries
    # 'dttimeeventcreated'  # date and time when log event was created
    # 'outflag'             # 1 for exit, 0 for entrance
    # 'carID'               # number of APS position (card number)
    # 'dttimeswipe'         # date and time card was swiped over card reader ???
    # 'vehiclesF0'          # number of occupied occupied positions on platform 0 at the time of event creation
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
                'vehiclesF0': '',  # TODO - extract first number from comma-separated row[4]
                'vehiclesF1': '',  # TODO - extract second number from comma-separated row[4]
                'vehiclesF2': '',  # TODO - extract third number from comma-separated row[4]
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
        print('1 entry (event) appended to list')
        print(datastat[-1])
print('Import of data from csv source file', filePath, 'done!')
print('Total of', len(datastat), ' entries (rows) have been imported.')


def list_by_user(id, since=datetime(2015, 1, 1), till=datetime.now(), data=datastat):
    """Return a list of entries from given list of dictionaries for selected user (card ID) and within selected time period.
    Default time period is between 1.1.2015 and today."""
    result = []
    for item in data:
        # print(item)
        if (item['carID'] == id) and (since <= item['dttimeeventcreated'] <= till):
            result.append(item)
    return result

id = input('Enter user (car) ID number: ')
print('List of operations by user ID:', id)
print(list_by_user(id))
