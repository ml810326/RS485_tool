import serial
import time
import sys
import getopt
import binascii

def crc16(data):
    crc = 0xFFFF
    for p in data:
        crc = crc ^ ord(p)
        for i in range(0, 8, ):
            flag = crc & 1
            crc = crc >> 1
            if flag:
                crc = crc ^ 0xA001
    return crc


device = '/dev/ttyUSB0'
baudrat = 115200
outtime = 3
num = 17
tim = 60
myopts, args = getopt.getopt(sys.argv[1:],"d:r:o:n:t:")
for o, a in myopts:
	if o == '-d':
		device=a
	elif o == '-r':
		baudrat=int(a)
	elif o == '-o':
		outtime=int(a)
	elif o == '-n':
		num=int(a)
	elif o == '-t':
		tim=int(a)


ser = serial.Serial(device, baudrate=baudrat ,timeout=outtime)
response_time = [0]*(num+1)
response_max = [0]*(num+1)
response_count = [0]*(num+1)
delay_time = [0]*(num+1)
delay_max = [0]*(num+1)
delay_count = [0]*(num+1)
count=0
max_value = 0
all_value = 0
count = 0
start = 0
end = 0
tstart=time.time()
while 1:
	ret1 = ser.read(8)
	end = time.time()
	print("delay time: " + str(end - start))	
	print ret1.encode('hex')
	ret2 = ser.read(9)
	end_de = time.time()	
	res = end_de - end
	print("response time: " + str(res))
        
        if not ret2 or len(ret2) != 9:
            	print("incorrect: " + ret2.encode('hex'))
		continue
        else:
                data = crc16(ret2[0:7])
                crc = ord(ret2[8]) * 256 + ord(ret2[7])
                if data == crc:
                        print("correct: " + ret2.encode('hex'))
                else:
                        print("incorrect: " + ret2.encode('hex'))
		response_time[ord(ret1[0])] = response_time[ord(ret1[0])] + res
        	response_count[ord(ret1[0])] = response_count[ord(ret1[0])] + 1
        	if response_max[ord(ret1[0])] < res:
                	response_max[ord(ret1[0])] = res
        	delay_time[ord(ret1[0])] = delay_time[ord(ret1[0])] + (end-start)
        	delay_count[ord(ret1[0])] = delay_count[ord(ret1[0])] + 1
        	if delay_max[ord(ret1[0])] < (end-start):
                	delay_max[ord(ret1[0])] = end - start 
	
	
	if (time.time()-tstart)>=tim:
		print "response time table"
		for j in range (1, (num+1), 1):
                	if response_count[j] != 0:
                        	print(str(j) + " " + str(response_count[j]) + " " + str(response_time[j]/response_count[j]) + " " + str(response_max[j]))
                	else:
                        	print(str(j) + " " + str(response_count[j]))
		print "delay time table"
		for j in range (1, (num+1), 1):
                	if delay_count[j] != 0:
                    		print(str(j) + " " + str(delay_count[j]) + " " + str(delay_time[j]/delay_count[j]) + " " + str(delay_max[j]))
		tstart = time.time()
	start = time.time()	
ser.close()

