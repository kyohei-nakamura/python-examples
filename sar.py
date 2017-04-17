import sys
import os
from datetime import datetime as dt
import csv
import pandas as pd
import subprocess

import time

# check parameter
if(len(sys.argv) != 3):
  print 'Usage: $ python %s server_list timestamp_list' % sys.argv[0]
  quit()

SERVERS=sys.argv[1]
TIMESTAMPS=sys.argv[2]

# read input files
df_sv = pd.read_csv(SERVERS)
df_ts = pd.read_csv(TIMESTAMPS)

dirname = 'result_%s' % dt.now().strftime('%Y%m%d%H%M%S')
os.mkdir(dirname)

# iterate servers list
for index_sv, row_sv in df_sv.iterrows():
  hostname = row_sv['hostname']
  cpunum = row_sv['cpunum']

  # open output file
  ofile = open('./%s/%s_cpu%s_info_%s.csv' % ( \
    dirname, \
    hostname, \
    cpunum, \
    dt.now().strftime('%Y%m%d%H%M%S')), 'a')

  writer = csv.writer(ofile)

  # iterate timestamps list
  for index_ts, row_ts in df_ts.iterrows():
    starttime = dt.strptime(str(row_ts['starttime']), '%Y%m%d%H%M%S')
    endtime = dt.strptime(str(row_ts['endtime']), '%Y%m%d%H%M%S')
    output_list = list(row_ts)

    try:
      # execute sar
      output = subprocess.check_output( \
        'ssh %s sar -P %s -f /var/log/sysstat/sa%s -s %s -e %s 2>&1 | grep "^Average:"' % ( \
          hostname, \
          cpunum, \
          starttime.strftime('%d'), \
          starttime.strftime('%H:%M:%S'), \
          endtime.strftime('%H:%M:%S')), shell=True)

      output_list.extend(output.split()[2:])
    except:
      output_list.append('N/A')

    # output csv
    writer.writerow(output_list)

  time.sleep(1)

# close file
ofile.close()
