
import glob
import os

DicMonths = {0:['Cero','cer',0],1:['January','jan',31],2:['February','feb',28],3:["March",'mar',31],4:["April",'apr',30],
5:["May",'may',31],6:["June",'jun',30],7:["July",'jul',31],8:["August",'aug',31],9:["September",'sep',30],
10:["October",'oct',31],11:["November",'nov',30],12:["December",'dec',31]}

NameMonths = {'jan':'January', 'feb':'February', 'mar':'March', 'apr':'April', 'may':'May', 'jun':'June',
'jul':'July', 'aug':'August', 'sep':'September', 'oct':'October', 'nov':'November', 'dec':'December' }


DataYea = 2022
IAGA = 'sta'

if (DataYea % 4) == 0:
	DicMonths[2][2] = 29

DicMonths2 = DicMonths
del DicMonths2[0]

list_days =[]
list_files = []
for key in DicMonths2:
	for day in range(DicMonths2[key][2]):
		list_days.append('"' + DicMonths2[key][0] + ' ' + '%02d'%(day + 1) + ', ' + '%04d'%(DataYea) + '",')
		list_files.append(IAGA + '%02d'%(day + 1) + DicMonths2[key][1] + '.' + '%02d'%(DataYea - 2000) + 'm')


DirFiles = '/home/ricardo/Documents/Python3/DataMin'

os.chdir(DirFiles)
DataFiles = glob.glob(IAGA + '*.%02d'%(DataYea - 2000) + 'm')


SortedFiles = []
for j in list_files:
	for h in DataFiles:
		if j == h:
			SortedFiles.append(h)
data_days = []
for i in SortedFiles:
	string_date = '"' + NameMonths[i[5:8]] + ' ' + i[3:5] + ', 20' + i[9:11] + '",'
	data_days.append(string_date)
	
Disabled_days = []
limit = len(data_days)
for n in list_days:
	conta = 0
	for m in data_days:
		if n!=m:
			conta = conta + 1
	if conta == limit:
		Disabled_days.append(n)


NameFile = '/home/ricardo/Documents/Python3/DateFiles.txt'
f = open(NameFile, 'w')
f.write('[' + '\n')
for i in Disabled_days:
	f.write(i + '\n')
f.write('"January 01, 2000"\n')
f.write(']')
f.close()

print('#####FINISH#####')
