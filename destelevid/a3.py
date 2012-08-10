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
__date__ ="$29-mar-2011 11:03:38$"

import sys
import urllib2
import re
from Descargar import Descargar
from utiles import salir, formatearNombre, stringFormat, printt

class A3(object):
    '''
        Clase de de A3 que maneja los métodos para descargar los vídeos de
        la web de antena3.com
    '''
    URL_DE_ANTENA3  = "http://www.antena3.com/"
    URL_DE_DESCARGA = "http://desprogresiva.antena3.com/"
    URL_DE_F1 = "http://www.antena3.com/gestorf1/xml_visor/"
    URL_VISOR_F1 = "http://www.antena3.com/gestorf1/static_visor/"

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
    def __descXML(self, url2down):
        ''' Método que utiliza la clase descargar para descargar HTML '''
        D = Descargar(url2down)
        return D.descargar()
    def __get8stream(self, url2down):
        ''' Método que utiliza la clase descargar para descargar HTML '''
        D = Descargar(url2down)
        return D.utfDown()
        
    def __modoSalonNuevo(self, streamXML):
        '''Nuevos vídeos con extensión .m4v'''
        printt(u"[INFO] Nuevos vídeos en formato f4v")
        if streamXML.find("000.f4v"):
            url2down1 = self.URL_DE_DESCARGA + streamXML.split("<archivo><![CDATA[")[1].split("]")[0]
        else:
            url2down1 = self.URL_DE_DESCARGA + \
                streamXML.split("<archivo><![CDATA[")[1].split("001.f4v]]></archivo>")[0] + "000.f4v"
        try: # Descargar entero
            urllib2.urlopen(url2down1)
            url2down = url2down1
            name = streamXML.split("<nombre><![CDATA[")[1].split("]]>")[0] + ".f4v"
        except urllib2.HTTPError: # Descargar por partes:
            printt(u"[!!!]  No se puede descargar el vídeo en un archivo (000.m4v)")
            printt(u"[INFO] El vídeo se descargará por partes")
            parts = re.findall("\<archivo\>\<\!\[CDATA\[.*\.f4v\]\]\>\<\/archivo\>", streamXML)
            if parts:
                name1 = streamXML.split("<nombre><![CDATA[")[1].split("]]>")[0]
                url2down = []
                name = []
                for i in parts:
                    url2down.append(self.URL_DE_DESCARGA + i.split("<archivo><![CDATA[")[1].split("]]></archivo>")[0])
                    name.append(name1 + "_" + i.split("]")[0].split("/")[-1])
            else:
                salir(u"[!!!] ERROR: No se encuentran las partes del vídeo")
        
        return [url2down,  name]

    def __modoSalon(self, streamHTML):
        printt(u"[INFO] Modo Salón")
        if streamHTML.find("so.addVariable(\"xml\"") != -1:
            streamXML = \
            self.__descXML(self.URL_DE_ANTENA3 + streamHTML.split("so.addVariable(\"xml\",\"")[1].split("\"")[0])
        elif streamHTML.find("player_capitulo.xml='") != -1:
            streamXML = \
            self.__descXML(self.URL_DE_ANTENA3 + streamHTML.split("player_capitulo.xml='")[1].split("'")[0])
        else:
            salir(u"[!!!] ERROR No se encuentra el XML")
        # Comprobar aquí si se puede descargar 000.mp4:
        if streamXML.find(".mp4") != -1:
            url2down1 = self.URL_DE_DESCARGA + \
                streamXML.split("<archivo><![CDATA[")[1].split("001.mp4]]></archivo>")[0] + "000.mp4"
        elif streamXML.find(".f4v") != -1:
            [url2down, name] = self.__modoSalonNuevo(streamXML)
            return [url2down, name]
        else:
            salir(u"[!!!] ERROR: No se encuentra vídeos mp4 o f4v")
        try: # Descargar entero
            urllib2.urlopen(url2down1)
            url2down = url2down1
            name = streamXML.split("<nombre><![CDATA[")[1].split("]]>")[0] + ".mp4"
        except urllib2.HTTPError: # Descargar por partes:
            printt(u"[!!!]  No se puede descargar el vídeo en un archivo (000.mp4)")
            printt(u"[INFO] El vídeo se descargará por partes")
            parts = re.findall("\<archivo\>\<\!\[CDATA\[.*\.mp4\]\]\>\<\/archivo\>", streamXML)
            if parts:
                name1 = streamXML.split("<nombre><![CDATA[")[1].split("]]>")[0]
                url2down = []
                name = []
                for i in parts:
                    url2down.append(self.URL_DE_DESCARGA + i.split("<archivo><![CDATA[")[1].split("]]></archivo>")[0])
                    name.append(name1 + "_" + i.split("]")[0].split("/")[-1])
            else:
                salir(u"[!!!] ERROR: No se encuentran las partes del vídeo")
        
        return [url2down,  name]
    def __modoNormalConURL(self,  streamHTML):
        url2down = streamHTML.split(".seoURL='")[1].split("'")[0]
        name = self.__descXML(self.URL_DE_ANTENA3 + streamHTML.split(".xml='")[1].split("'")[0]).split("<nombre><![CDATA[")[1].split("]]>")[0] + ".mp4"
                
        return [url2down,  name]
        
    def __modoNormalVariasPartes(self, streamHTML):
        url2down = []
        name = []
        # Delimitamos la parte del carrusel (funcionará para todos??)
        streamHTML = streamHTML.split("<a title=\"Video Anterior\"")[1].split("<a title=\"Video Siguiente\"")[0]
        partes = len(streamHTML.split("<img title="))-1
        streamPARTES = streamHTML.split("<img title=")[1:]
        printt(u"[INFO] Número de partes:", str(partes))
        #print streamPARTES
        for i in streamPARTES:
            xmlURL = self.URL_DE_ANTENA3 + i.split("rel=\"/")[1].split("\"")[0]
            streamXML = self.__descXML(xmlURL)
            url2down.append(self.URL_DE_DESCARGA + streamXML.split("<archivo><![CDATA[")[1].split("]")[0])
            ext = streamXML.split("<archivo><![CDATA[")[1].split("]")[0].split('.')[-1]
            name.append(i.split("\"")[1].split("\"")[0] + '.' + ext)
        
        print "[INFO] URLs    :",  url2down
        print "[INFO] Nombres :",  name
        
        return [url2down, name]
        
    def __modoNormalUnaParte(self, streamHTML):
        xmlURL = streamHTML.split("A3Player.swf?xml=")[1].split("\"")[0]
        streamXML = self.__descXML(xmlURL)
        url2down =  self.URL_DE_DESCARGA + \
        streamXML.split("<archivo><![CDATA[")[1].split("]]></archivo>")[0]
        name = streamXML.split("<nombre><![CDATA[")[1].split("]]>")[0] + ".mp4"
        
        return [url2down, name]
    
    def __modoF1(self,  streamHTML):
        '''
       <param value="_urlData=http://www.antena3.com/gestorf1/swf/player_hitos/xml/data.xml&_image=http://www.antena3.com/gestorf1/pictures/361/361/malasia-portada_crop1.png&_id_list=1405&_promo1=http://www.smartadserver.com/call/pubx/15272/241149/4654/S/&_promo2=http://www.smartadserver.com/call/pubx/15272/241148/4654/S/" name="flashVars">
       '''
        streamHTML = self.__get8stream(self._URL_recibida)
        # Qué vídeo:
        streamVids = streamHTML.split("<ul class=\"a3_gp_visor_menu\">")[1].split("</ul>")[0].replace("\t", "")
        streamVids = streamVids.split("<li>")[1:]
        printt(u"[???] Qué quieres descargar: ")
        b = 0
        for i in streamVids:
            b += 1
            printt(u"\t%d) %s" % (b, i.split(">")[1].split("<")[0].capitalize()))
        opc = False
        while opc is False:
            opc = raw_input("[(%d a %d) >>>] " % (1, b))
            if opc.isdigit():
                opc = int(opc)
                if opc < 1 or opc > b: 
                    opc = False
            else:
                opc = False
        streamVid = streamVids[opc-1]
        streamVidUrl = self.URL_DE_ANTENA3 + streamVid.split("href=\"")[1].split("\"")[0]
        
        # Vamos a por el vídeo
        streamHTML = self.__descHTML(streamVidUrl)
        
        url2down = []
        name = []
        id_list = streamHTML.split("_id_list=")[1].split("&")[0]
        #printt(u"[DEBUG] url2down", str(id_list))
        listxml = self.__descXML(self.URL_DE_F1 + id_list + "_playlist.xml")
        listxml = listxml.split("<video>")[1:]
        for i in listxml:
            url2down.append(i.split("<url>")[1].split("<")[0])
            ext = "." + url2down[-1].split(".")[-1]
            name.append(i.split("<title>")[1].split("<")[0] + ext)
            
        
        return [url2down, name]
    
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
        # print "[+] Procesando descarga"
        streamHTML = self.__descHTML(self._URL_recibida)
        if self._URL_recibida.find("antena3.com/videos/") != -1: # Modo Salón
            url2down,  name = self.__modoSalon(streamHTML)
        else: # Otro vídeos (No modo salón)
            printt(u"[INFO] Vídeo normal (no Modo Salón)")
            if streamHTML.find(".seoURL='") != -1: # Url directamente en HTML
                url2down, name = self.__modoNormalConURL(streamHTML)
            elif streamHTML.find("a3_gp_visor_player") != -1:
                url2down, name = self.__modoF1(streamHTML)
            else: # No está la url en el hmtl (buscar por varias partes)
                if streamHTML.find("<div class=\"visor\">") != -1: # Más de 1 parte # Quizas mejor "carrusel"?
                    url2down, name = self.__modoNormalVariasPartes(streamHTML)
                else: # Solo una parte
                    url2down, name = self.__modoNormalUnaParte(streamHTML)
        
        if type(url2down) == list:
            for i in url2down:
                if i.find("geobloqueo") != -1:
                    printt(u"[!!!] El vídeo \"" + i + "\" no se puedo descargar (geobloqueado)")
                    url2down.remove(i)
                    # TODO: Borrar también su nombre correspondiente
                
            # Comprobar si todas las partes están geobloqueadas (no quedan elementos en la lista):
            if len(url2down) == 0:
                salir(u"[!] No se puede descargar ninguna parte (geobloqueadas)")
        else:
            if url2down.find("geobloqueo") != -1:
                salir(u"[!] El vídeo no se puede descargar (geobloqueado)")

        if type(name) == list:
            for i in name:
                b = formatearNombre(i)
                name[name.index(i)] = b
        else:
            name = formatearNombre(name)
        
        return [url2down , name]

