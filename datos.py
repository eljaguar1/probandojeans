from utils import sizeof_fmt
import datetime
import time
import os
import asyncio


def text_progres(index,max):
	try:
		if max<1:
			max += 1
		porcent = index / max
		porcent *= 100
		porcent = round(porcent)
		make_text = ''
		index_make = 1
		make_text += ''
		while(index_make<20):
			if porcent >= index_make * 5: make_text+= '█'
			else: make_text+= '░'
			index_make+=1
		make_text += ''
		return make_text
	except Exception as ex:
			return ''

def porcent(index,max):
    porcent = index / max
    porcent *= 100
    porcent = round(porcent)
    return porcent

def descarga(filename,totalBits,currentBits,speed):

    msg = '📥Descargando... \n\n'
    msg+= '🔖Nombre: ' + str(filename)+'\n'
    msg+= '🗂Total: ' + str(sizeof_fmt(totalBits))+'\n'
    msg+= '🗂Descargado: ' + str(sizeof_fmt(currentBits))+'\n'
    msg+= '📶Velocidad: ' + str(sizeof_fmt(speed))+'/s\n'

    msg = '》| Descargando....\n\n'
    msg += '》| Archivo: '+filename+'\n'
    msg += text_progres(currentBits,totalBits)+' '+str(porcent(currentBits,totalBits))+'%\n'
    msg += '》| Total: '+sizeof_fmt(totalBits)+' - '+sizeof_fmt(currentBits)+'\n'
    msg += '》| Velocidad: '+sizeof_fmt(speed)+'/s\n\n'


def cromprimiendo(filename,filesize,splitsize):
    msg = '》| Comprimiendo... \n\n'
    msg+= '》| Nombre: ' + str(filename)+'\n'
    msg+= '》| Tamaño Total: ' + str(sizeof_fmt(filesize))+'\n'
    msg+= '》| Cantidad Partes: ' + str(round(int(filesize/splitsize)+1,1))+' - '+ str(sizeof_fmt(splitsize))+'\n\n'
    return msg