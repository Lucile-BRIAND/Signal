import sounddevice as sd
import soundfile as sf
from pylab import * 
from numpy import *                     # Import de numpy
from scipy.signal import *    # Import du module signal de scipy
from numpy.fft import *
from spicy import *


import socket

huff = {'10': 'e', '000': 'K', '001': 'a', '010': 'c', '011': 'p', '110': 's', '1110': '1', '1111': '7'}
"""
HOST = '192.168.43.148'  # Standard loopback interface address (localhost)
PORT = 33000        # Port to listen on (non-privileged ports are > 1023)
r = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while r:
            
            data = conn.recv(1024)
            data = data.decode()
            print(data)
            if data == "fichier":
                while r:
                    data = s.recv(1024)
                    if data == "fin":
                        r = 0
                        break
            val = input("Envoyez votre message : ").encode()
            conn.sendall(val)

            if val.decode() == "exit":
                break
            if not data:
                break
"""
"""
Client
"""




Fe = 44100

temp = 0

S = []

message = "1100111100100101"

def ajout1(S,temp):
    f1 = 1
    Fe = 44100
    t = arange(temp,temp+1,1/Fe)
    f1 = 2*sin(2*np.pi*f1*t)
    for i in f1:
        S.append(i)
    temp += 1
    return S,temp

def ajout0(S,temp):
    f2 = 500
    Fe = 44100
    t = arange(temp,temp+1,1/Fe)
    f2 = 2*sin(2*np.pi*f2*t)
    for i in f2:
        S.append(i)
    temp += 1
    return S,temp


for i in message:
    if i == "1":
        S,temp = ajout1(S,temp)
    elif i == "0":
        S,temp = ajout0(S,temp)


t = arange(0,temp,1/Fe)
fm = 2*sin(2*np.pi*20000*t)   
S = S * fm 

sd.play(S,44100)

plt.plot(t,S)                     # Affichage via la fonction plot de Matplotlib
plt.xlabel('En focntion du temps')        # Définition de l'axe des abscisses
plt.ylabel('Module')                # Définition de l'axe des ordonnées

plt.grid()
plt.title ('Module de la Transformée de Fourier du signal S=S1xS2',fontsize=14)
show()  




"""
Serveur
"""


def testdajout1(temps):
    S = []
    f1 = 1
    Fe = 44100
    t = arange(temps,temps+1,1/Fe)
    f1 = 2*sin(2*np.pi*f1*t)
    for i in f1:
        S.append(i)
    t = arange(temps,temps+1,1/Fe)
    fm = 2*sin(2*np.pi*20000*t)  
    A = fm * S
    return A


def testdajout0(temps):
    S = []
    f1 = 500
    Fe = 44100
    t = arange(temps,temps+1,1/Fe)
    f2 = 2*sin(2*np.pi*f1*t)
    for i in f2:
        S.append(i)
    t = arange(temps,temps+1,1/Fe)
    fm = 2*sin(2*np.pi*20000*t)  
    A = fm * S
    return A

star = 0
end = 50
pas = 44100
temps = 0
attempt = 0

message =""
while 1:
    i = 1
    val = S[star:end]
    A = testdajout1(temps)
    B = testdajout0(temps)
    vall = B[star - pas * attempt:end - pas * attempt]
    value = A[star - pas * attempt:end - pas * attempt]
    change = 0
    test1 = 0
    test0 = 0
    try:
        if val[1] == "":
            break
    except:
        break
    
    print(val)

    while change < end:
        if val[change] == A[change]:
            test0 = 0
        else:
            test0 = 1
            message += "0"
            break
        if val[change] == B[change]:
            test1 = 0
        else: 
            test1 = 1
            message += "1"
            break
        change += 1


    print(value)
    if test1:
        print('1')
    elif test0:
        print("0")
    else:
        break
    print(attempt)
   
    star += pas
    end += pas
    attempt += 1
    temps += 1
    print(message)


def verifintegrite(chaine):
    chaineencours=''
    chainedef=''
    b=8
    a=0
    parite=0
    e=0
    d=8

    #verification du nombre d'octets
    g=len(chaine)%8
    if g == 0:
        print("everything is alright")
    else:
        print("houston we have a problem")
    print("taille initiale :")   
    print(len(chaine))
    print("vérification des octets :")
    for x in chaine:
        #création d'un octets a partir de du paquet
        for val in range(0,int(len(chaine))-1):
            if a<len(chaine):
                if a<b:
                    chaineencours = chaineencours + chaine[val+e*d]
                    a+=1
                else:
                    break
                        
        #vérification du nombre de bit a l'etat logique haut
        for c in chaineencours:
            if c == "1":
                parite = parite + 1
        parite= parite%2 
        if parite ==  0:         
            print("false")
            parite=0
        else: 
            print("true")
            parite=0
        chainedef=chainedef + chaineencours[0:7]
        
        chaineencours=''
        e +=1
        b +=8  
        if a==len(chaine):
            print("taille finale :")
            print(len(chainedef))
            print("chaine finale :")
            print(chainedef)
            
            return chainedef
#def recuperation():

message = verifintegrite(message)




#DECOMPRESSION AVEC DECODAGE D'HUFFMAN
def decode(dictionary, text) :
	result = ""
	while text :
		for k in dictionary :
			print(k)
			if text.startswith(k) :
				result += dictionary[k]
				text = text[len(k):]
	return result

msg_decode = decode(huff,message)
print(msg_decode)