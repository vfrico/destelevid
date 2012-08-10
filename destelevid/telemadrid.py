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

__author__="aabilio"
__date__ ="$31-oct-2011 04:03:38$"

from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys
import httplib
from pyamf import remoting

class TeleMadrid(object):
    '''
        Clase TeleMadrid
    '''
    
    Publisher_ID = "104403117001"
    Player_ID = "111787372001"
    Const = "9f8617ac59091bcfd501ae5188e4762ffddb9925"

    def __init__(self, url=""):
        self._URL_recibida = url

    def getURL(self):
        return self._URL_recibida
    def setURL(self, url):
        self._URL_recibida = url
    url = property(getURL, setURL)

    # Funciones privadas que ayuden a procesarDescarga(self):
    def __getStream(self, url2down):
        ''' Método que utiliza la clase descargar para descargar el HTML '''
        D = Descargar(url2down)
        return D.descargar()
    
    def __build_amf_request(self, videoPlayer):
        env = remoting.Envelope(amfVersion=3)
        env.bodies.append(
            (
                "/1", 
                remoting.Request(
                    target="com.brightcove.player.runtime.PlayerMediaFacade.findMediaById", 
                    body=[self.Const, self.Player_ID, videoPlayer, self.Publisher_ID],
                    envelope=env
                )
            )
        )
        return env
    
    def __get_info(self, videoPlayer):
         conn = httplib.HTTPConnection("c.brightcove.com")
         envelope = self.__build_amf_request(videoPlayer)
         conn.request("POST", 
            "/services/messagebroker/amf?playerKey=AQ~~,AAAAF8Q-iyk~,FDoJSqZe3TSVeJrw8hVEauWQtrf-1uI7", 
            str(remoting.encode(envelope).read()),
            {'content-type': 'application/x-amf'})
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
        
        streamHTML = self.__getStream(self._URL_recibida)
        name = streamHTML.split("<meta name=\"dc.title\" content=\"")[1].split("\"")[0]
        VideoPlayer = streamHTML.split("<param name=\"@videoPlayer\" value=\"")[1].split("\"")[0]
        info = self.__get_info(VideoPlayer)['renditions']
                
        big = 0
        for video in info:
            if video['encodingRate'] >= big:
                big = video['encodingRate']
                url = video['defaultURL']
        
        ext = "." + url.split(".")[-1]
        
        if name:
            name = formatearNombre(name)
            
        name += ext

        return [url, name]



