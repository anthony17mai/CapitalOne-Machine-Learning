# Loading the package
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import csv
import random
import dateutil
import datetime as dt
# Reading the data

dict = {"ACCT_ID", "RecordDate", "LoanStartDate", "LoanPrincipleDueDate", "LoanMaturityDate",
        "LoanOriginalAmount", "LoanBalance", "MonthlyPayment", "LastPaidDate","TotalPaymentsCompleted",
        "RunningMonthsPaid", "TotalMonthsDelinquent", "RunningMonthsDelinquent", "AccountState"}
df=pd.DataFrame(dict)
StartPastDate=dt.datetime(2010, 1, 1)
CurrentDate=dt.datetime(2021, 12, 30)
FutureDate=dt.datetime(2031, 12, 30)
MinLoan=10000
MaxLoan=100000
def DaysForMonth(x):
    Days31 = [1, 3, 5, 7, 8, 10, 12]
    if x==2:
        return random.randrange(1,29)
    elif x in Days31:
        return random.randrange(1,32)
    return random.randrange(1, 31)

for i in range (0,200):
    ACCT_ID="{:0>7}".format(random.randint(0, 9999999))
    startY = random.randrange(StartPastDate.year, CurrentDate.year)
    startM = random.randrange(1, 13)
    startD = DaysForMonth(startM)
    LoanStartDate = dt.datetime(startY, startM, startD)
    dueY = random.randrange(LoanStartDate.year+1, FutureDate.year)
    dueM = random.randrange(1, 13)
    dueD = DaysForMonth(dueM)
    LoanPrincipleDueDate = dt.datetime(dueY, dueM, dueD)
    LoanMaturityDate = dt.datetime(dueY+random.randrange(1, 6), dueM, dueD)
    LoanOriginalAmount=random.randint(MinLoan*100,MaxLoan*100)/100.0
    LoanBalance=LoanOriginalAmount
    delta=dateutil.relativedelta.relativedelta(LoanMaturityDate,LoanStartDate)
    MonthDiff=delta.months+(delta.years*12)
    MonthlyPayment=LoanOriginalAmount/MonthDiff
    LastPaidDate=LoanStartDate
    first={"ACCT_ID":ACCT_ID, "RecordDate":LoanStartDate, "LoanStartDate":LoanStartDate, "LoanPrincipleDueDate":LoanPrincipleDueDate, "LoanMaturityDate":LoanMaturityDate,
        "LoanOriginalAmount":'{0:.2f}'.format(LoanOriginalAmount), "LoanBalance":'{0:.2f}'.format(LoanBalance), "MonthlyPayment":'{0:.2f}'.format(MonthlyPayment), "LastPaidDate":LastPaidDate,"TotalPaymentsCompleted":0,
        "RunningMonthsPaid":0,"TotalMonthsDelinquent":0,"RunningMonthsDelinquent":0, "AccountState":"Opened"}
    #print(first)
    df=df.append(first,ignore_index=True)
    delta = dateutil.relativedelta.relativedelta(LoanStartDate, CurrentDate)
    MonthDiff = delta.months + (delta.years * 12)
    RecordDate=LoanStartDate + dateutil.relativedelta.relativedelta(months=1)
    TotalPaymentsCompleted=0
    RunningMonthsPaid=0
    TotalMonthsDelinquent=0
    RunningMonthsDelinquent=0
    quitLoop=0
    while RecordDate<CurrentDate and quitLoop==0:
        defaulted=random.randrange(0,101)
        if defaulted>=15:
            defaulted=0;
        else:
            defaulted=1;
        AccountState=""
        if defaulted==0:
            LoanBalance=LoanBalance-MonthlyPayment
            LastPaidDate=RecordDate
            TotalPaymentsCompleted = TotalPaymentsCompleted+1
            RunningMonthsPaid=RunningMonthsPaid+1
            RunningMonthsDelinquent = 0
            AccountState="Paid"
            if RecordDate == LoanMaturityDate or LoanBalance<=0:
                LoanBalance = 0
                AccountState="Completed"
                quitLoop=1
        else:
            RunningMonthsPaid = 0
            TotalMonthsDelinquent = TotalMonthsDelinquent+1
            RunningMonthsDelinquent = RunningMonthsDelinquent+1
            AccountState = "Defaulting"

        other = {"ACCT_ID": ACCT_ID, "RecordDate": RecordDate, "LoanStartDate": LoanStartDate,
               "LoanPrincipleDueDate": LoanPrincipleDueDate, "LoanMaturityDate": LoanMaturityDate,
               "LoanOriginalAmount": '{0:.2f}'.format(LoanOriginalAmount), "LoanBalance": '{0:.2f}'.format(LoanBalance),
               "MonthlyPayment": '{0:.2f}'.format(MonthlyPayment), "LastPaidDate": LastPaidDate,
               "TotalPaymentsCompleted": TotalPaymentsCompleted, "RunningMonthsPaid":RunningMonthsPaid,
               "TotalMonthsDelinquent": TotalMonthsDelinquent, "RunningMonthsDelinquent": RunningMonthsDelinquent, "AccountState": AccountState}
        #print(other)
        df = df.append(other, ignore_index=True)
        RecordDate = RecordDate + dateutil.relativedelta.relativedelta(months=1)
df.to_csv('data.csv', index=False)
#After completed deleted frist column and empty rows manually