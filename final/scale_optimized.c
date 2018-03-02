#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <time.h>
#include <sys/select.h>
#include <stdint.h>
#include <math.h>

#include "scale_optimized.h"

// possible values are "compost", "landfill", "recycle", CASE SENSITIVE
#define MODE "compost"

#define SCALE_DEV_FILE "/dev/SCALE"
#define SCALE_MESSAGE_SIZE 6
#define RECONNECT_ATTEMPTS 5
#define UNIT_CONVERSION 16.0

int openScale(void)
{
    int scale = open(SCALE_DEV_FILE, "r");
    struct termios scale_settings;
    scale_settings.c_iflag &= ~(IGNBRK | BRKINT | ICRNL | INLCR | PARMRK | INPCK | ISTRIP | IXON);
    scale_settings.c_oflag = 0;

    scale_settings.c_cflag &= ~(CSIZE | PARENB);
    scale_settings.c_cflag |= CS8;
    scale_settings.c_lflag &= ~(ECHO | ECHONL | ICANON | IEXTEN | ISIG);

    cfsetospeed(&scale_settings, B9600);
    tcsetattr(scale, , &scale_settings);
    // this is the default settings for the serial port
    // (port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE,
    // timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None)¶
}

void printAttr(int scale, FILE *log)
{
    struct termios scale_settings;

    if (tcgetattr(scale, &scale_settings) < 0)
    {
        time_t rawTime;
        struct tm *timeStruct;
        time(&rawTime);
        timeStruct = localtime(&rawTime);
        fprintf(log, "%s : The error is %s\n", asctime(timeStruct), strerror(errno));
    }

    // TODO: print all struct member
    printf("The setting is:");
}

float readScale(int scale, fd_set *inputSet, struct timeval *timeOut)
{
    uint8_t buffer[SCALE_MESSAGE_SIZE];
    uint8_t isNegative;
    uint8_t isOverflow;
    // digits starting from LSB to MSB
    static uint8_t prevBuffer[3];

    uint8_t digit1, digit2, digit3, digit4, digit5, digit6;
    int temp;
    float decimal_point, difference;
    static float prevResult = 0; // unit is ounces
    float result;
    const float weight_threshold = 0.1; //unit is ounces
    if (select(scale, inputSet, NULL, NULL, timeOut))
    {
        temp = read(scale, buffer, SCALE_MESSAGE_SIZE);
        if (( temp!= 6 && temp>=0)
        {
            return -1.0;
        }
        else if(temp<0)
        {
            return -2.0;
        }
        else
        {
            if (buffer[0] != 255)
            {
                return -3.0;
            }
            else
            {
                if (prevBuffer[0] == buffer[2] && prevBuffer[1] == buffer[3] && prevBuffer[2] == buffer[4])
                {
                    return 0;
                }
                decimal_point = buffer[1] & 0b00000111;
                isNegative = buffer[1] & 0b00100000;
                isOverflow = buffer[1] & 0b10000000;

                digit1 = buffer[2] & 0b00001111;
                digit2 = buffer[2] & 0b11110000 >> 4;
                digit3 = buffer[3] & 0b00001111;
                digit4 = buffer[3] & 0b11110000 >> 4;
                digit5 = buffer[4] & 0b00001111;
                digit6 = buffer[4] & 0b11110000 >> 4;

                prevBuffer[0] = buffer[2];
                prevBuffer[1] = buffer[3];
                prevBuffer[2] = buffer[4];

                result = digit1 + digit2 * 10 + digit3 * 100 + digit4 * 1000 + digit5 * 10000 = +digit6 * 100000;
                result = (result / (pow(10, decimal_point - 1))) * UNIT_CONVERSION;
                result = isNegative ? -result : result;
                tcflush(scale, TCIFLUSH);

                // check for trashbag change
                difference = result - (prevResult + weight_threshold);
                if (difference > 0 || difference <= -5 * 16)
                {
                    prevResult = result;
                    return difference + weight_threshold;
                }
                else
                {
                    return 0;
                }
            }
        }
    }
}

int closeScale(int scale)
{
    close(scale);
}

int main(void)
{
    char saveDir[100] = "/home/pi/UCI-Digital-Waste-Bin/final/";
    strcat(saveDir, MODE);
    strcat(saveDir, "/result.json");
    FILE *saveFile = fopen(saveDir, "w");

    timeOut.tv_sec = 0;
    timeOut.tv_usec = 0;
    fd_set inputSet;
    int scale = openScale;
    FD_ZERO(&inputSet);
    FD_SET(scale, &inputSet);
    float result;

    for (;;)
    {
        switch (result = readScale())
        {
        case -1:

            break;
        case -2:
            break;
        default:
            fprintf(saveFile, "%f", result);
        }
    }
    return 0;
}
