import random
import urllib2
from configobj import ConfigObj
from sys import argv
import logging


class rps():
    __cnt = 0
    __r = 33
    __p = 33
    __s = 34

    def setPercent(self, r, p, s):
        rps.__r = r
        rps.__p = p
        rps.__s = s
        logging.info("rock probabilities: "+str(rps.__r)+"%")
        logging.info("paper probabilities: "+str(rps.__p)+"%")
        logging.info("scissors probabilities: "+str(rps.__s)+"%")

    def randomrps(self):
        return (random.choice(['rock', 'paper', 'scissors']))

    def halfrandomrps(self):
        w = random.randint(0, 99)
        if(w < rps.__r):
            return ('rock')
        elif(w < rps.__r+rps.__p):
            return ('paper')
        else:
            return ('scissors')

    def norandomrps(self):
        if(rps.__cnt % 3 == 0):
            rps.__cnt += 1
            return ('rock')
        elif(rps.__cnt % 3 == 1):
            rps.__cnt += 1
            return ('paper')
        else:
            rps.__cnt += 1
            return ('scissors')

    def fakerandomrps(self, data):
        return (data)


class game():

    def online(self, id, mode):
        url = 'http://localhost:4441'
        data = rps().randomrps()
        while True:
            if (mode == 1):
                logging.info("game: halfrandomrps")
                usock = urllib2.urlopen('%s/%i/%s' % (url, id, rps().halfrandomrps()))
            elif (mode == 2):
                logging.info("game: norandomrps")
                usock = urllib2.urlopen('%s/%i/%s' % (url, id, rps().norandomrps()))
            elif (mode == 3):
                logging.info("game: fakerandomrps")
                usock = urllib2.urlopen('%s/%i/%s' % (url, id, rps().fakerandomrps(data)))
            else:
                logging.info("game: randomrps")
                usock = urllib2.urlopen('%s/%i/%s' % (url, id, rps().randomrps()))
            data = usock.read()
            usock.close()

    def offline(self, id, mode):
        print (id)
        data = rps().randomrps()
        while True:
            if (mode == 1):
                logging.info("game: halfrandomrps")
                ki = rps().halfrandomrps()
            elif (mode == 2):
                logging.info("game: norandomrps")
                ki = rps().norandomrps()
            elif (mode == 3):
                logging.info("game: fakerandomrps")
                ki = rps().fakerandomrps(data)
            else:
                logging.info("game: randomrps")
                ki = rps().randomrps()
            data = raw_input('rock,paper or scissors? ')
            print (ki)

if __name__ == '__main__':
    logging.basicConfig(filename = "rps.log", filemode = "a", level = logging.DEBUG, format = "%(asctime)s [%(levelname)-8s] %(message)s")
    config = ConfigObj('settings.ini')
    mode = int(config['config']['playingmode'])
    if(mode==1):
        rps().setPercent(int(config['halfrandom']['rock']), int(config['halfrandom']['paper']), int(config['halfrandom']['scissors']))
    if len(argv) == 2:
        logging.info("new game")
        logging.info("ID: "+argv[1])
        #game().offline(int(argv[1]), mode)
        game().online(int(argv[1]), mode)
    else:
        logging.error("no ID")
