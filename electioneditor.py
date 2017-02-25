from __future__ import print_function

import serial, time, random, math, os
from math import pow
from time import sleep
import numpy as numpy

sysrand = random.SystemRandom()

DEBUG_LEDs = False
# DEBUG_Remote = True
DEBUG_Remote = False

years=range(2008,2024,2)

sensorValues={"economyStrength":0.5,"politicalSpending":0.5,"voterFraud":0.5,"lies":0.5,"voterAge":0.5,"voterApathy":0.5,"voterGender":0.5, "climateChange":0,"riggedElection":0, "mediaBias": 0.5}

compensations={"altright":[ [0.0, 1] ], "right":[ [1.0, 1] ], "independent":[ [0.1, 1] ], "left":[ [1.0, 1] ], "altleft":[ [0, 1] ], "libertarian":[ [0.2, 1] ], "green":[ [0.1, 1] ]  }
compensation={}


elections = {}
elections[2008]={"eligibleVoters": 229945000,
    "votes": {
        "popularVote": {"right": 59950323, "left": 69499428, "independent": (739278 + 523433) },
        "electoralVote": {"right": 173, "left": 365 },
        # "governor1": {"left": 7, "right": 5}
        "governor1": {"right": 21, "left": 29}
    }, "races": ["president","governor1","congress1"]}
elections[2010]={"eligibleVoters": int(229945000*pow(1.023062037,0.5)), "votes": {}, "races": ["governor2","congress2"]}
elections[2012]={"eligibleVoters": 235248000,
    "votes": {
        "popularVote": {"right": 60934407 , "left": 65918507 , "independent": 1275923 + 469015 },
        "electoralVote": {"right": 206 , "left": 332 },
        # "governor1": {"left": 7, "right": 5}
        "governor1": {"right": 30, "left": 19}
        },
    "races": ["president","governor1","congress1"]}
elections[2014]={"eligibleVoters": int(235248000*pow(1.067413963,0.5)),"votes": {}, "races": ["governor2","congress2"]}
elections[2016]={"eligibleVoters":
    { "popularVote": 251107000,
        "electoralVote": 538,
        "governors": 50,
        "supremeCourt": 8,
        "house": 435,
        "senate": 100
    }, "votes":
    {
    "popularVote": {"right": 62979879, "left": 65844954, "independent": 559568 + 1395217 + 4418051},
    "electoralVote": {"left": 232, "right": 306},
    # "governor1": {"left": 8, "right": 4},
    "governor1": {"right": 33, "left": 16},
    "house": {"right": 241, "left": 194},
    "senate": {"right": 52, "left": 46, "independent": 2},
    "supremeCourt": {"right": 4, "left": 4}
    }, "races": ["president","governor1","congress1","supremeCourt"]}
elections[2018]={"eligibleVoters":
    { "popularVote": int(251107000*pow(1.067413963,0.5)),
        "electoralVote": 538,
        "governors": 50,
        "supremeCourt": 9,
        "house": 435,
        "senate": 100
    },"votes": {}, "races": ["governor2","congress2"]}
elections[2020]={"eligibleVoters":
    { "popularVote": int(251107000*1.067413963),
        "electoralVote": 538,
        "governors": 50,
        "supremeCourt": 9,
        "house": 435,
        "senate": 100
    }, "votes": {}, "races": ["president","governor1","congress1"]}
elections[2022]={"eligibleVoters": {
    "popularVote": int(251107000*pow(1.067413963,1.5)),
    "electoralVote": 538,
    "governors": 50,
    "supremeCourt": 9,
    "house": 435,
    "senate": 100
    },"votes": {}, "races": ["governor2","congress2"]}
elections[2024]={"eligibleVoters": {
    "popularVote": int(251107000*pow(1.067413963,2)),
    "electoralVote": 538,
    "governors": 50,
    "supremeCourt": 9,
    "house": 435,
    "senate": 100
    }, "votes": {}, "races": ["president","governor1","congress1"]}

colors = { "left": [ 0, 174, 243 ], "right": [ 200, 69, 52 ], "libertarian": [ 244, 210, 80 ], "green" : [ 130, 166, 59 ] , "altright" : [ 224, 90, 61 ], "independent" : [ 127, 127, 127 ], "altleft" : [ 59, 111, 243 ], "nobody" : [ 0, 0, 0 ] }

leds = {}

leds[0] = { "president": 19, "popularVote": 20, "electoralVote" : 29, "congress" : 10, "house": 30, "senate" : 39, "supremeCourt" : 9, "governors": 0 } ;
leds[1] = { "president": 18, "popularVote": 21, "electoralVote" : 28, "congress" : 11, "house": 31, "senate" : 38, "supremeCourt" : 8, "governors": 1 } ;
leds[2] = { "president": 17, "popularVote": 22, "electoralVote" : 27, "congress" : 12, "house": 32, "senate" : 37, "supremeCourt" : 7, "governors": 2 } ;
leds[3] = { "president": 16, "popularVote": 23, "electoralVote" : 26, "congress" : 13, "house": 33, "senate" : 36, "supremeCourt" : 6, "governors": 3 } ;
leds[4] = { "president": 15, "popularVote": 24, "electoralVote" : 25, "congress" : 14, "house": 34, "senate" : 35, "supremeCourt" : 5, "governors": 4 } ;

displayMappings = { 2016: 0, 2018: 1, 2020: 2, 2022: 3, 2024: 4 }

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
    previousYear = years[index-1]


def processCompensations():
    global compensation,compensations
    for party in compensations:
        total = 0
        divisor = 0
        for factor in compensations[party]:
            total = total + factor[0]
            divisor = divisor + factor[1]
        compensation[party] = total / divisor

def findRatio(year, race):
    global compensation,compensations,elections
    currentYearIndex = years.index(year)
    ratio = {}
    sourceYear = year

    while race is not in elections[sourceYear]["votes"] or count(elections[sourceYear]["votes"][race].keys()) > 1:
        currentYearIndex = currentYearIndex - 1
        sourceYear = years[currentYearIndex]

    eligibleVoters = elections[sourceYear]["eligibleVoters"][race]
    for party in elections[sourceYear]["votes"][race].keys():
        ratio[party] = elections[sourceYear]["votes"][race][party] / eligibleVoters

    elections[year]["ratios"][race] = ratio

    return ratio


def applyRatio(year,race):
    eligibleVoters = elections[year]["eligibleVoters"][race]
    ratio = elections[year]["ratios"][race]
    for party in ratio.keys:
        elections[year]["votes"][party] = ratio[party] / eligibleVoters


def generateElection(year):
    races=elections[year]["races"]
    for race in races:

        if race is "president":
            races.extend(["popularVote","electoralVote"])
            continue

        if race is "congress" or race is "congress1" or race is "congress2":
            races.extend(["house","senate"])
            continue

        if race in elections[year]["eligibleVoters"]:
            pop = elections[year]["eligibleVoters"][race]
            total=sum(compensation.values())

            # uncompensatedVotes = elections[year]["votes"][race]
            ratio = findRatio(year,race)

            # print("Total voters in ",race,"is",pop)
            elections[year]["votes"][race] = {}

            applyRatio(year,race)

            for party in compensation.keys():
                print("Compensation for",party,"is",compensation[party],"out of",total,"or",(compensation[party] / total)*100,"%")
                elections[year]["votes"][race][party] = (compensation[party] / total) * elections[year]["votes"][race][party]

        else:
            print("couldn't find race",race,"in ",year,"races")
    print("Here is",year)
    print(elections[year]["votes"])
    return

# leds[0] = { "president": 19, "popularVote": 20, "electoralVote" : 29, "congress" : 10, "house": 30, "senate" : 39, "supremeCourt" : 9, "governors": 0 } ;
# elections[2008]={"eligibleVoters": 229945, "votes": {"president": {"right": 59950323, "left": 69499428, "independent": (739278 + 523433) }}, "races": ["president","governor1","congress1"]}

def displayElection(year):
    global colors
    global elections
    global displayMappings
    display = displayMappings[year]
    remoteSevenSegment(display,year)
    election = elections[year]
    # print("election year ",year)
    races = election["races"]
    for race in races:
        # print("Considering",race,"in",year)
        if race is "president":
            races.extend(["popularVote","electoralVote"])
            continue

        if race is "congress" or race is "congress1" or race is "congress2":
            races.extend(["house","senate"])
            house=getWinningParty(election,"house")
            senate=getWinningParty(election,"senate")
            color1=colors[house]
            color2=colors[senate]
            color=getPartyColor(house,senate)
        else:
            party = getWinningParty(election,race)
            if party is "nobody":
                print("no winner for race",race,"in year",year)
            color = getPartyColor(party)


        ledIndex = getLEDIndex(display,race)
        remoteLED(ledIndex,color[0],color[1],color[2])

        if race is "electoralVote":
            ledIndex = getLEDIndex(display,"president")
            remoteLED(ledIndex,color[0],color[1],color[2])


def getPartyColor(*parties):
    global colors
    ourColors=[]
    consider=[]

    for party in parties:
        if type(party)==list:
            consider.extend(party)
        elif party not in consider:
            consider.extend([party])


    for party in consider:
        if party in colors.keys():
            ourColors.append(colors[party])
        else:
            print("party",party,"not found in color table")
    # print(ourColors)
    if (len(ourColors) > 1):
        print("multiple winners: ",consider)
        # print(ourColors)
        # print(averageColors(ourColors)[0])
        return averageColors(ourColors)
    return ourColors[0]

def getLEDIndex(display,race):
    if race is "governor1" or race is "governor2":
        race="governors"
    elif race is "congress1" or race is "congress2":
        race="congress"
    return leds[display][race]

def getWinningParty(election,race):
    if race is "president":
        race="popularVote"
    # print("checking race ",race," in ",election)
    winningVotes=0
    winner="nobody"
    multipleWinners=[]
    if race in election["votes"]:

        for party, count in election["votes"][race].items():
            if count > winningVotes:
                winningVotes=count
                winner=party
                multipleWinners=[]
            elif count==winningVotes:
                if(len(multipleWinners)==0):
                    multipleWinners=[winner]
                multipleWinners.extend([party])
    # print("winner is ",winner)
    if (len(multipleWinners) > 0) :
        return multipleWinners
    return winner

def averageColors(colors):
    if any(isinstance(el, list) for el in colors):
        return [sum(e)/len(colors) for e in zip(*colors)]
    return colors


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
if (os.path.exists("/dev/tty.SLAB_USBtoUART")):
    port = "/dev/tty.SLAB_USBtoUART"
# timeout=None,write_timeout=None
ser = serial.Serial(port,115200)
print(str(ser.get_settings()))
time.sleep(2)

def remoteWrite(*values):

    if DEBUG_Remote:
        print("-> " + formatRemoteValues(values))

    # while (ser.out_waiting):
    #     time.sleep(0.0001)
    theBytes = bytearray(values)
    # print(theBytes)

    # if DEBUG_Remote:
    #     print("waiting for flush", end="")
    # while (ser.out_waiting):
    #     sleep(0.0001)
    #     if DEBUG_Remote:
    #         print('.', end="")
    # if DEBUG_Remote:
    #     print(' ')

    written = 0
    for i in range(len(theBytes)):
        written = written + ser.write(bytearray([theBytes[i]]))
    if DEBUG_Remote:
        print("Wrote ",written, " bytes")
        print("This many bytes waiting: ",ser.out_waiting)

    # while (ser.out_waiting):
    #     sleep(0.0001)
    #     if DEBUG_Remote:
    #         print('.', end="")
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
    # ser.flush()
    if DEBUG_Remote:
        print(" ")
        print("waiting for response", end="")
    max = 0
    # sleep(0.01)
    while (ser.in_waiting is 0 and max < 2000):
        sleep(0.001)
        if DEBUG_Remote:
            print('.', end="")
        max = max + 1
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
        if DEBUG_Remote:
            print("LED updated")

    elif (command=='b'):
        values = getBytes(1)
        if DEBUG_LEDs:
            print("LED brightness now " + formatRemoteValues(values[0]))

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
    if (led > 19):
        red = int(red / 3)
        green = int(green / 3)
        blue = int(blue / 3)
    remoteWrite('l',chr(led),chr(red),chr(green),chr(blue))
    # time.sleep(0.001)

def remoteLEDBrightness(brightness):
    remoteWrite('b',chr(brightness))
    # time.sleep(0.001)

def remoteSevenSegment(screen, value):
    remoteWrite('#',chr(screen),str(int(value % 10000 / 1000)),str(int(value % 1000 /100)),str(int(value % 100 / 10)),str(int(value % 10)));


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
# remoteInitializePins()
doSensorCompensation()
processCompensations()
print(str(compensation))

# print(remoteAnalogRead(3))

for name, number in leds[0].items() :
    remoteLED(number,0,0,255)
for name, number in leds[1].items() :
    remoteLED(number,0,255,255)
for name, number in leds[2].items() :
    remoteLED(number,0,255,0)
for name, number in leds[3].items() :
    remoteLED(number,255,255,0)
for name, number in leds[4].items() :
    remoteLED(number,255,0,0)

# for name in leds[0].keys():
#     for index in range(0,5):
#         number = leds[index][name]
#         color = remoteLEDs[number]
#         remoteLED(number,color[0] / (index + 1 ),color[1] / (index + 1 ),color[2] / (index + 1 ))

changed = False

cycles = 1
for number in range(0,40):
    remoteLED(number,0,0,0)

for year, display in displayMappings.items() :
    remoteSevenSegment(display, year)


starttime=time.time()

while True:
    while ser.in_waiting:
        remoteRead()
    remoteAnalogRead(0)
    remoteAnalogRead(1)
    remoteAnalogRead(2)
    remoteAnalogRead(3)
    remoteAnalogRead(4)
    remoteAnalogRead(5)
    remoteAnalogRead(6)
    remoteAnalogRead(7)
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
        remoteAnalogPins[0]["changed"] = False
        sensorValues["voterAge"] = translate(remoteAnalogPins[0]["value"],0,1023,0,1)
        # print("pin A0 is now " + str(remoteAnalogPins[0]["value"]))
        print ("voter age raw value is now " + str(remoteAnalogPins[0]["value"]))
        changed=True

    if (remoteAnalogPins[1]["changed"] == True):
        remoteAnalogPins[1]["changed"] = False
        sensorValues["voterApathy"] = translate(remoteAnalogPins[1]["value"],0,1023,0,1)
        print("voter apathy raw value is now " + str(remoteAnalogPins[1]["value"]))
        changed=True

    if (remoteAnalogPins[2]["changed"] == True):
        remoteAnalogPins[2]["changed"] = False
        sensorValues["voterGender"] = translate(remoteAnalogPins[2]["value"],0,1023,0,1)
        print("voter gender raw value is now " + str(remoteAnalogPins[2]["value"]))
        changed=True

    if (remoteAnalogPins[3]["changed"] == True):
        remoteAnalogPins[3]["changed"] = False
        sensorValues["mediaBias"] = translate(remoteAnalogPins[3]["value"],0,1023,0,1)
        print("media bias raw value is now " + str(remoteAnalogPins[3]["value"]))
        changed=True

    if (remoteAnalogPins[4]["changed"] == True):
        remoteAnalogPins[4]["changed"] = False
        sensorValues["economyStrength"] = translate(remoteAnalogPins[4]["value"],0,1023,0,1)
        print("economy strength raw value is now " + str(remoteAnalogPins[4]["value"]))
        changed=True

    if (remoteAnalogPins[5]["changed"] == True):
        remoteAnalogPins[5]["changed"] = False
        sensorValues["politicalSpending"] = translate(remoteAnalogPins[5]["value"],0,1023,0,1)
        print("political spending raw value is now " + str(remoteAnalogPins[5]["value"]))
        changed=True

    if (remoteAnalogPins[6]["changed"] == True):
        remoteAnalogPins[6]["changed"] = False
        sensorValues["voterFraud"] = translate(remoteAnalogPins[6]["value"],0,1023,0,1)
        print("voter fraud raw value is now " + str(remoteAnalogPins[6]["value"]))
        changed=True

    if (remoteAnalogPins[7]["changed"] == True):
        remoteAnalogPins[7]["changed"] = False
        sensorValues["lies"] = translate(remoteAnalogPins[7]["value"],0,1023,0,1)
        print("lies raw value is now " + str(remoteAnalogPins[7]["value"]))
        changed=True

    if (changed):
        changed=False
        doSensorCompensation()
        print(compensations)
        processCompensations()
        print(compensation)
        for year in displayMappings.keys():
            if year is not 2016:
                generateElection(year)

            displayElection(year)



    while (DEBUG_LEDs):
        # remoteLEDBrightness(random.randint(0,255))
        for a in range(40):
            # color = [,random.randint(0,255),random.randint(0,255)]
            # print(str(a) + " to " + str(color))
            color = numpy.random.random_integers(0,255,3)
            # color = [ 255, 255, 255]
            remoteLED(a,color[0],color[1],color[2])
            # time.sleep(1/200)
        for a in range(5):
            remoteSevenSegment(a,random.randint(0,9999))
        elapsed = time.time() - starttime
        print("Frame ",cycles, ": Frames per second: ", cycles / elapsed)
        cycles += 1
    cycles += 1

    # time.sleep(2)
