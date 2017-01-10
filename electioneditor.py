from __future__ import print_function

import serial, time, random, math
from math import pow
from time import sleep


DEBUG_LEDs = True
DEBUG_Remote = True

years=range(2008,2024,2)

sensorValues={"economyStrength":0.5,"politicalSpending":0.5,"voterFraud":0.5,"lies":0.5,"voterAge":0.5,"voterApathy":0.5,"voterGender":0.5, "climateChange":0,"riggedElection":0, "mediaBias": 0.5}

compensations={"altright":[ [0.0, 1] ], "right":[ [1.0, 1] ], "independent":[ [0.1, 1] ], "left":[ [1.0, 1] ], "altleft":[ [0, 1] ], "libertarian":[ [0.2, 1] ], "green":[ [0.1, 1] ] }
compensation={}


elections = {}
elections[2008]={"eligibleVoters": 229945, "votes": {"president": {"right": 59950323, "left": 69499428, "independent": (739278 + 523433) }}, "races": ["president","governor1","congress1"]}
elections[2010]={"eligibleVoters": int(229945*pow(1.023062037,0.5)), "votes": {}, "races": ["governor2","congress2"]}
elections[2012]={"eligibleVoters": 235248, "votes": {"president": {"right": 60934407 , "left": 65918507 , "independent": 1275923 + 469015 }}, "races": ["president","governor1","congress1"]}
elections[2014]={"eligibleVoters": int(235248*pow(1.067413963,0.5)),"votes": {}, "races": ["governor2","congress2"]}
elections[2016]={"eligibleVoters": 251107, "votes": {"president": {"right": 62235228, "left": 64434101, "independent": 559568 + 1395217 + 4418051}}, "races": ["president","governor1","congress1"]}
elections[2018]={"eligibleVoters": int(251107*pow(1.067413963,0.5)),"votes": {}, "races": ["governor2","congress2"]}
elections[2020]={"eligibleVoters": int(251107*1.067413963), "votes": {}, "races": ["president","governor1","congress1"]}
elections[2022]={"eligibleVoters": int(251107*pow(1.067413963,1.5)),"votes": {}, "races": ["governor2","congress2"]}
elections[2024]={"eligibleVoters": int(251107*pow(1.067413963,2)), "votes": {}, "races": ["president","governor1","congress1"]}

print (str(elections))
def doElectionCompensation(year):
    getElectionContext(year)


def doSensorCompensation():

    # empty out existing sensor compensations

    for party in compensations:
        compensations[party] = []

    # Media bias

    compensations["altright"].append([ translate(sensorValues["mediaBias"],0.75, 1.0, 0, 1), 2])
    compensations["right"].append([ translate(sensorValues["mediaBias"],0.5, 0.9, 0, 1), 2])
    if (sensorValues["mediaBias"] < 0.5):
        compensations["independent"].append([ translate(sensorValues["mediaBias"],0.4, 0.5, 0.5, 0.6), 2])
    else:
        compensations["independent"].append([ translate(sensorValues["mediaBias"],0.5, 0.6, 0.6, 0.5), 2])
    compensations["left"].append([ translate(sensorValues["mediaBias"],0, 0.5, 1, 0), 2])
    compensations["altleft"].append([ translate(sensorValues["mediaBias"],0, 0.2, 1, 0), 2])
    compensations["libertarian"].append([ translate(sensorValues["mediaBias"],0.6, 0.9, 0.5, 0.7), 2])
    compensations["green"].append([ translate(sensorValues["mediaBias"],0.1, 0.3, 0.7, 0.5), 2])


    # Economy strength



    # Political spending



    # Voter fraud



    # Lies

    compensations["altright"].append([ translate(sensorValues["lies"],0.5, 1.0, 0, 1), 1])
    compensations["right"].append([ translate(sensorValues["lies"],0, 1.0, 0.4, 0.7), .5])


    # Climate change

    compensations["green"].append([ 1, 1])
    compensations["right"].append([ 0, 1])
    compensations["left"].append([ .75, 1])

    # Rigged election



def getElectionContext(year):
    index = years.index(year)

def processCompensations():

    for party in compensations:
        total = 0
        divisor = 0
        for factor in compensations[party]:
            total = total + factor[0]
            divisor = divisor + factor[1]
        compensation[party] = total / divisor




OUTPUT = 1
INPUT = 0
INPUT_PULLUP = 2
HIGH = 1
LOW = 0


remoteDigitalPins =  [{"value": LOW,"mode": INPUT,"changed": 0,"watched": 0} for k in range(25)]
remoteAnalogPins =  [{"value": LOW,"mode": INPUT,"changed": 0,"watched": 0} for k in range(25)]
(A0, A1, A2, A3, A4, A5, A6, A7) = range(14,22)
remoteEncoder = 0
remoteLEDs =  [[0,0,0] for k in range(40)]


port = "/dev/ttyUSB0"
ser = serial.Serial(port,115200,timeout=None,write_timeout=None)
print(str(ser.get_settings()))


def remoteWrite(*values):

    if DEBUG_Remote:
        print("-> " + formatRemoteValues(values))

    # while (ser.out_waiting):
    #     time.sleep(0.0001)
    theBytes = bytearray(values)
    # print(theBytes)
    ser.write(theBytes)
    # for value in values:
    #     print (value)
    #     print (type(value))
    #     if (type(value) is str):
    #          ser.write(value)
    #     elif (type(value) is int):
    #          ser.write(chr(value))
    #          print(chr(value))
    #     else:
    #         ser.write(value)
    if DEBUG_Remote:
        print("waiting for flush", end="")
    sleep(0.0005)
    while (ser.out_waiting):
        sleep(0.0001)
        if DEBUG_Remote:
            print('.', end="")
    if DEBUG_Remote:
        print(" ")
        print("waiting for response", end="")
    while (ser.in_waiting is 0):
        sleep(0.0001)
        if DEBUG_Remote:
            print('.', end="")
    if DEBUG_Remote:
        print(" ")

    remoteRead()
    # ser.flush()
    while ser.in_waiting:
        remoteRead()


def remoteDigitalRead (pin, cached=False):
    remoteDigitalPins[pin]["changed"]=False
    if (cached==True):
        return remoteDigitalPins[pin]["value"]
    else:
        remoteWrite('r',chr(pin))
        # remoteRead()
        return remoteDigitalPins[pin]["value"]

def hasRemoteDigitalPinChanged (pin):
    previous = remoteDigitalPins[pin]["changed"]
    remoteDigitalPins[pin]["changed"]=False
    return previous

def remoteAnalogRead (pin, cached=False):
    remoteAnalogPins[pin]["changed"]=False
    if (cached==True):
        return remoteAnalogPins[pin]["value"]
    else:
        remoteWrite('R',chr(pin))
        # remoteRead()
        return remoteAnalogPins[pin]["value"]

def remoteRead ():
    command = getBytes(1)
    values = []
    if (command=='!'):
        print("Remote client online.")
        remoteInitializePins()
    elif (command=='\n'):
        print("Received blank command")
    elif (command=='\r'):
        print("Received blank command")
    elif (command=='*'):
        print("Remote client timed out waiting for us")

    elif (command=='.'):
        if DEBUG_LEDs:
            print("LED updated")

    elif (command=='b'):
        values = getBytes(1)
        if DEBUG_LEDs:
            print("LED brightness now " + str(values[0]))

    elif (command=='?'):
        print("Remote client did not understand message")

    elif (command==0):
        remoteRead()

    elif (command=='X'):
        print("Remote client did not understand message")
        values = getBytes(1)
        # time.sleep(2)

    elif (command=='M'):
        values = getBytes(1)
        if DEBUG_Remote:
            print ("Pin monitoring enabled for " + str(ord(values[0])))

    elif (command=='m'):
        values = getBytes(1)
        if DEBUG_Remote:
            print ("Pin monitoring disabled for " + str(ord(values[0])))

    elif (command=='P'):
        values = getBytes(2)

    elif (command=='d'):
        pin = int(ord(getBytes(1)))
        value = getBytes(1)
        values=[pin,value]

        if (pin < 24):

            # print(str(pin) + " pin: ")
            changed = ( remoteDigitalPins[pin]["value"] != value )
            # print(" changed? " + str(changed))
            if (type(value) is str):
                value = ord(value)
            remoteDigitalPins[pin]["changed"]= changed
            remoteDigitalPins[pin]["value"]=value
            # print ("type of value is " + str(type(value)))
            #
            # print ("type in array is " + str(type(remoteDigitalPins[pin]["value"])))

        else:
            print("Pin value for 'd' was out of range: " + str(pin))


    elif (command=='E'):
        value = getBytes(1)
        if value < 25:
            remoteEncoder += value
        values=[value]

    elif (command=='e'):
        value = getBytes(1)
        if value < 25:
            remoteEncoder -= value
        values=[value]

    elif (command=='A'):
        values = getBytes(2)
        pin = int(ord(values[0]))
        if (pin < 24):

            # print("byte 0 is " + str(int(ord(values[1]))))
            # print("byte 1 is " + str(int(ord(values[2]))))
            # print(str(pin) + " pin: ")
            analogValue = int(ord(values[1]))

            changed = ( remoteDigitalPins[pin]["value"] != analogValue )
            # print(" changed? " + str(changed))

            remoteDigitalPins[pin]["changed"] = changed
            remoteDigitalPins[pin]["value"]=analogValue

    elif (command=='a'):
        values = getBytes(3)
        pin = int(ord(values[0]))
        if (pin < 24):

            # print("byte 0 is " + str(int(ord(values[1]))))
            # print("byte 1 is " + str(int(ord(values[2]))))
            # print(str(pin) + " pin: ")
            analogValue = int(ord(values[1])) + (int(ord(values[2]))<<8)

            changed = ( remoteAnalogPins[pin]["value"] != analogValue )
            # print(" changed? " + str(changed))

            remoteAnalogPins[pin]["changed"] = changed
            remoteAnalogPins[pin]["value"]=analogValue
        else:
            print("Pin value for 'a' was out of range: " + str(pin))
    if DEBUG_Remote:
        print("<- " + str(command) + "," + formatRemoteValues(values))


def formatRemoteValues(values):
    returnValue=""
    for a in values:
        if (type(a) is int):
            if (a > 31 and a < 127):
                returnValue = returnValue + "'" + str(a) + "' (" + str(a) + "), "
            else:
                returnValue = returnValue + "(" + str(a) + "), "
        elif (type(a) is str):
            if ((ord(a) > 31 ) and ( ord(a) < 127)):
                returnValue = returnValue + "'" + str(a) + "' (" + str(ord(a)) + "), "
            else:
                returnValue = returnValue + "(" + str(ord(a)) + "), "
    return returnValue

def getBytes(number):
    return ser.read(number)

def remoteDigitalWrite (pin, value):
    remoteWrite('w',chr(pin),chr(value))
    remoteDigitalPins[pin]["value"]=value

def remoteAnalogWrite (pin, value):
    remoteWrite('W',chr(pin),value)
    remoteDigitalPins[pin]["value"]=value

def remotePinMode (pin, mode):
    command='i'
    if (mode==OUTPUT):
        command='o'
    elif (mode==INPUT):
        command='i'
    elif (mode==INPUT_PULLUP):
        command='I'
    else:
        return
    remoteWrite(command, chr(pin))
    remoteDigitalPins[pin]["mode"]=mode

def remoteMonitorDigitalPin(pin):
    remoteWrite('M',chr(pin))
    remoteDigitalPins[pin]["changed"]=True

def remoteStopMonitoringDigitalPin(pin):
    remoteWrite('m', chr(pin))

def remoteLED(led,red,green,blue):
    remoteLEDs[led]=[red,green,blue]
    remoteWrite('l',chr(led),chr(red),chr(green),chr(blue))
    time.sleep(0.001)

def remoteLEDBrightness(brightness):
    remoteWrite('b',chr(brightness))
    time.sleep(0.005)

def remoteInitializePins():
    remotePinMode(5,OUTPUT)
    # remoteDigitalWrite(5,HIGH)
    remotePinMode(6,OUTPUT)
    # remoteDigitalWrite(6,HIGH)
    time.sleep(0.005)

    remotePinMode(2,INPUT_PULLUP)
    remotePinMode(7,INPUT_PULLUP)
    remotePinMode(8,INPUT_PULLUP)
    time.sleep(0.005)

    remoteMonitorDigitalPin(2)
    remoteMonitorDigitalPin(7)
    remoteMonitorDigitalPin(8)
    time.sleep(0.005)

    remotePinMode(10,OUTPUT)
    remoteAnalogWrite(10,127)

    return

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    if (value < leftMin):
        value = leftMin
    if (value > leftMax):
        value = leftMax
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)



time.sleep(2)
remoteInitializePins()
doSensorCompensation()
processCompensations()
print(str(compensation))

print(remoteAnalogRead(3))



changed = False

while True:
    while ser.in_waiting:
        remoteRead()
    # remoteAnalogRead(0)
    # remoteAnalogRead(1)
    # remoteAnalogRead(2)
    # remoteAnalogRead(3)
    #
    # remoteDigitalRead(2)
    # remoteDigitalRead(7)
    # remoteDigitalRead(8)

    if (remoteDigitalPins[2]["changed"] == True):
        sensorValues["doProcess"] = True;
        remoteDigitalPins[2]["changed"] = False;
        # print("pin A0 is now " + str(remoteAnalogPins[0]["value"]))
        print ("process requested by user ")
        changed=True

    if (remoteDigitalPins[7]["changed"] == True):
        sensorValues["climateChange"] = (remoteDigitalPins[7]["value"] == LOW);
        remoteDigitalPins[7]["changed"] = False;

        if (sensorValues["climateChange"] == True):
            remoteDigitalWrite(5,HIGH)
        else:
            remoteDigitalWrite(5,LOW)


        # print("pin A0 is now " + str(remoteAnalogPins[0]["value"]))
        print ("climate change raw value is now " + str(remoteDigitalPins[7]["value"]))
        changed=True

    if (remoteDigitalPins[8]["changed"] == True):
        print (str(remoteDigitalPins[8]))
        sensorValues["riggedElection"] = (remoteDigitalPins[8]["value"] == LOW);
        remoteDigitalPins[8]["changed"] = False;

        # if (sensorValues["riggedElection"] == True):
        #     remoteDigitalWrite(6,HIGH)
        # else:
        #     remoteDigitalWrite(6,LOW)

        # print("pin A0 is now " + str(remoteAnalogPins[0]["value"]))
        print ("rigged election raw value is now " + str(remoteDigitalPins[8]["value"]))
        print ("riggedElection parsed to " + str(sensorValues["riggedElection"]))
        changed=True

    if (remoteAnalogPins[0]["changed"] == True):
        sensorValues["voterAge"] = translate(remoteAnalogPins[0]["value"],472,550,0,1)
        # print("pin A0 is now " + str(remoteAnalogPins[0]["value"]))
        print ("voter age raw value is now " + str(remoteAnalogPins[0]["value"]))
        changed=True

    if (remoteAnalogPins[1]["changed"] == True):
        sensorValues["voterApathy"] = translate(remoteAnalogPins[1]["value"],472,550,0,1)
        print("voter apathy raw value is now " + str(remoteAnalogPins[1]["value"]))
        changed=True

    if (remoteAnalogPins[2]["changed"] == True):
        sensorValues["voterGender"] = translate(remoteAnalogPins[2]["value"],472,550,0,1)
        print("voter gender raw value is now " + str(remoteAnalogPins[2]["value"]))
        changed=True


    if (remoteAnalogPins[3]["changed"] == True):
        remoteAnalogPins[3]["changed"] = False
        sensorValues["mediaBias"] = translate(remoteAnalogPins[3]["value"],507,551,0,1)
        # Do something to de-log
        print("media bias raw value is now " + str(remoteAnalogPins[3]["value"]))
        changed=True

    if (changed):
        changed=False
        doSensorCompensation()
        processCompensations()
        print(str(compensation))

    if (DEBUG_LEDs):
        remoteLEDBrightness(random.randint(0,255))
        for a in range(40):
            color = [random.randint(0,120),random.randint(0,120),random.randint(0,120)]
            # print(str(a) + " to " + str(color))
            remoteLED(a,color[0],color[1],color[2])
            time.sleep(1/200)


    time.sleep(2)
