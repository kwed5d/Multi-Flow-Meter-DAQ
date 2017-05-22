#KU_Flowmeter_Cal_rev2: changing Coeffiecents
#KU_Flowmeter_Cal_rev3: Added Weight Coeffiecents, still needs calcs
#KU_Flowmeter_Cal_rev4: Added to while loop, outputs updated flow data with errors
#KU_Flowmeter_Cal_rev5: Using only Coefficients from weight calibration

import RPi.GPIO as GPIO
import time, sys
import signal

FS1 = 12 
FS2 = 16
FS3 = 20
FS4 = 21

# Wet-Wet transducer coefficients 
#C1= 27.0034 
#C2= 269.303
#C3= 396.05473
#C4= 421.969

# Weight calibration coeffiecients @ 30 LPM

K1= 28.1591
K2= 290.087
K3= 392.58
K4= 438.814

chan_list = [12,16,20,21]

GPIO.setmode(GPIO.BCM)

GPIO.setup(FS1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(FS2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(FS3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(FS4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

count12 = 0
count16 = 0
count20 = 0
count21 = 0

delay = 60
tpass = 0
t_old = 0 
counttime = 0
tloop = 0
tlooptotal = 0

w_old=0
x_old=0
y_old=0
z_old=0

wc_old=0
xc_old=0
yc_old=0
zc_old=0

print('Data Collection Initialized')
print('Data Collection Initialized')
print('Data Collection Initialized')
print('Data Collection Initialized')
print('Data Collection Initialized')

# Beginning of data collection
timestart = time.time()

def countPulse(chan_list):

    # Setting count values to global variables for this function loop
    global count12
    global count16
    global count20
    global count21

    # Setting Channels up for Raspberry Pi                        
    FS1 = 12
    FS2 = 16
    FS3 = 20
    FS4 = 21

    if GPIO.event_detected(FS1):
        count12 = count12+1
#        print('F111:')
    elif GPIO.event_detected(FS2):
        count16 = count16+1
#        print('F22222:')
    elif GPIO.event_detected(FS3):
        count20 = count20+1
#        print('F333333:!!!!!!!!')
    elif GPIO.event_detected(FS4):
        count21 = count21+1
#        print('F4:')
    else:        
        print('no change')

# General Purpose Input Output (GPIO) callback that sends the loop back to 'def countPulse()' line after detecting a change in a specific channel 
GPIO.add_event_detect(FS1, GPIO.FALLING, callback = countPulse)
GPIO.add_event_detect(FS2, GPIO.FALLING, callback = countPulse)
GPIO.add_event_detect(FS3, GPIO.FALLING, callback = countPulse)
GPIO.add_event_detect(FS4, GPIO.FALLING, callback = countPulse)

while True:
    try:
        time.sleep(1)
        
        if counttime == delay:
            print('-------------------------------')

            #tloop = time.time()
            
            tpass = time.time() - t_old
            t_old = time.time()
            #print('Timepass:',tpass)
            #print('Old Time:',t_old)

            # Calc the approximate flow rate using the difference between the current and past count values divided by the time passed since the last iteration
            wm = (((count12-wc_old)/tpass)/K1)*60
            xm = (((count16-xc_old)/tpass)/K2)*60
            ym = (((count20-yc_old)/tpass)/K3)*60
            zm = (((count21-zc_old)/tpass)/K4)*60

            # Flow rate calcs for wet-wet transducer coefficients 
            #w = ((count12/delay)/C1)*60
            #x = ((count16/delay)/C2)*60
            #y = ((count20/delay)/C3)*60
            #z = ((count21/delay)/C4)*60

            print('Flow 1:',wm)
            print('Flow 2:',xm)
            print('Flow 3:',ym)
            print('Flow 4:',zm)
            
            #print('Flow 1:',wm,'PULSE:',count12-wc_old)
            #print('Flow 2:',xm,'PULSE:',count16-xc_old)
            #print('Flow 3:',ym,'PULSE:',count20-yc_old)
            #print('Flow 4:',zm,'PULSE:',count21-zc_old)
            #print('F4 Freq:',(count21-zc_old)/tpass)

            # Saving current count value for calculating difference in the next iteration of this if statement
            wc_old=count12
            xc_old=count16
            yc_old=count20
            zc_old=count21

            counttime = 1

            #tlooptotal = time.time() - tloop

            #print('Loop Time:',tlooptotal)
        else:
            counttime=counttime+1
            
            
    except KeyboardInterrupt:
        t = time.time()-timestart

        #w = ((count12/t)/C1)*60
        #x = ((count16/t)/C2)*60
        #y = ((count20/t)/C3)*60
        #z = ((count21/t)/C4)*60

        wm = ((count12/t)/K1)*60
        xm = ((count16/t)/K2)*60
        ym = ((count20/t)/K3)*60
        zm = ((count21/t)/K4)*60
        
        print('<><><><><><><><><><><><><><><><><><><><>')
        print('Runtime:',time.time()-timestart)
        print('-----------------------')
        #print('Flow 1:',w)
        print('Flow 1:',wm)
        print('Pulses:',count12)
        #print('Frequency:',count12/t)
        print('-----------------------')
        #print('Flow 2:',x)
        print('Flow 2:',xm)
        print('Pulses:',count16)
        #print('Frequency:',count16/t)
        print('-----------------------')
        #print('Flow 3:',y)
        print('Flow 3:',ym)
        print('Pulses:',count20)
        #print('Frequency:',count20/t)
        print('-----------------------')
        #print('Flow 4:',z)
        print('Flow 4:',zm)
        print('Pulses:',count21)
        #print('F4 Freq:',(count21)/t)
        #print('Frequency:',count21/t)
        print('-----------------------')
        GPIO.cleanup()
        print('Donzo!')
        print('Runtime:',time.time()-timestart)
        
        sys.exit()


