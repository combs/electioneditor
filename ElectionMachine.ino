
#define PIN_LED_ARRAY 9
#define PIN_SWITCH_CLIMATE_CHANGE 5
#define PIN_SWITCH_RIGGED_ELECTION 6
#define PIN_LED_CLIMATE_CHANGE 7
#define PIN_LED_RIGGED_ELECTION 8
#define PIN_POT_VOTER_AGE A0
#define PIN_POT_VOTER_GENDER A1
#define PIN_POT_VOTER_APATHY A2
#define PIN_POT_MEDIA_BIAS A3 


SoftwareSerial remoteSender(4, 5, false, 256);

byte remoteDigitalPins[20] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

uint16_t remoteAnalogPins[20] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

byte remotePinModes[20] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

byte remoteDigitalPinChanges[20] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
byte remoteAnalogPinChanges[20] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

volatile long remoteEncoder = 0;

byte remotePinMode(byte pin, byte pinMode) {
  switch (pinMode) {
    case INPUT:
      remoteWrite('i', pin);
      remotePinModes[pin] = INPUT;
      break;

    case INPUT_PULLUP:
      remoteWrite('I', pin);
      remotePinModes[pin] = INPUT_PULLUP;

      break;

    case OUTPUT:
      remoteWrite('o', pin);
      remotePinModes[pin] = OUTPUT;

      break;

    default:
      break;

  }
  yield();
  remoteDigitalPins[pin] = 0;

}
byte remotePinMonitoring(byte pin) {
  remoteWrite('M', pin);
}

byte remotePinStopMonitoring(byte pin) {
  remoteWrite('m', pin);

}

byte remoteDigitalRead(byte pin) {
  remoteWrite('r', pin);
  while (!remoteSender.available()) {
    delayMicroseconds(125);
  }
  while (remoteSender.available()) {
    remoteRead();
  }
  return remoteDigitalPins[pin];
}

byte remoteDigitalWrite(byte pin, byte value) {
  remoteWrite('w', pin, value);
  remoteDigitalPins[pin] = value;
  // remoteSender.flush();
}

byte remoteAnalogWrite(byte pin, byte value) {
  remoteWrite('W', pin, value);
  remoteDigitalPins[pin] = value;
  // remoteSender.flush();
}



byte remoteDigitalPinChanged(byte pin) {
  if (remoteDigitalPinChanges[pin]) {
    remoteDigitalPinChanges[pin] = 0;
    return true;
  }
  return false;
}



void remoteWrite(byte command, byte pin, byte value, byte value2) {
  Serial.print("->");

  remoteSender.write(command);
  remoteSender.write(pin);
  remoteSender.write(value);
  remoteSender.write(value2);
  Serial.write(command);
  Serial.write(pin);
  Serial.print(" (");
  Serial.write(pin + 48);
  Serial.write(") ");
  Serial.write(value);
  Serial.print(" (");
  Serial.write(value + 48);
  Serial.write(") ");
  Serial.write(value2);
  Serial.print(" (");
  Serial.write(value2 + 48);
  Serial.write(") ");

  Serial.write('\n');
  // remoteSender.flush();

  waitForRemoteSerial();

  while (remoteSender.available()) {
    remoteRead();
  }

  // Serial.flush();
  yield();


}


void remoteWrite(byte command, byte pin, byte value) {

  remoteSender.write(command);
  remoteSender.write(pin);
  remoteSender.write(value);
  if (pin != PIN_ACCESS) {
    Serial.print("->");

    Serial.write(command);
    Serial.write(pin);
    Serial.print(" (");
    Serial.write(pin + 48);
    Serial.write(") ");
    Serial.write(value);
    Serial.print(" (");
    Serial.write(value + 48);
    Serial.write(") ");


    Serial.write('\n');

  }

  waitForRemoteSerial();

  while (remoteSender.available()) {
    remoteRead();
  }

  // Serial.flush();
  yield();

}

void remoteWrite(byte command, byte pin) {
  Serial.print("->");

  remoteSender.write(command);
  remoteSender.write(pin);
  Serial.write(command);

  Serial.write(pin);
  Serial.print(" (");
  Serial.write(pin + 48);
  Serial.write(") ");
  Serial.write('\n');

  waitForRemoteSerial();

  while (remoteSender.available()) {
    remoteRead();
  }

  // Serial.flush();
  yield();
}


void remoteWrite(byte command) {
  Serial.print("->");
  remoteSender.write(command);
  Serial.write(command);
  Serial.write('\n');

  waitForRemoteSerial();

  while (remoteSender.available()) {
    remoteRead();
  }

  // Serial.flush();
  yield();
}

void waitForRemoteSerial() {
  uint8_t a = 0;
  while (a < 10) {
    if (!remoteSender.available()) {
      a++;
      delayMicroseconds(500);
    } else {
      return;
    }
  }
}

void remoteInitializePins() {

  remotePinMode(PIN_SWITCH_CLIMATE_CHANGE, INPUT_PULLUP);
  remotePinMode(PIN_SWITCH_RIGGED_ELECTION, INPUT_PULLUP);
  remotePinMode(PIN_LED_CLIMATE_CHANGE, OUTPUT);
  remotePinMode(PIN_LED_RIGGED_ELECTION, OUTPUT);
  
  #define PIN_POT_VOTER_AGE A0
  #define PIN_POT_VOTER_GENDER A1
  #define PIN_POT_VOTER_APATHY A2
  #define PIN_POT_MEDIA_BIAS A3 


  for (uint8_t a = 0; a < 19; a++) {
    if (remotePinModes[a]) {
      remotePinMode(a, remotePinModes[a]);
    }
    if (remoteDigitalPins[a] == 1) {
      remoteDigitalWrite(a, remoteDigitalPins[a]);
    } else if ( remoteDigitalPins[a] > 0 ) {
      remoteAnalogWrite(a, remoteDigitalPins[a]);
    }
    
  Serial.print("file 6 is ");
  Serial.println(filenames[6]);
  
  }

  
  Serial.print("file 6 is ");
  Serial.println(filenames[6]);
  remotePinMode(PIN_DESTROYBUTTON, INPUT_PULLUP);
  //
  //
  //  remotePinMode(PIN_MOTOR, OUTPUT);
  remotePinMode(PIN_READY, OUTPUT);
  //  remoteDigitalWrite(PIN_READY, HIGH);
  //
  //  remotePinMode(PIN_MOTOR, OUTPUT);
  //  remotePinMode(PIN_DESTROYBUTTONGLOW, OUTPUT);
  remoteAnalogWrite(PIN_DESTROYBUTTONGLOW, 63);
  remotePinMonitoring(PIN_DESTROYBUTTON);
  remoteDigitalWrite(PIN_ACCESS, LOW);

  Serial.print("file 6 is ");
  Serial.println(filenames[6]);
  //
  //  remoteWrite('?');
  //  while (remoteSender.available()) {
  //    remoteRead();
  //  }
  //
  //  remoteWrite('*');
  //
  //  while (remoteSender.available()) {
  //    remoteRead();
  //  }


  //  remoteDigitalWrite(PIN_MOTOR, HIGH);
  //  delay(500);
  //  remoteDigitalWrite(PIN_MOTOR, LOW);
  //  delay(50);
  //
  ////  remoteDigitalWrite(PIN_DESTROYBUTTONGLOW, HIGH);
  ////  delay(250);
  //  remoteDigitalWrite(PIN_DESTROYBUTTONGLOW, LOW);
  //  delay(50);
  //
  //  remoteDigitalWrite(PIN_READY, HIGH);
  //  delay(500);
  ////  remoteDigitalWrite(PIN_READY, LOW);
  //
  //  remoteWrite('?');
  //  delay(50);


}


void remoteRead() {

  if (!remoteSender.available() ) {
    return;
  }
  char command = remoteSender.read();
  byte pin;
  byte value = 0;
  byte value2 = 0;
  uint16_t analogValue = 0;

  switch (command) {
    case '!':
      remoteInitializePins();
      break;

    case '\n':
    case '\r':
      break;
    case 0:
      waitForRemoteSerial();
      pin = remoteSender.read();
      if (pin == '!') {
        remoteInitializePins();

      }

    case 'X':
      waitForRemoteSerial();
      pin = remoteSender.read();
      waitForRemoteSerial();
      value = remoteSender.read();

      break;
    case 'm':
    case 'M':
      waitForRemoteSerial();
      pin = remoteSender.read();
      break;
    case 'P':
      waitForRemoteSerial();
      pin = remoteSender.read();
      waitForRemoteSerial();
      value = remoteSender.read();
      break;

    case 'd':
      waitForRemoteSerial();
      pin = remoteSender.read();
      waitForRemoteSerial();
      value = remoteSender.read();
      if (remoteDigitalPins[pin] != value) {
        remoteDigitalPins[pin] = value;
        remoteDigitalPinChanges[pin] = 1;
      }
      /*
            tft.print("D");
            tft.print(pin);
            tft.print(" is ");
            tft.println(value);*/

      break;
    case 'E':
      waitForRemoteSerial();
      value = remoteSender.read();
      if (value < 25) {
        remoteEncoder += value;
      }
      break;

    case 'e':
      waitForRemoteSerial();
      value = remoteSender.read();
      if (value < 25) {
        remoteEncoder -= value;
      }

      break;

    case 'a':
      waitForRemoteSerial();
      pin = remoteSender.read();
      waitForRemoteSerial();
      value = remoteSender.read();
      waitForRemoteSerial();
      value2 = remoteSender.read();
      analogValue = (value2 << 8) + value;
      if (remoteAnalogPins[pin] != analogValue) {
        remoteAnalogPins[pin] = analogValue;
        remoteAnalogPinChanges[pin] = 1;
      }

      //      tft.print("A");
      //      tft.print(pin);
      //      tft.print(" is ");
      //      tft.println(analogValue);

      break;


    default:
      //      tft.print("?: ");
      //      tft.println(command);

      break;



  }
  if (pin != PIN_ACCESS) {
    Serial.print("<-");

    Serial.write(command);
    Serial.print(" (");
    Serial.write(command + 48);
    Serial.write(") ");
    Serial.write(pin);
    Serial.print(" (");
    Serial.write(pin + 48);
    Serial.write(") ");
    Serial.write(value);
    Serial.print(" (");
    Serial.write(value + 48);
    Serial.write(") ");
    Serial.write(value2);
    Serial.print(" (");
    Serial.write(value2 + 48);
    Serial.write(") ");
    Serial.write(analogValue);
    Serial.write('\n');
  }

}


byte isEncoderButtonPressed() {
  if (remoteDigitalPinChanged(2)) {
    return !remoteDigitalPins[2];
  }
  return false;
}

byte isDestroyButtonPressed() {
  if (remoteDigitalPinChanged(5)) {
    return !remoteDigitalPins[5];
  }
  return false;
}


void setup() {
  remoteSender.begin(115200);



}

void loop() {
  // put your main code here, to run repeatedly:

}
