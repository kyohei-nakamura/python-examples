import pandas as pd
import datetime as dt
import sys
import subprocess
import csv
import socket

# check parameter
if(len(sys.argv) != 3):
  print 'Usage: $ python %s filename cpu_num' % sys.argv[0]
  quit()

# get parameter
FILENAME=sys.argv[1]
CPU_NUM=sys.argv[2]

# open file (get writer)
df = pd.read_csv(FILENAME)
ofile = open('%s_cpu%s_info_%s.csv' % (socket.gethostname(), CPU_NUM, dt.datetime.now().strftime('%Y%m%d%H%M%S')), 'a')
writer = csv.writer(ofile)

# iterate row
for key, row in df.iterrows():
  # get column
  header1 = row['header1']
  header2 = row['header2']
  starttime = dt.datetime.strptime(str(row['time1']), '%Y%m%d%H%M%S')
  endtime = dt.datetime.strptime(str(row['time2']), '%Y%m%d%H%M%S')
  outputList = [header1, header2, starttime.strftime('%Y/%m/%d %H:%M:%S'), endtime.strftime('%Y/%m/%d %H:%M:%S')]

  try:
    # execute sar
    output = subprocess.check_output('sar -P %s -f /var/log/sysstat/sa%s -s %s -e %s 2>&1 | grep "^Average:"' % (CPU_NUM, starttime.strftime('%d'), starttime.strftime('%H:%M:%S'), endtime.strftime('%H:%M:%S')), shell=True)
    outputList.extend(output.split()[2:])
  except:
    outputList.append('N/A')

  # output csv
  writer.writerow(outputList)

# close file
ofile.close()
