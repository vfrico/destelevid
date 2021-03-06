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
from pyamf import remoting
import httplib

from pprint import pprint

class EITB(object):
    '''
        Clase que maneja la descarga los vídeos de la EITB
    '''
    
    URL_EITB = "http://www.eitb.com/"
    URL_EITB_JSON = "http://www.eitb.com/es/get/multimedia/video_json/id/"

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
    
    def build_amf_request(self, const, playerID, videoID, publisherID):
        env = remoting.Envelope(amfVersion=3)
        env.bodies.append(
            (
                "/1", 
                remoting.Request(
                    target="com.brightcove.player.runtime.PlayerMediaFacade.findMediaById", 
                    body=[const, playerID, videoID, publisherID],
                    envelope=env
                )
            )
        )
        return env
    
    def get_data(self, publisherID, playerID, const, videoID, playerKey):
        conn = httplib.HTTPConnection("c.brightcove.com")
        envelope = self.build_amf_request(const, playerID, videoID, publisherID)
        #conn.request("POST", "/services/messagebroker/amf?playerKey=AQ~~,AAAAF8Q-iyk~,FDoJSqZe3TSVeJrw8hVEauWQtrf-1uI7", str(remoting.encode(envelope).read()),{'content-type': 'application/x-amf'})
        conn.request("POST", "/services/messagebroker/amf?playerKey="+playerKey, str(remoting.encode(envelope).read()),{'content-type': 'application/x-amf'})
        response = conn.getresponse().read()
        response = remoting.decode(response).bodies[0][1].body

        return response
    
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
        
        streamHTML = self.__descHTML(self._URL_recibida)
        if self._URL_recibida.find("audios/") != -1 or self._URL_recibida.find("audioak/") != -1:
            printt(u"[INFO] Audio")
            name = streamHTML.split("<title>")[1].split("<")[0]
            streamMP3 = streamHTML.split("<a id=\"descargaMp3\"")[1].split(">")[0]
            url = self.URL_EITB + streamMP3.split("href=\"")[1].split("\"")[0]
            name += ".mp3"
            
        elif self._URL_recibida.find("videos/") != -1 or self._URL_recibida.find("bideoak/") != -1 or self._URL_recibida.find("video/") != -1 :
            if streamHTML.find("<a id=\"descargaMp4\"") != -1:
                name = streamHTML.split("<title>")[1].split("<")[0]
                streamMP4 = streamHTML.split("<a id=\"descargaMp4\"")[1].split(">")[0]
                url = self.URL_EITB + streamMP4.split("href=\"")[1].split("\"")[0]
            else:
                #streamHTML = self.__descHTML(self._URL_recibida)
                name = self._URL_recibida.split("/")[-1]
                playerID = streamHTML.split("<param name=\"playerID\" value=\"")[1].split("\"")[0]
                playerKey = streamHTML.split("<param name=\"playerKey\" value=\"")[1].split("\"")[0]
                const = "9f8617ac59091bcfd501ae5188e4762ffddb9925"
                publisherID = "102076681001"
                videoID = self._URL_recibida.split("/")[-1]
                
                rtmpdata = self.get_data(publisherID, playerID, const, videoID, playerKey)['renditions']
                URL = str(rtmpdata[0]['defaultURL'])
                r = URL.split("&")[0] 
                a = "/".join(r.split("/")[-3:])
                C1 = "B:0"
                C2 = "S:" + "&".join(URL.split("&")[1:])
                y = URL.split("&")[1]
                url = r
                
                #print "rtmpdump -r " + r + " -a " + a + " -C " + C1 + " -C " + C2 + " -y " + y + " -o " + name + ".mp4"
                
            name += ".mp4"
        else:
            salir(u"[!!!] No se reconoce el tipo de contenido")
        
        
        if name:
            name = formatearNombre(name)

        return [url, name, "-a", a, "-C", C1, "-C", C2, "-y", y]



