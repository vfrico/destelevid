#!/usr/bin/python
# -*- coding:utf-8 -*-
#
#    Returns url of a video in RTVE.es/alacarta
#    Copyright (C) 2012 - Víctor Fernández Rico
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  

import urllib2
from bs4 import BeautifulSoup

class rtvees_alacarta():
    def __init__(self):
        None
        
    def parseRtveUrl(self,url): #EL id tiene 7 números
        """Obtiene el id a través de una dirección"""
        url_L = list(url)[-8:] #cogemos los 8 últimos caracteres
        url_L = url_L[:7] #cogemos los 7 primeros para quitar la barra que hay al final
        idExit = ''
        for x in url_L:
            idExit = idExit+x #convertimos en una cadena
        #~ print url_L
        return idExit

    def parseRtveUrl_2(self,url): #Falla
        """Obtiene el id a través de una dirección. Método alternativo"""
        listasplit = url.split('/') #Obtenemos una lista con todos los elementos que estén separados por '/'
        if listasplit[-1:] == [u'']: #Si el último elemento está vacío
            "Tiene una barra al final"  #cogemos el penúltimo elemento, quitamos el último
            idEx = str(listasplit[-2:-1][0]) #Devuelve una lista, cogemos el elemento 0
        else:
            "No tiene una barra al final" #cogemos el último elemento
            idEx = str(listasplit[-1:][0]) #Devuelve una lista, cogemos el elemento 0
        return idEx
        
    def getTextFromTag(self,txt): 
        """Obtiene el texto cuando le das una etiqueta con texto dentro"""
        soup = BeautifulSoup(txt)
        return soup.get_text()
        
    def getAssetDataId(self,idVideo): 
        """Obtienen el Asset Data de un vídeo cuando le das el id"""
        urlIdAsset = "http://www.rtve.es/ztnr/?idasset=%s" % idVideo
        #~ print idVideo
        htmlfile = urllib2.urlopen(urlIdAsset) #abre el html
        #~ print htmlfile.read()
        archivohtml = htmlfile.read()
        soup = BeautifulSoup(archivohtml)
        #~ print archivohtml
        #~ print "/n/n/n/n"+str(soup.find_all('td'))+"/n/n/n/n"
        id0_raw = str(soup.find_all('td')[3]) #El AssetData (de alta calidad) se encuentra en el 4º elemento de todos los elementos 'td' que hay en el documento html
        #~ newid0 = BeautifulSoup(id0_raw) 
        #~ id0 = int(newid0.get_text())
        #~ print id0;
        return self.getTextFromTag(id0_raw)
        
    def getLinkVideo(self,assetData): 
        """Obtiene el link final de un vídeo"""
        urlPreset = "http://www.rtve.es/ztnr/preset.jsp?idpreset=%s&lenguaje=es&tipo=video" % assetData
        htmlfile = urllib2.urlopen(urlPreset) #abre el html
        archivohtml = htmlfile.read()
        soup = BeautifulSoup(archivohtml)
        fileName_raw = str(soup.find_all('span')[1]) #El nombre de archivo se encuentra en el 2º elemento de la lista de elementos 'span'
        nameServer_raw = str(soup.find_all('span')[3]) #El nombre del servidor (junto con otra información) se encuentra en el 4º elemento de la lista de elementos 'span'
        fileName = self.getTextFromTag(fileName_raw) #Nombre de archivo "final"
        #~ print fileName
        nameServer_1 = self.getTextFromTag(nameServer_raw) # Este texto tiene más información de la que necesitamos
        #~ print nameServer_1 
        nameServer_1 = list(nameServer_1)  #Lo convertimos en lista para poder manejarlo más fácilmente
        #~ print nameServer_1 # tiene esta forma '9273 | TE_SAMARE' debemos saber en que posicion está la barra
        indice = 0; # el índice a partir debemos cortar
        indicelista = 0 #Índice de la lista que recorremos
        for x in nameServer_1:
            if x == '|':
                indice = indicelista+2 #Sumamos para poner otro índice, excluyendo la barra vertical y el espacio
            else:
                indicelista = indicelista+1
        #~ print "índice "+str(indice)
        nameServer_L = nameServer_1[indice:] #Extraemos de la lista los caracteres que nos interesan
        #~ print nameServer_L
        nameServer = ''
        for x in nameServer_L: #Convertimos la lista en una cadena de texto
            nameServer = nameServer+x
        #~ print nameServer
        return "http://www.rtve.es/resources/%s/%s" % (nameServer,fileName)
        
    def descifrarUrl(self,url):
        Idelvideo = self.parseRtveUrl_2(url) #primero obtenemos el id del video (está separado porque es más propenso a errores)
        return self.descifrarDesdeId(Idelvideo) #obtenemos el url
        
    def descifrarDesdeId(self,identificator): #Esta función es menos propensa a fallar
        return self.getLinkVideo(self.getAssetDataId(identificator))

#~ print getLinkVideo(getAssetDataId('1345310')) #Amar en tiempos revueltos
#~ print getLinkVideo(getAssetDataId('1452436')) #On_off
#~ print getLinkVideo(getAssetDataId('1462683')) #Telediario
if __name__ == "__main__":
    print "Introduce la dirección del vídeo de rtve.es para descargar: "
    direccion = raw_input()
    print "La dirección del vídeo es: "
    print rtvees_alacarta().descifrarUrl(direccion)
