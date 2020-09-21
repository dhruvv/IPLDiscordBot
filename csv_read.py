import csv
import datetime

moDict = {"sep":9, "oct":10, "nov":11}




def map_month_to_date(mo: str):
    mo = mo.lower()
    return moDict[mo]


with open("sched.csv",mode="r") as file:
    scores = csv.reader(file, delimiter=",")
    matches = []
    for row in scores:
        day = int(row[0].split("-")[0])
        mo = int(list(map(map_month_to_date, [row[0].split("-")[1]]))[0])
        if row[1].split(":")[1][2:] == "PM":
            hr = int(row[1].split(":")[0]) + 12
        else:
            hr = row[1].split(":")[0]
        hr = int(hr)
        mi = int(row[1].split(":")[1][0:2])
        finalTime = datetime.datetime(2020,mo,day,hr,mi,0).timestamp()
        matches.append([finalTime,row[3].lower(),row[4].lower(),row[5].lower()])
print(matches)



            

        

