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

# Este módulo no es independiente, se utiliza Telecinco.py


__author__="aabilio"
__date__ ="$03-may-2012 23:11:07$"

from telecinco import Telecinco
from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys 

class Divinity(object):
    '''
        Clase que maneja la descarga de los vídeo de Divinity
    '''

    URL_TELECINCO = "http://www.telecinco.es/"

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
        '''
        
        streamHTML = self.__descHTML(self._URL_recibida)
        streamVids = streamHTML.split("<iframe src=\"http://www.telecinco.es/")[1:]
        urls = [self.URL_TELECINCO + i.split("\"")[0] for i in streamVids]
        url2down = []
        name = []
        for url in urls:
            tv5 = Telecinco(url)
            tmp_url, tmp_name = tv5.procesarDescarga()
            url2down.append(tmp_url)
            name.append(tmp_url.split(".mp4")[0].split("/")[-1] + ".mp4")
        
        if url2down == list and len(url2down) == 1:
            url2down = url2down[0]
        
        if type(name) == list:
            for i in name:
                b = formatearNombre(i)
                name[name.index(i)] = b
            if len(name) == 1:
                name = name[0]
        else:
            name = formatearNombre(name)
        
        return [url2down, name]



