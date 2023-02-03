import sys
import csv
from datetime import datetime

# Get the passed argument
points_to_spend = int(sys.argv[1])

# Code that processes the CSV file and obtains the data
with open('transactions.csv', "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)
header = reader.fieldnames
date_column_index = header.index('timestamp')
sorted_data = []

# Code to sort the rows based on timestamp
for row in data:
    try:
        datetime_value = datetime.strptime(row[header[2]], "%Y-%m-%dT%H:%M:%SZ")
        sorted_data.append((datetime_value, row))
    except ValueError as e:
        print(f"Error parsing datetime string '{row[header[2]]}': {e}")
sorted_data.sort(key=lambda x: x[0])
sorted_data = [row[1] for row in sorted_data]

# Logic to do the calculations
# The idea is to reduce points one by one as we have already sorted the data.
for i in sorted_data:
    available_points = int(i['points'])
    if points_to_spend >= available_points:
        points_to_spend = points_to_spend - available_points
        i['points'] = 0
    elif points_to_spend < available_points:
        i['points'] = available_points - points_to_spend
        points_to_spend = 0
        break

# Return value is calculated.
# We need to return total points remaining for each payer, thus using dictionary we can calculate total points
dt = {}
for i in sorted_data:
    if i['payer'] in dt.keys():
        dt[i['payer']] = dt[i['payer']] + int(i['points'])
    else:
        dt.update({i['payer']: int(i['points'])})
if points_to_spend > 0:
    print("Insufficient points")
print(dt)
