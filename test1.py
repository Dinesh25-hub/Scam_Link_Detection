import browser_history

ss=""
while True:
    outputs = browser_history.get_history()

    #print(outputs.to_csv())
    ss=outputs.to_csv()
    


f1=open("static/data.txt","w")
f1.write(ss)
f1.close()


