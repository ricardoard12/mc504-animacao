import threading
import os
from time import sleep

mutex = threading.Semaphore(1)
mutexCreate = threading.Semaphore(1)
id = 0
boarded = 0
totalBoarded = 0
posCarrinho = 0
cheio = 0;
boardQueue = threading.Semaphore(0)
unboardQueue = threading.Semaphore(0)
canEnterOrLeave = threading.Semaphore(0)

def animation(movCarrinho, passageiro, op):
	global id
	global totalBoarded
	global boarded
	global posCarrinho
	global cheio
	restr = '';
	for k in range(id,totalBoarded,-1):
		restr+= '(p'+str(k)+')'
	restr+= '||'

	if movCarrinho != 0:
		posCarrinho+= movCarrinho
	
	for j in range(0,posCarrinho):
		restr+= ' '
	
	carrinho = 'C:'+str(boarded)
	if cheio == 1:
		carrinho = 'MAX'
		
	restr+= '[['+carrinho+']]'
	
	if op == 1:
		restr+= ' <-- (p'+str(passageiro)+')'
	if op == -1:
		restr+= ' --> (p'+str(passageiro)+')'
	
	print (restr)
		
class Passenger(threading.Thread):
    """docstring for Passenger"""
    def __init__(self, id):
        super(Passenger, self).__init__()
        self.id = id

    def run(self):
        animation(0,-1,0)
        mutexCreate.release()
        self.board()
        self.unboard()
        return 0

    def board(self):
        global boarded
        global size
        global totalBoarded
        boardQueue.acquire()
        mutex.acquire()
        sleep(1)
        boarded += 1
        totalBoarded += 1
        animation(0,self.id,1)
        if boarded == size:
            canEnterOrLeave.release()
        mutex.release()

    def unboard(self):
        global boarded
        global size
        global totalBoarded
        unboardQueue.acquire()
        mutex.acquire()
        boarded -= 1
        animation(0,self.id,-1)
        if boarded == 0:
            canEnterOrLeave.release()
        mutex.release()


class Car(threading.Thread):
	
    def __init__(self):
        super(Car, self).__init__()

    def run(self):
        global cheio
        while True:
            
            self.load()
			
            sleep(1)
            cheio = 1 
            animation(0,-1,0)
            sleep(1)
            
            self.go()

            sleep(1)
            cheio = 0
			
            self.unload()

    def load(self):
        for x in range(0,size):
            boardQueue.release()
        canEnterOrLeave.acquire()

    def go(self):
        for x in range(1,11):
            animation(1,-1,0)
            sleep(1/5.0)
        for x in range(1,11):
            animation(-1,-1,0)
            sleep(1/5.0)

    def unload(self):
        for x in range(0,size):
            unboardQueue.release()
            sleep(1)
        canEnterOrLeave.acquire()


os.system('cls' if os.name == 'nt' else 'clear')		
print("Desafio da Montanha Russa\n")
print("Desenvolvido por:")
print("Gustavo de Mello Crivelli  - RA 136008")
print("Vinicius Andrade Frederico - RA 139223\n")
print("Use ENTER para adicionar passageiros, CTRL+C para sair.")
size = int(input("Capacidade do carro: "))

#Easter egg
if size == 1987:
	print("                       ______")
	print("                     <((((((\\\\\\\\")
	print("                     /      . }\\")
	print("                     ;--..--._|}")
	print("  (\\                 '--/\--'  )")
	print("   \\\\                | '-'  :'|")
	print("    \\\\               . -==- .-|")
	print("     \\\\               \.__.'   \\--._")
	print("     [\\\\          __.--|       //  _/'--.")
	print("     \\ \\\\       .'-._ ('-----'/ __/      \\")
	print("      \\ \\\\     /   __>|      | '--.       |")
	print("       \\ \\\\   |   \\   |     /    /       /")
	print("        \\ '\\ /     \\  |     |  _/       /")
	print("         \\  \\       \\ |     | /        /")
	print("          \\  \\      \\        /")
	print("GET TO DA CHOPPA!!!")

car = Car()
car.daemon = True
car.start()

while True:
    mutexCreate.acquire()
    input("")
    id+= 1
    x = Passenger(id)
    x.daemon = True
    x.start()