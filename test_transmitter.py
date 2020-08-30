import logging
import os
import pty
import sys
from random import randrange

from open_audi import Runner


def send_data(fd, data):
    os.write(fd, bytearray(data, "ISO-8859-1"))


def generate_random_string() -> str:
    random_data = ["Qw", "Pv", "asdf", "1\nb", "1v", "1e"]
    # Generate 1 to 10 items in the string
    items = randrange(9) + 1
    string = ""
    for x in range(items):
        random_item_index = randrange(len(random_data) - 1)
        string += random_data[random_item_index]
    return string


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    master, slave = pty.openpty()
    runner = Runner(os.ttyname(slave))
    try:
        while 1:
            send_data(master, generate_random_string())
            runner.read()
    except KeyboardInterrupt:
        sys.exit(0)
