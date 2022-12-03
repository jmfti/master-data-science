#!/usr/bin/env python3
import sys

#Leemos cada linea de la entrada estandar
for line in sys.stdin:  
    #Dividimos en palabras cada linea
    words = line.split()  
    #Iteramos sobre cada palabra contenida en words
    for word in words:    
        #Escribimos por salida estandar el par <Clave,Valor>
        #En este caso la Clave será la palabra en cuestión y el valor será 1
        print(f"{word}\t1")
