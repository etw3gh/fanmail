#!/usr/bin/env python3
import sys, os, subprocess, time

"""
Determines fan speed for both CPU fans on a Dell Server using openmanage cli

Sends a warning email by AWS SES if MAX_RPM is exceeded 
"""

fans_cmd="/opt/dell/srvadmin/bin/omreport chassis fans | grep Reading | awk {'print $3'}"
mail_cmd="aws ses send-email --from {} --destination '{}' --message '{}'"

while True:

  # get ENV variables
  # will obtain from .bashrc or /etc/sysconfig/fanmail (see README)
  sending_email = os.getenv('SES_SENDER')
  destination_email = os.getenv('SES_DEST')
  max_rpm = int(os.getenv('MAX_RPM'))

  msg = None
  dest = None

  # get RPM values for CPU fans
  fans = subprocess.check_output(fans_cmd, shell=True)
  f = str(fans.decode('utf-8'))

  rpms = []

  # push valid fan speeds onto rpms
  for temp in f.split('\n'):
    if temp.strip() == '':
     continue
    try:
      rpms.append(int(temp))
    except:
      pass

  if len(rpms) >= 2:
    # get the low and high RPM values
    lo, hi = sorted(rpms)[0:2]

    # if the threshold is exceeded then construct the email message and send it
    if hi >= max_rpm:

      # insert RPM values into the email message json
      with open('msg.json', 'r') as msgfile:
        msg = msgfile.read()
        msg = msg.replace('%%F1%%', str(lo)).replace('%%F2%%', str(hi))

      # insert destination email address into the destination json
      with open('dest.json', 'r') as destfile:
        dest = destfile.read()
        dest = dest.replace('%%SES_DEST%%', destination_email)

      # form the email command
      send_cmd = mail_cmd.format(sending_email, dest, msg)

      # send the email by awscli
      os.system(send_cmd)

  # sleep 1 hour
  time.sleep(60 * 60)
