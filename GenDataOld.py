import pandas as pd
import datetime as dt
import random

columnnames = ["Acct","MTRTY_DT","TERM_DUR","DAY_PDUE_CNT","LAST_PMT_DT","LOAN_BAL_AMT","PRCPL_DUE_DT","ORIG_BAL_AMT","PMT_AMT","PDUE_AMT","LAST_TRXN_DT","ORIG_PROC_DT","DELQ_CNT","NUM_OF_PMTS_PDUE","PAYOF_AMT"]


def genrow():
    Acct = "{:0>7}".format(random.randint(0, 9999999))
    startyr = random.randint(1970, 2025)
    startmo = random.randint(1,12)
    endyr = random.randint(startyr+1, 2040)
    endmo = random.randint(1,12)
    day = random.randint(1, 28) #I don't know how paying on a day of the month that doesn't exist works
    #Hour/minute not required

    currentdate = dt.datetime.now()
    startdate = dt.datetime(startyr, startmo, day, 0, 0)
    enddate = dt.datetime(endyr, endmo, day, 0, 0)
    payday = dt.datetime(currentdate.year-1 if day>currentdate.day and currentdate.month==1 else currentdate.year, ((currentdate.month-2)%12)+1 if day>currentdate.day else currentdate.month, day)
    duration = 12*(endyr-startyr) + endmo-startmo

    #adjust it to the monthly paydate
    lastpaydatets = random.choice([0, 0, 0, 0, 0, random.randrange(startdate.timestamp()), int(currentdate.timestamp())]) #15% ish
    lastpaydate = dt.datetime.fromtimestamp(lastpaydatets)

    delqpayments = (currentdate - lastpaydate).days//30

    #Comsider putting the min/max price
    origbal = random.randint(1000000, 10000000)/100.0

    curbal = 0

    MTRTY_DT = enddate.strftime('%m/%d/%y %H:%M')
    TERM_DUR = duration
    DAY_PDUE_CNT = (currentdate-lastpaydate).days
    LAST_PMT_DATE = lastpaydate.strftime('%m/%d/%y %H:%M')
    ORIG_BAL_AMT = "{:0>8}".format(str(origbal))
    PRCPL_DUE_DT = dt.datetime.fromtimestamp(random.randint(startdate.timestamp(), enddate.timestamp())).strftime('%m/%d/%y %H:%M')
    PMT_AMT = round(origbal / duration, 2)
    LOAN_BAL_AMT = origbal-(PMT_AMT * ((lastpaydate-startdate).days//30))             #
    PDUE_AMT = PMT_AMT * delqpayments                                                                                                   #
    LAST_TRXN_DT = LAST_PMT_DATE
    ORIG_PROC_DT = startdate.strftime('%m/%d/%y %H:%M')
    DELQ_CNT = delqpayments                                                                                                             #
    NUM_OF_PAYMENTS_PDUE = delqpayments                                                                                                 #
    PAYOF_AMT = "{:0>8}".format(str(curbal))

    return [Acct, MTRTY_DT, TERM_DUR, DAY_PDUE_CNT, LAST_PMT_DATE, LOAN_BAL_AMT, PRCPL_DUE_DT, ORIG_BAL_AMT, PMT_AMT, PDUE_AMT, LAST_TRXN_DT, ORIG_PROC_DT, DELQ_CNT, NUM_OF_PAYMENTS_PDUE, PAYOF_AMT]


df = pd.DataFrame(columns=columnnames)

for i in range(200):
    df.loc[len(df)] = (genrow())

print(df)

df.to_csv(r"data.csv")


