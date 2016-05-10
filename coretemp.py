import re
import datetime, time

def open_coretemp(path = "badCT-Log.csv"):
    fh = open(path, "r")
    result = dict()
    result["info"] = {}

    # Collecting report info: CPUID, Processor, Platform, Revision, Lithography, Session start
    line = fh.readline().split(',')
    while line[0] != "Time":
        if line[0] == "\n":
            line = fh.readline().split(',')
            continue
        result["info"][line[0].decode("cp1252")] = line[1].strip().decode("cp1252")
        line = fh.readline().split(',')

    # Checking number of cores and collecting core values.
    result["core"] = []
    i = 1
    while line[i] != '':
        result["core"].append(line[i][:7].strip().decode("cp1252"))
        i += 1
    number_of_cores = i
    result["core_values"] = [u'Temp. (\xb0)']
    #result["core_values"].extend(line[i+2:i+6])
    for item in line[i+2:i+6]:
        result["core_values"].append(item.decode("cp1252"))

    # Creating subdictionary with keys 'Core 0', 'Core 1' and etc.
    result["sensors"] = dict()
    result["Time"] = []
    for item in result["core"]:
        result["sensors"].setdefault(item, {v: [] for v in result["core_values"]})


    row = fh.readline().split(',')
    while row[0] != "\n":
        try:
            #result["sensors"][result["core"][0]].append(ct_datetime(row[0])) # Time
            result["Time"].append(ct_unixtime(row[0]))
        except:
            # If CT-Log*.csv will be suddenly interrupted, function returns not full result.
            return result

        i = 1
        for item in result["core"]:
            result["sensors"][item][u'Temp. (\xb0)'].append(row[i])
            i += 1

        i += 2
        for item in result["core"]:
            for value in result["core_values"][1:]:
                result["sensors"][item][value].append(row[i])
                i += 1
            i += 1

        row = fh.readline().split(',')

    line = fh.readline().split(',')
    result["info"][line[0].decode("cp1252")] = line[1].strip().decode("cp1252")

    #return sensors, core, core_values, info
    return result

def ct_datetime(s):
    """s = '10:37:18 04/07/16'"""
    s = s.split(' ')
    d = []
    for x in s[-1].split('/')[::-1]:
        d.append(int(x))
    t = []
    for x in s[0].split(':'):
        t.append(int(x))

    return datetime.datetime(2000 + d[0], d[1], d[2], t[0], t[1], t[2])

def ct_unixtime(s):
    return time.mktime( time.strptime(s.strip(), "%H:%M:%S %m/%d/%y") )

if __name__ == '__main__':
    #print ct_datetime()
    s = open_coretemp()
    print s["info"]
    print s["core"]
    print s["core_values"]
    print len(s["Time"])
    print
    print sorted(s["info"].keys())