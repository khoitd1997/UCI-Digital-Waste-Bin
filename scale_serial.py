"""
scale.py

Description: [DESCRIPTION]

Created on Apr 25, 2017

Data Format: Every message includes 6 bytes;
    a. No. 1: D0-D7 = 0FFH (Message Flag)
    b. No. 2: D0-D2 = Decimal point (0-5)
        D3-D4 = Current mode: 00-Weight; 01-Count; 10-Percent
        D5 = 1 means weight is negative, otherwise positive
        D6 = 1 means weight is stable, otherwise unstable
        D7 = 1 means weight is overflow, otherwise normal
    c. No. 3: D0-D7 = BCD1 (LSB)
    d. No. 4: D0-D7 = BCD2 (MSB)
    e. No. 5: D0-D7 = BCD3 (HSB)


Bytes 3-5 to Digits
D2: 0001 D1: 0000
D4: 0000 D3: 0000
D6: 0000 D5: 0000

IMPORTANT: Assumptions made on the hardware
Assuming that the scale runs in STB mode(send when stable)
Assuming that the units are in lbs
"""
import threading
import serial
# import time
import collections
import sector_draw
import pygame
import time
Reading = collections.namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])
baud_rate = 9600  # scale supports 1200, 2400, 4800, 9600

white = (255, 255, 255)
black = (0, 0, 0)


# Commented out codes for threading

# class Scale_Thread(threading.Thread):
#     def __init__(self, screen, scale_lock: threading.RLock=None, text_box: sector_draw.text_surface=None, header: sector_draw.text_surface=None, header_text=None, im_list=None, top_rect_list=None, mid_rect_list=None, bot_rect_list=None, top_rect=None, mid_rect=None, bot_rect=None):
#         self._Scale = Scale()
#         super(Scale_Thread, self).__init__()
#         self.daemon = True
#         self._lock = scale_lock
#         self._text_bubble = text_box
#         self._header = header
#         self._screen = screen
#         self._header_text = header_text
#         self._im_list = im_list
#         self._top_rect_list = top_rect_list
#         self._mid_rect_list = mid_rect_list
#         self._bot_rect_list = bot_rect_list
#         self._top_rect = top_rect
#         self._mid_rect = mid_rect
#         self._bot_rect = bot_rect

#     def run(self):
#         weight = 0
#         while(True):
#             if self._Scale.ser.in_waiting >= 6:
#                 reading = self._Scale.ser.read(6)
#                 while((len(reading) != 6 or reading[0] != 0xff)):
#                     self._Scale.ser.close()
#                     self._Scale.ser.open()
#                     reading = self._Scale.ser.read(6)
#                 if not(reading[2] == self._Scale.raw[2] and reading[3] == self._Scale.raw[3] and reading[1] == self._Scale.raw[1] and reading[4] == self._Scale.raw[4]):
#                     weight = self._Scale.check(reading)
#                     if(weight):
#                         while(not(self._lock.acquire(blocking=False))):
#                             pygame.event.pump()
#                         self._screen.fill(white)
#                         pygame.event.pump()
#                         self._text_bubble.draw_text_surface(
#                             sector_draw.compost_text_processing(weight))
#                         pygame.event.pump()
#                         pygame.display.flip()
#                         pygame.event.pump()
#                         time.sleep(4)
#                         pygame.event.pump()
#                         self._screen.fill(white)
#                         self._header.draw_text_surface(self._header_text)
#                         pygame.display.flip()
#                         self._screen.fill(white, self._top_rect)
#                         self._screen.fill(white, self._mid_rect)
#                         self._screen.fill(white, self._bot_rect)
#                         pygame.display.flip()
#                         pygame.event.pump()
#                         self._screen.blit(
#                             self._im_list[0], self._top_rect_list[0])
#                         pygame.event.pump()
#                         self._screen.blit(
#                             self._im_list[1], self._mid_rect_list[1])
#                         pygame.event.pump()
#                         self._screen.blit(
#                             self._im_list[2], self._bot_rect_list[2])
#                         pygame.event.pump()
#                         pygame.event.pump()
#                         pygame.display.flip()
#                         pygame.event.pump()
#                         self._lock.release()

# scale class representing a scale

class Scale:
    def __init__(self) -> None:
        # create serial object using pyserial API
        self.ser = serial.Serial('/dev/SCALE', baud_rate)

        # safeguard, close port if not already closed
        if (self.ser.isOpen()):
            self.close()

        # open the port
        self.open()

        # last recorded stable value in lbs
        self.last_value = 0

        # last recorded raw value
        self.raw = [0, 0, 0, 0, 0, 0]

        # minimum increase in weight to be counted as increased
        self.weight_threshold = 0.006

        self.trashbag_replaced_counter = 0
    # function to process data, input is 6 bytes read from serial port
    # ie scale.ser.read(6), meaning of each byte described at the top

    def check(self, raw: bytes) -> Reading:
        # flush all unread inputs to avoid overloading the port
        # with too much data
        self.ser.reset_input_buffer()

        # # this is the preliminary quick check to make sure that the
        # # value did change from last time
        # if not(raw[2] == self.raw[2] and raw[3] == self.raw[3] and raw[1] == self.raw[1] and raw[4] == self.raw[4]):

        # save the raw value for comparison next time
        #self.raw = raw

        # scale data parsing starts here

        decimal_point = raw[1] & 0b111
        # current_mode = (raw[1] & 0b11000) >> 3
        negative = (raw[1] & 0b100000)

        # self.stable = (raw[1] & 0b1000000) >> 6
        # overflow = (raw[1] & 0b10000000) >> 7

        # TODO: Handle third byte
        digit1 = raw[2] & 0b1111
        digit2 = (raw[2] & 0b11110000) >> 4

        # TODO: Handle fourth byte
        digit3 = raw[3] & 0b1111
        digit4 = (raw[3] & 0b11110000) >> 4

        # TODO: Handle fifth byte
        digit5 = raw[4] & 0b1111
        digit6 = (raw[4] & 0b11110000) >> 4

        # calculate the total value from interpreted digits
        result = float(digit1) + digit2 * 10 + digit3 * 100 + \
            digit4 * 1000 + digit5 * 10000 + digit6 * 100000
        result /= float(10 ** (decimal_point - 1))  # more precision

        # Convert from lbs to ounce, which will be multiplied
        # with a conversion factor to determine the ounces of carbon
        # emission saved
        result = result * 16
        result = result * (-1.0) if negative else result

        # this is a check implemented to detect if the
        # trashbag has been replaced, if replaced
        # then reset the max value to zero
        if(self.last_value > 5 and result < 0.5):
            self.trashbag_replaced_counter += 1
            if self.trashbag_replaced_counter == 5:
                self.trashbag_replaced_counter = 0
                self.last_value = 0

        # if the current reading is bigger than last reading by a value
        # then output the difference
        if (self.last_value + self.weight_threshold) < result:

            difference = float(result) - float(self.last_value)
            self.last_value = result

            #self.raw = raw

            return difference  # return weight change between this and the last stable read in lbs

    def open(self) -> None:
        self.ser.open()

    def close(self) -> None:
        self.ser.close()


"""
if __name__ == '__main__':
    # Test the examples from Khoi's screenshot

    s = Scale()

    while(True):
        # 0:unusable, -1:error, others: difference in mass
        print(s.check(s.ser.read(6)))

    s.close()
"""
