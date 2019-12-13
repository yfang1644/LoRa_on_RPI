#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>
#include <math.h>

#define	BAUDRATE B9600		// 9600 bps

#define	DEV	"/dev/ttyUSB0"


void readback(int fd)
{
    unsigned char d;
    char cnt, i;

    for(i = 0; i < 12; i++) {
        usleep(100000);
    	read(fd, &d, 1);
        printf("%02X\n", d);
    }
    printf("\n");
}

int main(int argc, char *argv[])
{
    int fd;
    int	i = 0;
    unsigned char snd[128];
    unsigned char d;
    unsigned char cnt;
    struct termios newtio;
    unsigned char *p;
    int a, b;

    fd=open(DEV, O_RDWR|O_NOCTTY|O_NDELAY);
    //fd=open(DEV, O_RDWR | O_NOCTTY);
    printf("%d\n",fd);
    if(fd<0){
    	printf("open error\n");
    	exit(0);
    }

    tcgetattr(fd, &newtio);
    //configure the serial port;
    cfsetspeed(&newtio, BAUDRATE);
    newtio.c_cflag &= ~CSIZE;    /* Mask the character size bits */
    newtio.c_cflag |= CS8;       /* Select 8 data bits */
    newtio.c_cflag &= ~PARENB;   /* Parity disabled */
    newtio.c_cflag &= ~CSTOPB;   /* Stop bit=1 */
    newtio.c_cflag &= ~CRTSCTS;  /* disable hardware flow control; */
    newtio.c_cflag |= CREAD|CLOCAL; /* Turn on the receiver */
    newtio.c_iflag &= ~(IXON|IXOFF|IXANY);  /* Turn off software flow control */
    newtio.c_iflag &= ~(ICANON|ECHO|ECHOE|ISIG)  ;/*raw input*/
    newtio.c_oflag &= ~OPOST; /*raw output*/
    newtio.c_cc[VTIME] = 0; /* inter-character timer unused */
    newtio.c_cc[VMIN] = 0; /* blocking read until 0 character arrives */

    tcsetattr(fd, TCSANOW, &newtio);
    tcflush(fd, TCIFLUSH);
    sleep(1);

    memcpy(snd, "\xc2\x00\x09\xff\xff\x00\x62\x00\x17\x03\x00\x00", 12);
    /* strncpy broken at \x00 */

    write(fd, snd, 12);
    fprintf(stderr, "info: ");
    sleep(1);
    readback(fd);

    close(fd);
}
