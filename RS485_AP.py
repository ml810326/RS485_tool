import time
import serial
import binascii
import sys
import getopt

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

devi='/dev/ttyUSB0'
baudrat=115200
outtime=1
num=1
dela=0.5
show=60
myopts, args = getopt.getopt(sys.argv[1:],"d:r:o:n:t:s:")
for o, a in myopts:
	if o == '-d':
		devi=a
	if o == '-r':
		baudrat=int(a)
	if o == '-o':
		outtime=int(a)
	if o == '-n':
		num=int(a)
	if o == '-t':
		dela=float(a)
	if o == '-s':
		show=int(a)

ser = serial.Serial(devi, baudrate=baudrat, timeout=outtime)
count=0
cor=0
incor=0
rfail=0
tstart=time.time()
response_time = [0]*(num+1)
response_max = [0]*(num+1)
response_count = [0]*(num+1)
while True:
    for i in range(1, (num+1), 1):
        time.sleep(dela)
	flag = 0
        out=chr(i) + "\x04\x00\x00\x00\x02"
        crccode = crc16(out)
	start = time.time()
        ser.write(out + chr(crccode&0xff) + chr(crccode>>8))
        ret1 = ser.read(9)
	end = time.time()
        print((out + chr(crccode&0xff) + chr(crccode>>8)).encode('hex'))
        count=count+1
        if not ret1 or len(ret1) != 9:
            print("incorrect: " + ret1)
            rfail=rfail+1
            continue
        data = crc16(ret1[0:7])
        crc = ord(ret1[8]) * 256 + ord(ret1[7])
	print(str(i) + ": " + str(end - start))
        if data == crc:
            cor=cor+1
	    flag = 1
            print("correct: " + ret1.encode('hex'))
        else:
            incor=incor+1
            print("incorrect: " + ret1.encode('hex'))
	if flag == 1:
	    response_time[i] = response_time[i] + (end-start)
	    response_count[i] = response_count[i] + 1
	    if response_max[i] < (end-start):
		response_max[i] = end - start
	if i == 1 and response_count[i] % 10 == 0:
	    for j in range (1, (num+1), 1):
	        if response_count[j] != 0:
		    print(str(j) + " " + str(response_count[j]) + " " + str(response_time[j]/response_count[j]) + " " + str(response_max[j]))
        if (time.time()-tstart)>=show:
            print("count " + str(count))
            print("cor " + str(cor))
            print("incor " + str(incor))
            print("read fail " + str(rfail))
            tstart=time.time()

exit()
