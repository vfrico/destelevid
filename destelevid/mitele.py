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

# Módulo MiTele.
# Utiliza el módulo MD5 de http://code.google.com/p/xbmc-tvalacarta/source/browse/trunk/pelisalacarta/core/aes.py
# Y la primera versión del módulo el procedimiento descrito por Carballude en http://www.carballude.es/blog/2011/11/17/descargar-videos-de-telecinco-mitele-es-de-forma-manual/

__author__="aabilio"
__date__ ="$07-Feb-2012 11:03:38$"


from Descargar import Descargar
from utiles import salir, formatearNombre, printt
import sys 
import urllib
import urllib2
import httplib
import time
import aes

class MiTele(object):
    '''
        MiTele 
    '''
    
    #URL_TIME  = "http://www.mitele.es/media/clock.php"
    URL_TIME = "http://servicios.telecinco.es/tokenizer/clock.php"
    
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
    
    def __getpassw(self, current):
        self.usedpass.append(current)
        passw = self.PASS
        for i in range(len(passw)):
            if i == len(passw) and passw[i] == current:
                if passw[0] in self.usedpass:
                   return None 
                return passw[0]
            if passw[i-1] == current:
                if passw[i] in self.usedpass:
                    return None
                return passw[i]
    
    def __post(self, post_args, tokenizer):
        Post = urllib.urlencode(post_args, doseq=True)
        headers = {
                    "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)", 
                    "Host": "servicios.mitele.es", 
                    #"Accept-Encoding": "gzip", 
                    "Accept-Charset": "ISO-8859-1,UTF-8;q=0.7,*;q=0.7", 
                    "Referer": "http://static1.tele-cinco.net/comun/swf/playerMitele.swf",
                    "Connection": "close", 
                    "Accept-Language": "de,en;q=0.7,en-us;q=0.3", 
                    "Content-type": "application/x-www-form-urlencoded"
                    }
        #conn = httplib.HTTPConnection("213.4.97.107", 80)
        conn = httplib.HTTPConnection("servicios.mitele.es", 80)
        conn.request("POST", tokenizer, Post, headers)
        response = conn.getresponse()
        
        #print response.status, response.reason
        if response.status == 404: #NOT FOUND
            data = None
        elif response.status == 400: #BAD REQUEST
            data = None
        else:
            data = response.read()
        conn.close()
        
#        import re
#        
#        patron = '<stream>([^?]+)?([^<]+)</stream>'
#        matches = re.compile(patron,re.DOTALL).findall(data)
#        rtmp0 = matches[0][0]
#        print "rtmp0 -->", rtmp0
#        rtmp1 = matches[0][1]
#        print "rtmp1 -->", rtmp1
#        
#        patron = '<file>([^<]+)</file>'
#        matches = re.compile(patron,re.DOTALL).findall(data)
#        file = matches[0]
#        print "file -->", file
#        
#        rtmp = rtmp0 + "/" + file + rtmp1
#        print "rtmp -->", rtmp
#     
#        xbmcrtmp = rtmp0 + " playpath=" + file+rtmp1 + " swfUrl=\"http://static1.tele-cinco.net/comun/swf/playerMitele.swf\" pageUrl=\"" + "AQUI_VA_LA_URL" + "\" live=true"
#        
#        print "total -->", xbmcrtmp
        
        return data
                
    def __metodo_1(self, id, startTime, endTime):
        '''
            Método principal, el primero de todos implementado:
            
            TK - Pass de "N":
            ==================
            force_http -> 1
            id -> /url/url/url.mp4
            sec -> encode(serverTime;id;startTime;endTime)
        '''
        printt(u"[INFO] Probando Método 1")
        AES = aes.AES() 
        tokenizer = "/tokenizer/tk.php"
        passwd = "xo85kT+QHz3fRMcHNXp9cA"
        
        server_time = self.__descHTML(self.URL_TIME).strip()
        toEncode = server_time+";"+id+";"+startTime+";"+endTime
        data = AES.encrypt(toEncode, passwd, 256)
        post_args = {
                    'force_http' : '1',
                    'sec' : data,
                    'id' : id
                    }
        
        url = self.__post(post_args, tokenizer)
        return url
    
    def __metodo_2(self, id, startTime, endTime):
        '''
            Segundo Método implementado:
            
            TK2 - Pass de "N":
            ==================
            force_http -> 1
            id -> /url/url/url.mp4
            sec -> encode(serverTime;id;startTime;endTime)
        '''
        printt(u"[INFO] Probando Método 2")
        AES = aes.AES() 
        tokenizer = "/tokenizer/tk2.php"
        passwd = "xo85kT+QHz3fRMcHNXp9cA"
        server_time = self.__descHTML(self.URL_TIME).strip()
        toEncode = server_time+";"+id+";"+startTime+";"+endTime
        data = AES.encrypt(toEncode, passwd, 256)
        post_args = {
                    'force_http' : '1',
                    'sec' : data,
                    'id' : id
                    }
                    
        url = self.__post(post_args, tokenizer)
        if url is None: return None
        else: return url
    
    def __metodo_3(self, id, startTime, endTime):
        '''
            Tercer método implementado:
            
            TK3 - Pass de "M":
            ==================
            force_http -> 1
            hash -> encode(serverTime;id;startTime;endTime)
            id -> /url/url/url.mp4
            startTime -> 0
            endTime -> 0
        '''
        printt(u"[INFO] Probando Método 3")
        AES = aes.AES() 
        tokenizer = "/tokenizer/tk3.php"
        passwd = "xo85kT+QHz3fRMcHMXp9cA"
        server_time = self.__descHTML(self.URL_TIME).strip()
        toEncode = server_time+";"+id+";"+startTime+";"+endTime
        data = AES.encrypt(toEncode, passwd, 256)
        post_args = {
                   #'force_http' : '1',
                    'hash' : data,
                    'id' : id,
                    'startTime' : '0',
                    'endTime': '0'}
        
        data = self.__post(post_args, tokenizer)

        if data is None:
            return None
        else:
            #print "DATA:", data
            if data.find("<stream>") != -1: # FIXME: Este comandono funciona
                R = data.split("<stream>")[1].split("</stream>")[0]
                A = "\""+ "/".join(data.split("/")[4:]).split("</stream>")[0] +"\""
                F = "\""+ "WIN 11,1,102,55" +"\""
                W = "\""+ "http://static1.tele-cinco.net/comun/swf/playerMitele.swf" +"\""
                P = "\""+ self._URL_recibida +"\""
                Y = "\""+ "mp4:" + data.split("</file>")[0].split("mp4:")[1] +"\""
                url = [R, "-a", A, "-f", F, "-W", W, "-p", P, "-y", Y]
            else:
                try:
                    url = data.split("<url><file>")[1].split("</file></url>")[0].replace("&amp;", "&")
                except IndexError:
                    url = data.split("<file geoblocked=\"true\">")[1].split("</file></url>")[0].replace("&amp;", "&")
            return url

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
        
        # Obtener HTML y XML:
        streamHTML = self.__descHTML(self._URL_recibida).replace(" ", "")
        streamXML = self.__descHTML(streamHTML.split("{\"host\":\"")[1].split("\"")[0].replace("\/", "/"))
                                                                                               
        # Obtener ID y starTime, endTime:
        if streamXML.find("<rtmp") != -1:
            if streamXML.find("rtmp=\"false\"") != -1: # Igual que el normal
                    id = (streamXML.split("<link start=")[1].split("</link>")[0]).split("\">")[1].split("<")[0]
            else:
                id = streamXML.split("<rtmp")[1].split("<url><![CDATA[")[1].split("]")[0]
        else:
            # Mantengo este ID por compatibilidad:
            id = (streamXML.split("<link start=")[1].split("</link>")[0]).split("\">")[1].split("<")[0]

        printt(u"[INFO] ID:", id)
        startTime = '0' if streamXML.find("<link start=\"") == -1 else streamXML.split("<link start=\"")[1].split("\"")[0]
        endTime = '0' if streamXML.find("end=\"") == -1 else streamXML.split("end=\"")[1].split("\"")[0]
        #printt(u"[INFO] startTime: %s\n[INFO] endTime: %s" % (startTime, endTime))
        
       # Probar los diferentes Métodos:
        url = self.__metodo_3(id, startTime, endTime) # Tendría que funcionar este
        if url is None:
            url = self.__metodo_2(id, startTime, endTime)
        if url is None:
            url = self.__metodo_1(id, startTime, endTime)
        if url is None:
            sys.exit("[!!!] Error al recuperar la url final de descarga.")
        
        # Obtener nombre:
        if type(url) == str:
            name = streamHTML.split("<title>")[1].split("<")[0] + "." + url.split(".")[-1].split("?")[0]
        else: # De momento: suponemos que son mp4.
            name = streamHTML.split("<title>")[1].split("<")[0] + ".mp4"
        if name:
            name = formatearNombre(name)
        
        name = name.replace("VERPROGRAMASVer", "").replace("online", "")
        name = name.replace("VERSERIESVer", "").replace("online", "")
        
        if type(url) == list:
            # La URL es una lista, pero no por que sean partes, si no porque
            # son streams RTMP con más opciones..
            _return = [url[0], name]
            for i in url[1:]:
                _return.append(i)
            return  _return
            
        return [url, name]



