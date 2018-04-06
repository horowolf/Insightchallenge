from datetime import datetime, time, timedelta
import sys
import csv


if len(sys.argv) != 4 :
    print("The input should be: python program.py input-log.csv input-inactivity_period.txt output-sessionization.txt")

f = open(sys.argv[2], "r")
fd = f.read()
inactivityPeriod = int(fd)
f.closed

f = open(sys.argv[3], "w")

csvf = open(sys.argv[1], mode = "r")
reader = csv.reader(csvf)

ipStartDic = dict() # (key = ip : value = (dt-str, order))
ipLastDic = dict()  # (key = ip : value = dt-str)
ipRequestCount = dict()
# pre-printout dict: (key = datetime with microsecond in string for sorting : printout-str)
prePrintoutDic = dict()
removeList = list()

currentDatetime = ""

def makePrePrintDic(ip):
    timelength = datetime.strptime(ipLastDic[ip], "%Y-%m-%d %H:%M:%S") - datetime.strptime(ipStartDic[ip][0], "%Y-%m-%d %H:%M:%S")
    outputString = ip + "," + ipStartDic[ip][0] + "," + ipLastDic[ip] + "," + str(timelength.seconds + 1) + "," + str(ipRequestCount[ip])
    prePrintoutDic[ipStartDic[ip][0] + " " + time.strftime(time(microsecond=ipStartDic[ip][1]), "%f")] = outputString


def removeDic(ip):
    del ipStartDic[ip]
    del ipLastDic[ip]
    del ipRequestCount[ip]

def checkInactivity(checkDatetime):
    #for in ipLastDic
    for k, d in ipLastDic.items():
        # if inact -> remove in ipStartDic, ipRequestCount, and then write to file.
        if datetime.strptime(d, "%Y-%m-%d %H:%M:%S") < checkDatetime:
            # do remove ...
            makePrePrintDic(k)
            removeList.append(k)
    #write
    #f = open(sys.argv[3], "a")
    #f.seek(0,2)
    for i in sorted(prePrintoutDic.keys()):
        f.write(prePrintoutDic[i])
        f.write("\n")
    #f.close()
    prePrintoutDic.clear()
    for ip in removeList:
        removeDic(ip)
    removeList.clear()



ordering = 0 # number for record the order of data in each second

reader.__next__() #skip the first line(header)
r = next(reader)
dtstr = r[1] + " " + r[2]
currentDatetime = dtstr # initial Datetime

csvf.seek(0)
reader.__next__()
for row in reader:
    dtstr = row[1] + " " + row[2]

    while dtstr != currentDatetime:
        ordering = 0
        currentDatetime = datetime.strftime(datetime.strptime(currentDatetime, "%Y-%m-%d %H:%M:%S") + timedelta(seconds=1), "%Y-%m-%d %H:%M:%S")
        checkInactivity(datetime.strptime(currentDatetime, "%Y-%m-%d %H:%M:%S") - timedelta(seconds=inactivityPeriod))

    ordering += 1
    dt = datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")

    #add ipStartDic (if non)
    if row[0] not in ipStartDic:
        ipStartDic[row[0]] = (dtstr, ordering)
    #add/modified ipLastDic
    ipLastDic[row[0]] = dtstr
    #increase count in ipRequestCount
    if row[0] not in ipRequestCount:
        ipRequestCount[row[0]] = 0
    ipRequestCount[row[0]] += 1;

#end of file -> dump all the data even still in activity
checkInactivity(datetime.strptime(currentDatetime, "%Y-%m-%d %H:%M:%S") + timedelta(days=1))
f.close()
