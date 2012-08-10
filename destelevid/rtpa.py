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

# Se establece la Clase del objeto a3: que maneja los métodos para descargar
# los vídeos de la página de Antena 3 Televisón:

__author__="aabilio"
__date__ ="$2-mar-2012 22:03:38$"

import sys
import urllib2
import re
from Descargar import Descargar
from utiles import salir, formatearNombre, printt

class RTPA(object):
    '''
        Clase de RTPA que maneja los métodos para descargar los vídeos de
        la web de rtpa.es
    '''
    
    TOKEN = "http://servicios.rtpa.es/flumotion/player/tokenondemand_mp4.php?r=vod&v="
    TOKEN_ARCHIVO = "http://www.rtpa.es/vod_get_m3u_video.php?id="

    def __init__(self, url=""):
        self._URL_recibida = url

    def getURL(self):
        return self._URL_recibida
    def setURL(self, url):
        self._URL_recibida = url
    url = property(getURL, setURL)

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
        '''
        
        streamHTML = self.__descHTML(self._URL_recibida).replace("\n", "").replace("\t", "")
        # Cuantas partes son:
        try: 
            partes = int(streamHTML.split("&partes=")[1].split("&")[0])
        except IndexError: # No existe "&partes"
            partes = 1
        
        if partes == 1:
            videoID = streamHTML.split("<param value=\"video1=")[1].split("&")[0]
            if videoID.find("http://") != -1:
                url = videoID
                name = streamHTML.split("data-text=\"")[1].split("\"")[0].strip() + "." + url.split(".")[-1]
            else:
                # Probar entre TOKEN nuevo y antiguo por reproductor:
                repro = streamHTML.split("<param value=\"player/")[1].split("\"")[0]
                if repro == "reproductorVideoOnDemmand-mp4-rtpa.swf": # Antiguo
                    streamINFO = self.__descHTML(self.TOKEN_ARCHIVO + videoID)
                    url = "http://" + streamINFO.split("http://")[1]
                else: # Reproductor nuevo: "reproductorVideoOnDemmand.swf"
                    streamINFO = self.__descHTML(self.TOKEN + videoID + "_1")
                    streamINFO = self.__descHTML(streamINFO.split("&url=")[1])
                    url = "http://" + streamINFO.split("http://")[1]
                name = streamHTML.split("<div id=\"sobreElVideo\">")[1].split("<h3>")[1].split("</h3>")[0]
                if name == "":
                    name = streamHTML.split("<title>")[1].split("</title>")[0] + ".mp4"
                else: name + ".mp4"
        else:
            # Recordar que hay videos que ponen varias partes en las que realmente solo existe una:
            videoID = streamHTML.split("<param value=\"video1=")[1].split("&")[0]
            url = []
            name = []
            for i in range(1, partes+1):
                streamINFO = self.__descHTML(self.TOKEN + videoID + "_" + str(i))
                streamINFO = self.__descHTML(streamINFO.split("&url=")[1])
                
                tmp_url = "http://" + streamINFO.split("http://")[1]
                tmp_name = streamHTML.split("<div id=\"sobreElVideo\">")[1].split("<h3>")[1].split("</h3>")[0] +"_part" + str(i)
                if tmp_name == "":
                    tmp_name = streamHTML.split("<title>")[1].split("</title>")[0] + "_part" + str(i) + ".mp4"
                else: tmp_name + ".mp4"
                
                try: #TODO to FIXME: Buscar cómo saber si está disponible el vídeo sin descargarlo
                    print "Intentando descargar:", tmp_url
                    self.__descHTML(tmp_url)
                except:
                    break # ya no habrá más partes válidas
                else:
                    # La parte es válida
                    url.append(tmp_url)
                    name.appen(tmp_name)
                    continue
                    
        if type(name) == list:
            for i in name:
                b = formatearNombre(i)
                name[name.index(i)] = b
        else:
            name = formatearNombre(name)
        
        return [url, name]

