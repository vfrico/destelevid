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
__date__ ="$2-mar-2012 23:55:38$"

import sys
import urllib2
import httplib
import re
from Descargar import Descargar
from utiles import salir, formatearNombre

class MTV(object):
    '''
        Clase de mtv que maneja los métodos para descargar los vídeos de
        la web de rtpa.es
    '''
    
    # Url de xml:
    XML_URL = "http://www.mtv.es/services/scenic/feeds/get/mrss/"
    PROXY_LINFOX = "http://linfox.es/p/browse.php?u="

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

    def __GET(self, url):
        headers = {
                    "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)", 
                    }
        host = "".join(url.split("/")[1:3])
        path = "/" + "/".join(url.split("/")[3:])
        conn = httplib.HTTPConnection(host, 80)
        conn.request("GET", path, None, headers)
        response = conn.getresponse()
        
        if response.status == 404: #NOT FOUND
            data = "404"
        elif response.status == 400: #BAD REQUEST
            data = "400"
        else:
            data = response.read()
        conn.close()
        return data
        
    
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
        uri = streamHTML.split("var uri = \"")[1].split("\"")[0]
        streamXML = self.__descHTML(self.XML_URL + uri)
        name = streamXML.split("<title>")[1].split("<![CDATA[")[1].split("]]>")[0]
        name = name.replace("!", "").replace("|","") + ".mp4"
        
        #xmlURL = self.PROXY_LINFOX + streamXML.split("<media:content")[1].split("url=\"")[1].split("\"")[0]
        #Sin Proxy en modo local:
        xmlURL = streamXML.split("<media:content")[1].split("url=\"")[1].split("\"")[0]
        streamXML2 = self.__GET(xmlURL)
        #ulr = streamXML2.split("</rendition>")[-2].split("<src>")[1].split("</src>")[0]
        url = "rtmp" + streamXML2.split("<src>rtmp")[-1].split("</src>")[0]

        name = formatearNombre(name)
        
        return [url, name]
