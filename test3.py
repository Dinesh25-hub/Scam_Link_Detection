'''from browser_history import get_history

outputs = get_history()

# his is a list of (datetime.datetime, url) tuples
his = outputs.histories'''

import csv
from browser_history.browsers import Firefox

f = Firefox()
outputs = f.fetch_history()

# his is a list of (datetime.datetime, url) tuples
his = outputs.histories
print(his)



'''# open the file in the write mode
ff = open('data.csv', 'w')
# create the csv writer
writer = csv.writer(ff)
# write a row to the csv file
writer.writerow(his)
# close the file
ff.close()'''
fieldnames = ['date', 'url_link']
with open('data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(fieldnames)

    # write multiple rows
    writer.writerows(his)
