import re
import datetime
import time

def open_gpuz(path = "GPU-Z Sensor Log2.txt"):
    fh = open(path)
    result = dict()

    index = fh.readline().split(',')
    for i in range(len(index)):
        index[i] = index[i].strip().decode('cp1251')
    index.remove(u'')
    result["index"] = index

    sensors = {item: [] for item in index}
    for line in fh:
        row = line.split(',')
        if "Date" in line or line.strip() == "": # TODO: make pause visible
            continue
        for i in range(len(index)):
            if row[i].strip() == "-":
                row[i] = 0
            if u'Date' in index[i]:
                r = row[i]
                #sensors[index[i]].append( gpu_datetime(row[i]) ) # row[i].decode("cp1251")
                sensors[index[i]].append( gpu_unixtime(row[i]) )
            elif u"RPM" in index[i]:
                sensors[index[i]].append( int(row[i]) )
            elif u"MB" in index[i]:
                sensors[index[i]].append( int(row[i]) )
            elif u'%' in index[i] and u'TDP' not in index[i]:
                sensors[index[i]].append( int(row[i]) )
            else:
                sensors[index[i]].append( float(row[i]) )
    result["sensors"] = sensors

    dimension = {}
    for item in index:
        d = re.findall("\[(.+)\]", item)
        if len(d) != 0:
            dimension[d[0]] = None
    result["dimension"] = dimension.keys()

    fh.close()

    return result

def gpu_datetime(s):
    """s= '2016-02-27 08:27:24'"""
    s = s.strip().split(' ')
    d = []
    for x in s[0].split('-'):
        d.append(int(x))
    t = []
    for x in s[-1].split(':'):
        t.append(int(x))

    return datetime.datetime(d[0], d[1], d[2], t[0], t[1], t[2])

def gpu_unixtime(s):
    return time.mktime( time.strptime(s.strip(), "%Y-%m-%d %H:%M:%S") )

if __name__ == '__main__':
    r = open_gpuz()

    for item in r["index"]:
        print item, r["sensors"][item]
    print
    print r["dimension"]