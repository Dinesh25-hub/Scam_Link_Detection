from browser_history.browsers import Chrome

f = Chrome()
outputs = f.fetch_history()

#outputs.write_browserhistory_csv()

#f.write_browserhistory_csv()

#his = outputs.histories

outputs = f.fetch_history()
outputs.histories.write_browserhistory_csv()
