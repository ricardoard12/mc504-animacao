import threading
import os
from time import sleep

mutex = threading.Semaphore(1)
id = 0
boarded = 0
posCarrinho = 0
cheio = 0;
wildride = ''
boardQueue = threading.Semaphore(0)
unboardQueue = threading.Semaphore(0)
canEnterOrLeave = threading.Semaphore(0)
vez = [0]

def animation(movCarrinho, passageiro, op):
	global id
	global vez
	global boarded
	global posCarrinho
	global cheio
	restr = '';
	for k in reversed(range(0,len(vez))):
		if (op == 1 and k == 0):
			continue
		restr+= '(p'+str(vez[k])+')'
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
    backForMore = False
	
    def __init__(self, id):
        super(Passenger, self).__init__()
        self.id = id

    def run(self):
        global wildride
        while True:
            if self.backForMore:
                 vez.append(self.id)
            self.board()
            self.unboard()
            if (wildride == 'N' or wildride == 'n'):
                 break
            self.backForMore = True
        return 0

    def board(self):
        global boarded
        global size
        global vez
        boardQueue.acquire()
        while vez[0] != self.id:
             sleep(1/100000.0)
        mutex.acquire()
        sleep(1)
        boarded += 1
        animation(0,self.id,1)
        if boarded == size:
            canEnterOrLeave.release()
        vez.pop(0)
        mutex.release()

    def unboard(self):
        global boarded
        global size
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
wildride = input("Passageiros retornam para a fila depois de sair do brinquedo?(S/N) ")

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
	
vez.pop(0)
car = Car()
car.daemon = True
car.start()

while True:
    input("")
    id+= 1
    vez.append(id)
    animation(0,-1,0)
    x = Passenger(id)
    x.daemon = True
    x.start()