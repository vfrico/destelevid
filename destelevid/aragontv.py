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
__date__ ="$12-oct-2011 21:03:38$"


from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys 

class AragonTV(object):
    '''
        Maneja lo descarga de os vídeos de A la carta de Aragón TV
    '''

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
        streamHTML = self.__descHTML(self._URL_recibida)
        name = streamHTML.split("<title>")[1].split("<")[0]
        streamHTML = streamHTML.replace("%3A", ":").replace("%2F", "/").replace(" ", "").replace("\t", "")
        clip = streamHTML.split("clip:")[1].split("url:\'")[1].split("\'")[0].replace("mp4:", "")
        server = streamHTML.split("netConnectionUrl:\'")[1].split("\'")[0]
        url = server + clip
        name += "." + clip.split(".")[-1]
        
        if name:
            name = formatearNombre(name)

        return [url, name]



