import threading
from time import sleep

mutex = threading.Semaphore(1)
boarded = 0
boardQueue = threading.Semaphore(0)
unboardQueue = threading.Semaphore(0)
canEnterOrLeave = threading.Semaphore(0)
size = 5

class Passenger(threading.Thread):
    """docstring for Passenger"""
    def __init__(self, id):
        super(Passenger, self).__init__()
        self.id = id

    def run(self):
        global boarded
        global size
        boardQueue.acquire()
        self.board()
        
        mutex.acquire()
        boarded += 1
        if boarded == size:
            canEnterOrLeave.release()
        mutex.release()
        
        unboardQueue.acquire()
        self.unboard()
        
        mutex.acquire()
        boarded -= 1
        if boarded == 0:
            canEnterOrLeave.release()
        mutex.release()
        return 0

    def board(self):
        print("I'M GOING IN %d " % self.id)

    def unboard(self):
        print("SUCH RIDE, MUCH FUN, VERY SICK %d " % self.id)


class Car(threading.Thread):

    def __init__(self):
        super(Car, self).__init__()

    def run(self):
        while True:
            self.load()
            for x in range(0,size):
                boardQueue.release()
                sleep(1)

            canEnterOrLeave.acquire()
    
            self.allAboard()
            sleep(1)
            self.go()
            sleep(1)
            self.unload()
            sleep(1)

            for x in range(0,size):
                unboardQueue.release()
                sleep(1)
            canEnterOrLeave.acquire()

            self.allAshore()
    
    def allAboard(self):
        print("ALL ABOOAAAARDDD!")
    
    def allAshore(self):
        print("ALL ASHOREE!")
        
    def load(self):
        print("GET TO DA CHOPPA")
        pass

    def go(self):
        print("LET'S GO")

    def unload(self):
        print("GTFO")

size = int(input("Capacidade do carro: "))
car = Car()
car.daemon = True
car.start()
id = 1

while True:
    input("")
    x = Passenger(id)
    x.daemon = True
    x.start()
    id += 1