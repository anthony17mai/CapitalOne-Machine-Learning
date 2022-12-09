import pandas as pd
import datetime as dt

inp = input("Enter name of existing time series, or leave blank if there is none: ").strip()
if inp == "":
    outdf = pd.DataFrame(columns=["DATE", "DELQ_ACCTS"])
else:
    outdf = pd.read_csv(inp)

while True:
    inp = input("Input name of file, or q to quit: ")
    if inp == "q":
        break
    
    try:
        indf = pd.read_csv(inp)
    except:
        print("There was an issue with the file, please try again")
        continue
    
    indf['LastPaidDate'] = pd.to_datetime(indf['LastPaidDate'])
    for x in range(len(indf["LastPaidDate"])):
        indf["LastPaidDate"][x] = dt.date(indf["LastPaidDate"][x].year, indf["LastPaidDate"][x].month, 1)
    
    for i in indf["LastPaidDate"].unique():
        entrydate = i
        currdaydf = indf[indf["LastPaidDate"]==i]
        openacc = len(currdaydf[currdaydf["AccountState"]=="Opened"])
        paidacc = len(currdaydf[currdaydf["AccountState"]=="Paid"])
        defacc = len(currdaydf[currdaydf["AccountState"]=="Defaulting"])
        delqaccts = defacc/(openacc+paidacc+defacc)
        outdf.loc[len(outdf)] = ([entrydate, delqaccts])
    
    print("Current time series:")
    print(outdf)

outdf.to_csv(r"TS.csv")

    
