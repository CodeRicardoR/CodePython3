import os


NameFile = "/home/ricardo/Documents/Python3/DataMin/jica/jic22006.23m"
f = open(NameFile, 'r')
DataLines = f.readlines()
f.close()

DicDataSecH = {}
DicDataSecD = {}
DicDataSecZ = {}
for line in DataLines:
    try:
        a = line.split()
        hour = a[0]
        minute = a[1]
        second = a[2]
        D = float(a[3])
        ListDataD = DicDataSecD.get(minute)
        if ListDataD == None:
            DicDataSecD.setdefault(minute, [])
        DicDataSecD[minute].append(D)

        H = float(a[4])
        ListDataH = DicDataSecH.get(minute)
        if ListDataH == None:
            DicDataSecH.setdefault(minute, [])
        DicDataSecH[minute].append(H)

        Z = float(a[5])
        ListDataZ = DicDataSecZ.get(minute)
        if ListDataZ == None:
            DicDataSecZ.setdefault(minute, [])
        DicDataSecZ[minute].append(Z)
    except:
        continue

ListPromMinuteD = [None]*60
ListPromMinuteH = [None]*60
ListPromMinuteZ = [None]*60

for minute in range(60):
    promD = 0
    for i in DicDataSecD['%02d'%minute]:
        promD = promD + i
    promD = promD/len(DicDataSecD['%02d'%minute])
    ListPromMinuteD[minute] = promD

    promH = 0
    for i in DicDataSecH['%02d'%minute]:
        promH = promH + i
    promH = promH/len(DicDataSecH['%02d'%minute])
    ListPromMinuteH[minute] = promH

    promZ = 0
    for i in DicDataSecZ['%02d'%minute]:
        promZ = promZ + i
    promZ = promZ/len(DicDataSecZ['%02d'%minute])
    ListPromMinuteZ[minute] = promZ

print(ListPromMinuteZ)
