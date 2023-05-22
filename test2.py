import browserhistory as bh
dict_obj = bh.get_browserhistory()
dict_obj.keys()
g=dict_obj(['chrome'])
#dict_obj['chrome'][1]
print()
#('https://mail.google.com', 'Mail', '2018-08-14 08:27:26')
# Write the data to csv files in the current working directory.
# safari_browserhistory.csv, chrome_browserhistory.csv, and firefox_browerhistory.csv.
bh.write_browserhistory_csv()
# Create csv files that contain broswer history
