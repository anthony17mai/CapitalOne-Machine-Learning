import pandas as pd
import datetime as dt
import random

columnnames = ["DATE", "DELQ_ACCTS"]

movingdate = dt.date(2010, 1, 1)
delqaccts = 30
movingvalue = 0
def gennext(cur_delq, movval):
    if delqaccts <= 5:
        movval = random.randint(0, 3)
    elif delqaccts < 30:
        movval += random.randint(-1, 2)
    elif delqaccts >= 30:
        movval += random.randint(-2, 1)

    cur_delq += movingvalue

    return max(cur_delq, 5), movval

df = pd.DataFrame(columns=columnnames)

for i in range(300):
    df.loc[len(df)] = (pd.to_datetime(movingdate), delqaccts/100)
    try:
        try:
            movingdate = dt.date(movingdate.year, movingdate.month, movingdate.day+1)
        except:
            movingdate = dt.date(movingdate.year, movingdate.month+1, 1)
    except:
        movingdate = dt.date(movingdate.year+1, 1, 1)
    delqaccts, movingvalue = gennext(delqaccts, movingvalue)

print(df)

df.to_csv(r"TS.csv")

