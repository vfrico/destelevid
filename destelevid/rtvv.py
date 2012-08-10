#!/usr/bin/python
# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2

class rtvv_mediateca:
    def __init__(self):
        None
        
    def getTextFromTag(self,txt): #Obtiene el texto cuando le das una etiqueta con texto dentro
        soup = BeautifulSoup(txt)
        return soup.get_text()

    def averiguarXml(self,url):
        htmlfile = urllib2.urlopen(url)
        archivohtml = htmlfile.read()
        soup = BeautifulSoup(archivohtml)
        javascript = soup.find_all('script')
        #~ return getTextFromTag(str(javascript))
        #~ return javascript    
        salida = self.getTextFromTag(str(javascript))
        #~ salida = averiguarXml('http://www.rtvv.es/es/comunidad-valenciana/Bars-cafeteries-mes-beneficiats-turisme_3_749355079.html')
        #~ print salida
        salida1 = salida.split('file:')[1]
        #~ print salida1
        salida2 = salida1.split('xml')[0]
        #~ print salida2
        archivofin = salida2.split('\"')[1]+'xml'
        return archivofin
    def descifrarUrl(self,url):
        url = 'http://www.rtvv.es'+self.averiguarXml(url)
        htmlfile = urllib2.urlopen(url)
        archivohtml = htmlfile.read()
        soup = BeautifulSoup(archivohtml)
        archivo = soup.find_all('media:content')
        archivoraw = str(archivo).split('url=\"')[1]
        video = archivoraw.split('"><')[0]
        return video
if __name__ == "__main__":
    print "Introduce la dirección del vídeo de rtvv.es/mediateca para descargar: "
    direccion = raw_input()
    print "La dirección del vídeo es: "
    print rtvv_mediateca().descifrarUrl(direccion)
