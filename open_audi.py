import logging
import sys
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
            bytes_to_read = self.ser.in_waiting
            data = self.ser.read(bytes_to_read)
            try:
                decoded_data = data.decode("ISO-8859-1")
                Mappings.parse_and_execute(decoded_data)
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
        print(self)
        keyboard.write(self)


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
            for mapping in Mappings:
                if data[i:].startswith(mapping[0]):
                    i += len(mapping[0])
                    mapping[1].press()


if __name__ == "__main__":
    runner = Runner("/dev/ttyAMA0")
    runner.run()
