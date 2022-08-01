import time
from datetime import datetime
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetMikoTimeoutException
from netmiko import NetmikoAuthenticationException

start = time.perf_counter()

# current date and time
curDT = datetime.now()
# current day
day = curDT.strftime("%d")
# print("day:", day)
# current month
month = curDT.strftime("%m")
# print("month:", month)
# current year
year = curDT.strftime("%Y")
# print("year:", year)
# current time
# time = curDT.strftime("%H:%M:%S")
# print("time:", time)
# current date and time
date_time = curDT.strftime("%m/%d/%Y, %H:%M:%S")
# print("date and time:", date_time)

with open('commands_all_devices.txt') as f:
	commands_list = f.read().splitlines()

with open('devices_list.txt') as f:
	devices_list = f.read().splitlines()

log = open('log.txt', 'a')

count = 0

for devices in devices_list:
	device_Info = devices.split(",")
	device_Username = device_Info[0]
	ip_address_of_device = device_Info[1]
	pass_Of_Device = device_Info[2]
	print(f"{'#'*20} Connecting to " + ip_address_of_device + f" {'#'*20}")
	fgt_device = {
		'device_type': 'fortinet',
		'ip': ip_address_of_device,
		'username': device_Username,
	    'password': pass_Of_Device,
		 }
	
	try:
		net_connect = ConnectHandler(**fgt_device)
		output = net_connect.send_config_set(commands_list,cmd_verify=False)
		print(output)
		print(f"{'#'*20} " + ip_address_of_device  + f" Connected {'#'*24}")
		count += 1

	except (NetmikoAuthenticationException):
		print(date_time + '   ' + ip_address_of_device + '   ' + device_Username +' Authentication failure: ' + '\n')
		log.write(date_time + ',' + ip_address_of_device + ',' + device_Username +',Authentication failure: ' + '\n')
		continue
	except (NetMikoTimeoutException):
		print(date_time + '   ' + ip_address_of_device + '   ' + device_Username +' Timeout to device: ' + '\n')
		log.write(date_time + ',' + ip_address_of_device + ',' + device_Username +',Timeout to device: ' + '\n')
		continue
	except (EOFError):
		print(date_time + '   ' + ip_address_of_device  + '   ' + device_Username + ' End of file while attempting device ' + '\n')
		log.write(date_time + ',' + ip_address_of_device + ',' + device_Username +',End of file while attempting device ' + '\n')
		continue
	except (SSHException):
		print(date_time + '   ' + ip_address_of_device + '   ' + device_Username + ' SSH Issue: Are you sure SSH is enable??? ' + '\n')
		log.write(date_time + ',' + ip_address_of_device + ',' + device_Username +',SSH Issue: Are you sure SSH is enable??? ' + '\n')
		continue
	except Exception as unknown_error:
		print(date_time + '   ' + ip_address_of_device + '   ' + device_Username + ' Some other error: ' + unknown_error + '\n')
		log.write(date_time + ',' + ip_address_of_device + ',' + device_Username +',Some other error: ' + unknown_error + '\n')
		continue

end = time.perf_counter()
print( '\r\nNumber of IP: ' + str(count) + f'\r\nFinished in {round(end-start, 2)} second(s)\r\n')