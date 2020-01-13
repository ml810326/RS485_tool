import serial
import time
import getopt
import sys

device = '/dev/ttyUSB0'
baudrat = 115200
outtime = 1
receive = 0
write = 0
timeout_test = 1
myopts, args = getopt.getopt(sys.argv[1:],"d:r:o:g:s:t:")
for o, a in myopts:
        if o == '-d':
                device=a
        elif o == '-r':
                baudrat=int(a)
        elif o == '-o':
                outtime=float(a)
	elif o == '-g':
		receive=int(a)
	elif o == '-s':
		write=int(a)
	elif o == '-t':
		timeout_test=int(a)

ser = serial.Serial(device, baudrate=baudrat,timeout=3)
command="\x0e\x04\x00\x00\x00\x02\x71\x34"
out="\x0e\x04\x04\x00\xf7\x02\x4a\x35\xe1"
if timeout_test==1:
	while 1:
		ret = ser.read(8)
		if ret == command:
			print ret.encode('hex')
			time.sleep(outtime)
			ser.write(out)
		else:
			ret1 = ser.read(9)
			print ret.encode('hex')
elif receive==1:
	if write==1:
		while 1:
			ret2 = ser.read(9)
			print("read data: " + ret2.encode('hex'))
			ser.write(out)
	else:
		while 1:
			ret2 = ser.read(9)
			print("read data: " + ret2.encode('hex'))
elif write==1:
	while 1:
		ser.write(out)
	
ser.close()

