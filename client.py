import sounddevice as sd
import soundfile as sf
from pylab import * 
from numpy import *                     # Import de numpy
from scipy.signal import *    # Import du module signal de scipy
from numpy.fft import *
from spicy import *
import struct
import socket
from heapq import heappush, heappop, heapify
from collections import defaultdict

huff =dict()

adress = ""
port1 = 0
freq = 0

f = open("config.txt","r")
files = f.readlines()

def config() :
    par1 = "ip"
    par2 = "port"
    par3 = "frequence"
    i = 0
    f = open("config.txt", "r")
    c = f.readlines()
    print(c)
    for line in c :
        if par1 in line :
            adress = c[i].split(":") 
            adress = adress[1]
            adress = adress.split("\n")
            adress = adress[0]
            #print(adress)
        elif par2 in line :
            port1 = c[i].split(":") 
            port1 = port1[1]
            port1 = port1.split("\n")
            port1 = port1[0]
            #print(port1)
        elif par3 in line :
            freq = c[i].split(":") 
            freq = freq[1]
            freq = freq.split("\n")
            freq = freq[0]
            #print(freq)
        i += 1
    f.close()
    return adress,port1,freq

adress,port1,freq = config()

PORT = int(port1)
print("test")
print(PORT)
HOST = str(adress)




huff = dict()
#COMPRESSION AVEC CODAGE D'HUFFMAN
def encode(symbfreq) :		#Encode les symboles selon leur poids
    heap = [[wt, [sym, ""]] for sym, wt in symbfreq.items()]
    heapify(heap)
    while len(heap) > 1 :
        lo = heappop(heap)			#Retire valeur
        hi = heappop(heap)			#Retire valeur
        for pair in lo[1:] :
            pair[1] = '0' + pair[1]
        for pair in hi[1:] :
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])		#Ajoute valeur
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


txt = input("Entrez votre message : ")
symbfreq = defaultdict(int)
code = ""

for ch in txt :			#Calcule l'occurrence de chaque caractère
    symbfreq[ch] += 1
huffman = encode(symbfreq)

print("Symbole\tPoids\tCode")
for p in huffman :
	print("%s\t%s\t%s" % (p[0], symbfreq[p[0]], p[1]))		#Affiche le code de chaque caractère
	huff[p[1]] = p[0]
for ch in txt :
	for p in huffman :
		if ch == p[0] :
			code += str("%s" % (p[1]))
print(code)
print(huff)


message = code
def integrite(message):
    chaine=message #chaine de base
    chainef=''           #chaine definitive
    chaineencours= '' #chaine de transition
    parite = 0
    a = 7
    b = 0
    c = 0
    d = 7
    e = 0
    x= 0    
    g=int(len(chaine))%7
    print(g)
    for var in range(0,g):
        chaine= chaine + '0'
        g=int(len(chaine))%7      
    for x in chaine:
        #vérifié que le programme ne dépasse pas le nombre de bit maximal
        if a>len(chaine):
            print("voici votre chaine finale")
            #print(chainef)
            return chainef
        #création de la chaine de caractere nous permettant de compter seulement 7 bits afin de créé un octet avec le bit de parite
        for val in range(0,int(len(chaine))-1):
            if b < a:
                chaineencours = chaineencours + chaine[val+d*e]
                b += 1
            else :
                break
        #calcul du nombre de 1 dans l'octet
        for c in chaineencours:
            if c == "1":
                parite = parite + 1 
        
        #ajout d'un bit de parité afin de rendre le nombre de 1 impair peut importe la situation
        if parite ==  0 or parite == 2 or parite == 4 or parite == 6:
            chainef = chainef + chaineencours + "1" +""
            chaineencours = ''
            parite = 0
        else: 
            chainef = chainef +chaineencours + "0"+ ""    
            chaineencours = ''
            parite = 0
        a = a + 7
        e +=1  
        

        
message = integrite(message)
print(message)




Fe = 44100

temp = 0

S = []



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
plt.xlabel('En fonction du temps')        # Définition de l'axe des abscisses
plt.ylabel('Module')                # Définition de l'axe des ordonnées

plt.grid()
plt.title ('Module de la Transformée de Fourier du signal S=S1xS2',fontsize=14)
show()  



f,FFT = periodogram(S,Fe)
# On définit une variable qui reçoit le signal filtré de la même taille que la transformée de Fourier(FFT)
FFT_filtre = FFT



plt.plot(f,FFT)                     # Affichage via la fonction plot de Matplotlib
plt.xlabel('Fréquence (Hz)')        # Définition de l'axe des abscisses
plt.ylabel('Module')                # Définition de l'axe des ordonnées
plt.xlim(0, 22000)
plt.grid()
plt.title ('Module de la Transformée de Fourier du signal S=S1xS2',fontsize=14)
show()  



r = 1
S = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while 1:
        val = input("Envoyez un message : ").encode()
        exi = "exit".encode()
        s.sendall(val)
        if val.decode() == "fichier":
            while r:
                data = s.recv(1024).decode()
                if data == "fin":
                    break
                S.append(float64(data))
        data = s.recv(1024)
        data = data.decode()
        
        if len(data) == 1000:
            break
        