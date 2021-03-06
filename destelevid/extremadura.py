#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PyDownTV.
#
#    PyDownTV is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyDownTV is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyDownTV.  If not, see <http://www.gnu.org/licenses/>.

# Pequeña descripción de qué canal de tv es el módulo

__author__="aabilio"
__date__ ="$15-may-2011 11:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys  

class ETV(object):
    '''
        Clase que maneja la descarga los vídeos de Extremadura TV
    '''
    
    URL_ETV = "http://extremaduratv.canalextremadura.es/"

    def __init__(self, url=""):
        self._URL_recibida = url

    def getURL(self):
        return self._URL_recibida
    def setURL(self, url):
        self._URL_recibida = url
    url = property(getURL, setURL)

    # Funciones privadas que ayuden a procesarDescarga(self):
    def __descHTML(self, url2down):
        ''' Método que utiliza la clase descargar para descargar el HTML '''
        D = Descargar(url2down)
        return D.descargar()

    def procesarDescarga(self):
        '''
            Procesa lo necesario para obtener la url final del vídeo a descargar y devuelve
            esta y el nombre como se quiere que se descarge el archivo de la siguiente forma:
            return [ruta_url, nombre]

            Si no se quiere especificar un nombre para el archivo resultante en disco, o no se
            conoce un procedimiento para obtener este automáticamente se utilizará:
            return [ruta_url, None]
            Y el método de Descargar que descarga utilizará el nombre por defecto según la url.
            
            Tanto "ruta_url" como "nombre" pueden ser listas (por supuesto, el nombre del ruta_url[0]
            tiene que ser nombre[0] y así sucesivamente).
        '''
        
        if self._URL_recibida.find("tv-a-la-carta/") != -1 or self._URL_recibida.find("http://alacarta.canalextremadura.es/tv") != -1 or self._URL_recibida.find("canalextremadura.es/alacarta/tv/") != -1:
            printt(u"[INFO] TV a la carta")
            streamHTML = self.__descHTML(self._URL_recibida).replace(" ", "")
            
            if streamHTML.find("crea_video_hd(") != -1:
                urlFLV = streamHTML.split("crea_video_hd(\"")[1].split("\"")[0]
                streamFLV = self.__descHTML(urlFLV)
                url = "http://" + streamFLV.split("http://")[1]
                ext = "." + url.split(".")[-1].split("?")[0]
            elif streamHTML.find("file:'") != -1:
                try:
                    url = streamHTML.split("\'file\':\'")[1].split("\'")[0] #Modo nomal nuevo
                except: #Modo normal antiguo
                    url = streamHTML.split("streamer:\'")[1].split("\'")[0] + streamHTML.split("file:\'")[1].split("\'")[0]
                ext = "." + url.split(".")[-1]
            elif streamHTML.find("rel=\"rtmp://") != -1: #RTMP en alacarta
                url = "rtmp://" + streamHTML.split("rel=\"rtmp://")[1].split("\"")[0].replace("#", "")
                url = url.split(".mp4")[0] + ".mp4"
                ext = ".mp4"
            elif streamHTML.split("if(isiPad)") != -1: #HTTP para iPad
                url = streamHTML.split("<video")[1].split(".mp4")[0].split("\"")[-1] + ".mp4"
                ext = ".mp4"
            else:
                salir(u"[!!!] No se encuentra el vídeo")
            name = streamHTML.split("<title>")[1].split("<")[0] + ext
        elif self._URL_recibida.find("radio-a-la-carta/") != -1 or self._URL_recibida.find("http://alacarta.canalextremadura.es/radio") != -1 or self._URL_recibida.find("canalextremadura.es/alacarta/radio/") != -1:
            printt(u"[INFO] Radio A la Carta")
            streamHTML = self.__descHTML(self._URL_recibida).replace(" ", "")
            try: #Modo nuevo
                url = streamHTML.split("<divclass=\"descargar\">")[1].split("<ahref=\"")[1].split("\"")[0]
            except: #Modo antiguo
                url = streamHTML.split("s1.addVariable(\'file\',\'")[1].split("\'")[0]
            name = streamHTML.split("<title>")[1].split("<")[0] + ".mp3"
        else: #Modo normal nuevo con nueva url recibida
            printt(u"[INFO] Modo Genérico")
            streamHTML = self.__descHTML(self._URL_recibida).replace(" ", "")
            url = streamHTML.split("\'file\':\'")[1].split("\'")[0] #Modo nomal nuevo
            ext = "." + url.split(".")[-1]
            name = streamHTML.split("<title>")[1].split("<")[0] + ext
        
        if name:
            name = formatearNombre(name)

        return [url, name]



