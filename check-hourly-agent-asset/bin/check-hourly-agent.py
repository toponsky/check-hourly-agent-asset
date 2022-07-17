import subprocess,os,json,socket
from datetime import datetime, time

# This is our shell command, executed by Popen.
def convert_output_to_time_string(lines):
  findTimeInLine = False
  i = 0
  while not findTimeInLine and i < len(lines):
    line = lines[i]
    i = i + 1
    curLine = line.split(" - ")
    
    if("new properties inserted to Collection" in line and len(curLine) == 2):
     findTimeInLine = True
     time_str = curLine[0]
     time_str = time_str.replace("T", " ").replace("Z","")
     return time_str

def convert_time_str_to_time(time_str):
  return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')

def get_time_different(time_1, time_2):
  time_interval = time_1 - time_2
  return time_interval.total_seconds()/3600

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def get_ip_address():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]
  s.close()
  return ip

def check_hourly_task():
  check_result = "Craler finished"
  p = subprocess.Popen("docker logs --tail 5 test", stdout=subprocess.PIPE,shell=True)
  output = p.communicate()[0].decode("utf-8")
  lines = output.split("\n")
  time_str = convert_output_to_time_string(lines)
  if(not time_str):
    exit(0)
    return
  time_obj = convert_time_str_to_time(time_str)
  currentDT = datetime.now()
  time_def = get_time_different(currentDT,time_obj)
  if(not is_time_between(time(8,30), time(20,00)) or time_def < 2):
    print(time_str)
    print(lines[len(lines)-3])
    print(lines[len(lines)-2])
    exit(0)
  else:
    data = {}
    data['subject'] = 'Check Hourly Task Agent'
    data['body'] = "Didn't detect hourly task for hourly task tenant with IP :" + get_ip_address()
    json_data = json.dumps(data)
    print(json_data)
    exit(2)


check_hourly_task()