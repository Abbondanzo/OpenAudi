import logging
import sys
import time
from enum import Enum

import keyboard
import serial


class Runner:
    def __init__(self, port: str):
        self.ser = serial.Serial(
            port=port,
            baudrate=9600,
            timeout=1,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
        )
        if self.ser.is_open:
            logging.info("Opened serial port {}".format(self.ser.port))

    def run(self):
        while 1:
            self.read()

    def read(self):
        bytes_to_read = self.ser.in_waiting
        data = self.ser.read(bytes_to_read)
        try:
            decoded_data = data.decode("ISO-8859-1")
            logging.debug("Received {}\n".format(decoded_data))
            Mappings.parse_and_execute(decoded_data)
            time.sleep(1)
        except UnicodeEncodeError as e:
            logging.error("Unable to decode: {}".format(e))
        except KeyboardInterrupt:
            logging.info("Closing connection")
            self.ser.close()
            sys.exit(0)


class KeyControls(Enum):
    ENTER = "enter"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    BACK = "esc"
    HOME = "h"
    PHONE = "p"
    CALL_END = "o"
    PLAY = "x"
    PAUSE = "c"
    PREVIOUS_TRACK = "v"
    NEXT_TRACK = "n"
    TOGGLE_PLAY = "b"
    VOICE = "m"
    WHEEL_LEFT = "1"
    WHEEL_RIGHT = "2"

    def press(self):
        logging.debug("Sending key control {}".format(self.name))
        keyboard.write(self.value)


class Mappings(Enum):
    WHEEL_LEFT = ("Qw", KeyControls.WHEEL_LEFT)
    WHEEL_RIGHT = ("Pv", KeyControls.WHEEL_RIGHT)
    WHEEL_ENTER = ("1W", KeyControls.ENTER)
    RETURN = ("1e", KeyControls.BACK)
    RETURN_LEFT = ("1\nb", KeyControls.PREVIOUS_TRACK)
    RETURN_RIGHT = ("1v", KeyControls.NEXT_TRACK)

    @staticmethod
    def parse_and_execute(data: str):
        i = 0
        while i < len(data):
            handled = False
            for mapping in Mappings:
                delimiter, control = mapping.value
                if data[i:].startswith(delimiter):
                    i += len(delimiter)
                    handled = True
                    control.press()
            if not handled:
                i += 1


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    runner = Runner("/dev/ttyAMA0")
    runner.run()
