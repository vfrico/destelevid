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

# Clase que se encarga de descargar:

__author__="aabilio"
__date__ ="$30-mar-2011 20:57:46$"

import urllib2
import urllib
import subprocess
import time
import sys
import codecs
from os import system, path, remove, makedirs

from pyaxel import pyaxel
from utiles import salir, printt, PdtVersion, isWin


class Descargar(object):
    ''' Clase que se encarga de descargar con urllib2 '''
    
    std_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; '
        'en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/xml,application/xml,application/xhtml+xml,'
        'text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    'Accept-Language': 'en-us,en;q=0.5',
    }

    def __init__(self, url=None):
        self._outputName = None
        self._URL = url
        self._otros = None
        if self._URL == None:
            salir(u"ERROR: No se puede descargar la url")
    
    def getOutputName(self):
        return self._outputName
    def setOutputName(self, name):
        self._outputName = name
    def getOtros(self):
        return self._otros
    def setOtros(self, otros):
        self._otros = otros
    
    outputName = property(getOutputName, setOutputName)
    otros = property(getOtros, setOtros)
    
#    def descarga_general(self):
#        '''
#            Descarga el stream de la URL especificada
#        '''
#        if self._URL.find("http://") == -1: self._URL = "http://" + self._URL
#        
#        try:
#            request = urllib2.Request(self._URL, None, self.std_headers)
#            f = urllib2.urlopen(request)
#            Reader = codecs.getreader("utf-8")
#            fh = Reader(f)
#            stream = fh.read()
#            return stream
#        except Exception, e:
#            if self._URL.find("rtve.es") != -1:
#                return -1
#            elif self._URL == PdtVersion.URL_VERSION:
#                return -1
#            else:
#                printt(u"[!!!] ERROR al descargar:", e)
#                salir(u"")
#        else:
#            pass
#    
#    descargar = descarga_general # Compatibilidad
    
    def utfDown(self):
        if self._URL.find("http://") == -1:
            self._URL = "http://" + self._URL
        f = urllib2.urlopen(self._URL)
        Reader = codecs.getreader("utf-8")
        fh = Reader(f)
        stream = fh.read()
        return stream

    def descargar(self):
        '''
            Recoge una url la descarga y lo devuelve
            Pensado para descargar streams HTML y XML
        '''

        if self._URL.find("http://") == -1:
            self._URL = "http://" + self._URL
            
        try:
            # TVG necesita headers:
            if self._URL.find("crtvg.es/") != -1 or self._URL.find("tv3.cat/") != -1:
                request = urllib2.Request(self._URL, None, self.std_headers)
                f = urllib2.urlopen(request)
                stream = f.read()
                f.close()
                return stream
            elif self._URL == PdtVersion.URL_VERSION: # Si lo que se descarga es VERSION (convertir a utf-8)
                f = urllib2.urlopen(self._URL)
                Reader = codecs.getreader("utf-8")
                fh = Reader(f)
                stream = fh.read()
                return stream
            else:
                f = urllib2.urlopen(self._URL)
                stream = f.read()
                f.close()
                return stream
        except Exception, e:
            if self._URL.find("rtve.es") != -1: # No salir (para identificar si es a la carta o no)
                return -1
            elif self._URL == PdtVersion.URL_VERSION:
                return -1
            else:
                printt(u"[!!!] ERROR al descargar:", e)
                salir(u"")
        else:
            pass
    
    def __winGetExpandDownDir(self):
        home = path.expanduser("~")
        if path.isdir(path.join(home, "Descargas")):
            return path.join((home, "Descargas"))
        elif path.isdir(path.join(home, "Downloads")):
            return path.join((home, "Downloads"))
        else:
            return path.join((home, "Descargas"))
        
        
        
    
    def descargarVideoWindows(self, nombre=None):
        '''
            Procesa la descarga del vídeo llamanda a la función download de pyaxel para la mayoría de los
            vídeos en GNU/Linux y Mac OS X. Para sistemas win32, se llama a descargarVideoWindows() y tanto para
            GNU/Linux como para Mac OS X y Windows cuando el protocolo es mms:// se utiliza libmms (por ahora Windows no)
            y cuando el protocolo es rtmp:// se utiliza el binario rtmpdump que el user debe tener instalado.
        '''
        url = self._URL
        name = nombre if nombre != None else self._URL.split('/')[-1]
        downdir = self.__winGetExpandDownDir()
        
        printt(u"")
        printt(u"DESCARGAR:")
        printt(u"----------------------------------------------------------------")

        if type(self._URL) == list:
            b=1
            for i in self._URL:
                printt(u"[ URL DE DESCARGA FINAL ] [Parte %d] %s" % (b, i))
                b += 1
        else:
            printt(u"[ URL DE DESCARGA FINAL ]", self._URL)
            
        printt(u"[INFO] Presiona \"Ctrl + C\" para cancelar")
        printt(u"")
        
        def estadodescarga(bloque, tamano_bloque, tamano_total):
            '''
                función reporthook que representa en pantalla información mientras
                se realiza la descarga
            '''
            # En Megas
            try:
                cant_descargada = ((bloque * tamano_bloque) / 1024.00) / 1024.00
                tamano_total = (tamano_total / 1024.00) / 1024.00
                porcentaje = cant_descargada / (tamano_total / 100.00)
                if porcentaje > 100.00:
                    porcentaje = 100.00
            except ZeroDivisionError:
                pass
                #print "[DEBUG] Error de divisiñon entre cero"
            # TODO: Agregar velocidad de descarga al progreso
            sys.stdout.write("\r[Descargando]: [ %.2f MiB / %.2f MiB ]\t\t[ %.1f%% ]" \
                            % (cant_descargada, tamano_total, porcentaje))
                            
        #######
                            
        if type(self._URL) == list:
            printt(u"[?] Quieres descargar todas las partes? [s/n]:")
            opc = ""
            while opc != "s" and opc != "n":
                opc = raw_input()
                if opc is not "s" or opc is not "n":
                    printt(u"[!!!] [s/n]")
            
            if opc is "s":
                for i in range(0, len(self._URL)):
                    absdowndir = path.join(downdir, name[i])
                    printt(u"[Descargando %d parte]" % (int(i) + 1))
                    printt(u"[Destino]", absdowndir)
                    try:
                        urllib.urlretrieve(url[i], absdowndir, reporthook=estadodescarga)
                        print ""
                    #except KeyboardInterrupt:
                    #    sys.exit("\nCiao!")
                    except:
                        pass
                    print "\n"
            elif opc is "n":
                printt(u"\n[?] Qué partes quieres descargar?")
                printt(u"[INFO] Puedes introducir varias partes separadas por comas")
                
                ERROR = True
                while ERROR is True: 
                    ERROR = False
                    printt(u"[INFO] Partes:")
                    b = 1
                    for i in range(0, len(self._URL)):
                        printt(u"[Parte %s] %s" % (str(b), self._URL[i]))
                        b += 1
                    del b
                    printt(u"[?] --> ")
                    partes = raw_input()
                    partes = partes.split(",")
                    for i in partes:
                        if not i.isdigit():
                            printt(u"[!!!] ERROR. No se reconoce la parte \"%s\"" % i)
                            ERROR = True
                            break
                        if int(i) < 1 or int(i) > len(self._URL):
                            printt(u"[!!!] ERROR. La parte \"%s\" no existe" % int(i))
                            ERROR = True
                            break
                            
                printt(u"[OK] Se descargarán las partes")
                for i in partes:
                    absdowndir = path.join(downdir, name[int(i)-1])
                    printt(u"[Descargando %d parte]" % (int(i)))
                    printt(u"[Destino]", absdowndir)
                    try:
                        urllib.urlretrieve(url[int(i)-1], absdowndir, reporthook=estadodescarga)
                        print ""
                    #except KeyboardInterrupt:
                    #    sys.exit("\nCiao!")
                    except:
                        pass
                    print "\n"
        else:
            try:
                absdowndir = path.join(downdir, name)
                printt(u"[Destino]", absdowndir)
                urllib.urlretrieve(url, absdowndir, reporthook=estadodescarga)
                print ""
            except KeyboardInterrupt:
                salir("\nCiao!")
  
  
        #######
                            
    def alternative(self, name=None):
        url = self._URL

        file_name = name if name is not None else url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
        
    def descargarVideo(self):
        '''
            Procesa la descarga del vídeo llamanda a la función download de pyaxel para la mayoría de los
            vídeos en GNU/Linux y Mac OS X. Para sistemas win32, se llama a descargarVideoWindows() y tanto para
            GNU/Linux como para Mac OS X y Windows cuando el protocolo es mms:// se utiliza libmms (por ahora Windows no)
            y cuando el protocolo es rtmp:// se utiliza el binario rtmpdump que el cliente debe tener instalado.
        '''
        # downdir: ruta absoluta donde se va a descargar el video
        downdir = self.__winGetExpandDownDir() if isWin() else path.abspath(".")
        
        ########### RTMP  ###############################################################################################
        if type(self._URL) is not list and (self._URL.startswith("rtmp://") or self._URL.startswith("rtmpe://")):
            command = "rtmpdump"
            if sys.platform == "win32":
                command += ".exe"
            
            self.outputName = path.join(downdir, self.outputName)
            
            printt(u"")
            printt(u"DESCARGAR:")
            printt(u"----------------------------------------------------------------")
            printt(u"[ URL DE DESCARGA FINAL ]", self._URL)
            printt(u"[   DESTINO   ]", self.outputName)
            printt(u"\n[INFO] Presiona \"Ctrl + C\" para cancelar\n")
            
            args = [command, "--resume", "-o", self.outputName, "-r", self._URL]
            
            if self._otros: args[len(args):] = self._otros
            
            try:
                printt(u"\nLanzando rtmpdump...\n")
                out = None
                err = 0
                while out != 0:
                    out = subprocess.call(args)
                    if out == 0: # Descarga realizada con éxito
                        printt(u"[OK] Descarga realizada con éxito")
                    else:
                        err += 1
                        printt(u"\n[!!!] Se ha producido un error grave al descargar.")
                        printt(u"[INFO] Se intentará reiniciar la descarga pero no es seguro que funcione.")
                        printt(u"[INFO] Intentando reiniciar descarga en 3 segundos")
                        time.sleep(3)
                        if err == 5: salir(u"[!!!] Demasiados errores. Se aborta la descarga.")
                        if err == 2:
                            remove(self.outputName)
                            printt(u"\n[ERROR] El vídeo no se puede descargar con RTMPDUMP.")
                            printt(u"[INFO]  Se intenta descargar con MPLAYER/MENCODER:")
                            time.sleep(3)
                            command = "mencoder"
                            args =  [command, "-oac", "pcm", "-ovc", "copy", self._URL, "-o", self.outputName]
                            #command = "mencoder"
                            #args = [command, "-dumpstream", "-dumpfile", self.outputName, self._URL]
#                while out != 0:
#                    out = subprocess.call(args)
#                    if out == 2: # Error grave
#                        err += 1
#                        if err > 3:
#                            printt(u"\n[!!!] Demasiados errores.")
#                            time.sleep(2)
#                            printt(u"[INFO] Se intenta volver a descargar entero")
#                            time.sleep(2)
#                            printt(u"[INFO] Borrando", self.outputName)
#                            remove(self.outputName)
#                        if err > 5:
#                            printt(u"[!!!] ERROR irrecuperable. Se aborta la descarga. Sorry :(")
#                            break
#                            
#                        printt(u"\n[!!!] Se ha producido un error grave al descargar.")
#                        time.sleep(1)
#                        printt(u"[INFO] Se intentará reiniciar la descarga pero no es seguro que funcione.")
#                        time.sleep(1)
#                        printt(u"[INFO] Intentando reiniciar descarga en 3 segundos")
#                        time.sleep(3)
#                        
#                    if out == 0: # Descarga realizada con éxito
#                        printt(u"[OK] Descarga realizada con éxito")
#                    else: # Error recuperable
#                        err += 1
#                        if err > 3:
#                            printt(u"\n[!!!] Demasiados errores.")
#                            time.sleep(2)
#                            printt(u"[INFO] Se intenta volver a descargar entero")
#                            time.sleep(2)
#                            printt(u"[INFO] Borrando", self.outputName)
#                            remove(self.outputName)
#                        if err > 5:
#                            printt(u"\n[!!!] ERROR irrecuperable. Se aborta la descarga. Sorry :(")
#                            err = 0
#                            break
#                            
#                        printt(u"\n[!!!] Se ha producido un error con Rtmpdump, se intenta recuperar...")
#                        time.sleep(1)
#                        printt(u"[INFO] Se reinicia en 3 segundos")
#                        time.sleep(3)
                    
            except OSError, e:
                printt(u"[!!!] ERROR. No se encuenta rtmpdump o mplayer:", e)
            except KeyboardInterrupt:
                salir(u"Bye!")
            
            return
            
        if type(self._URL) is list and (self._URL[0].startswith("rtmp://") or self._URL[0].startswith("rtmpe://")):
            command = "rtmpdump"
            if sys.platform == "win32":
                command += ".exe"
                
            for n in range(len(self.outputName)):
                self.outputName[n] = path.join(downdir, self.outputName[n])
            
            printt(u"")
            printt(u"DESCARGAR:")
            printt(u"----------------------------------------------------------------")
            b=1
            for i in self._URL:
                printt(u"[ URL DE DESCARGA FINAL ] [Parte %d] %s" % (b, i))
                b += 1
            
            printt(u"[INFO] Presiona \"Ctrl + C\" para cancelar (Por partes)")
            printt(u"")
            
            printt(u"[?] Quieres descargar todas las partes? [s/n]:")
            opc = ""
            while opc != "s" and opc != "n":
                opc = raw_input()
                if opc is not "s" or opc is not "n":
                    printt(u"[!!!] [s/n]")
            
            if opc is "s":
                del i
                for i in range(0, len(self._URL)):
                    printt(u"[ Descargando %d parte ]" % (int(i) + 1))
                    printt(u"[ Destino ] %s" % self.outputName[i])
                    
                    command = "rtmpdump"
                    if sys.platform == "win32":
                        command += ".exe"
            
                    args = [command, "--resume", "-o", self.outputName[i], "-r", self._URL[i]]
                    if self._otros: args[len(args):] = self._otros
            
                    try:
                        printt(u"\nLanzando rtmpdump...\n")
                        out = None
                        err = 0
                        while out != 0:
                            out = subprocess.call(args)
                            if out == 0: # Descarga realizada con éxito
                                printt(u"[OK] Descarga realizada con éxito")
                            else:
                                err += 1
                                printt(u"\n[!!!] Se ha producido un error grave al descargar.")
                                printt(u"[INFO] Se intentará reiniciar la descarga pero no es seguro que funcione.")
                                printt(u"[INFO] Intentando reiniciar descarga en 3 segundos")
                                time.sleep(3)
                                if err == 5: salir(u"[!!!] Demasiados errores. Se aborta la descarga.")
                                if err == 2:
                                    remove(self.outputName[i])
                                    printt(u"\n[ERROR] El vídeo no se puede descargar con RTMPDUMP.")
                                    printt(u"[INFO]  Se intenta descargar con MPLAYER/MENCODER:")
                                    time.sleep(3)
                                    command = "mencoder"
                                    args =  [command, "-oac", "pcm", "-ovc", "copy", self._URL[i], "-o", self.outputName[i]]
#                    printt(u"\nLanzando rtmpdump...\n")
#                    out = None
#                    err = 0
#                    while out != 0:
#                        out = subprocess.call(args)
#                        if out == 2: # Error grave
#                            err += 1
#                            if err > 3:
#                                printt(u"\n[!!!] Demasiados errores.")
#                                time.sleep(2)
#                                printt(u"[INFO] Se intenta volver a descargar entero")
#                                time.sleep(2)
#                                printt(u"[INFO] Borrando", self.outputName[i])
#                                remove(self.outputName[i])
#                            if err > 5:
#                                printt(u"[!!!] ERROR irrecuperable. Se aborta la descarga. Sorry :(")
#                                break
#                                
#                            printt(u"\n[!!!] Se ha producido un error grave al descargar.")
#                            time.sleep(1)
#                            printt(u"[INFO] Se intentará reiniciar la descarga pero no es seguro que funcione.")
#                            time.sleep(1)
#                            printt(u"[INFO] Intentando reiniciar descarga en 3 segundos")
#                            time.sleep(3)
#                            
#                        if out == 0: # Descarga realizada con éxito
#                            pass
#                        else: # Error recuperable
#                            err += 1
#                            if err > 3:
#                                printt(u"\n[!!!] Demasiados errores.")
#                                time.sleep(2)
#                                printt(u"[INFO] Se intenta volver a descargar entero")
#                                time.sleep(2)
#                                printt(u"[INFO] Borrando", self.outputName[i])
#                                remove(self.outputName[i])
#                            if err > 5:
#                                printt(u"\n[!!!] ERROR irrecuperable. Se aborta la descarga. Sorry :(")
#                                err = 0
#                                break
#                                
#                            printt(u"\n[!!!] Se ha producido un error con Rtmpdump, se intenta recuperar...")
#                            time.sleep(1)
#                            printt(u"[INFO] Se reinicia en 3 segundos")
#                            time.sleep(3)
                    except OSError, e:
                        printt(u"[!!!] ERROR. No se encuenta rtmpdump o mplayer:", e)
                    except KeyboardInterrupt:
                        salir(u"Bye!")
            else:
                printt(u"\n[?] Qué partes quieres descargar?")
                printt(u"[INFO] Puedes introducir varias partes separadas por comas")
                
                ERROR = True
                while ERROR is True: 
                    ERROR = False
                    printt(u"[INFO] Partes:")
                    b = 1
                    for i in range(0, len(self._URL)):
                        printt(u"[Parte %s] %s" % (str(b), self._URL[i]))
                        b += 1
                    del b
                    printt(u"[?] --> ")
                    partes = raw_input()
                    partes = partes.split(",")
                    for i in partes:
                        if not i.isdigit():
                            printt(u"[!!!] ERROR. No se reconoce la parte \"%s\"" % i)
                            ERROR = True
                            break
                        if int(i) < 1 or int(i) > len(self._URL):
                            printt(u"[!!!] ERROR. La parte \"%s\" no existe" % int(i))
                            ERROR = True
                            break
                            
                printt(u"[OK] Se descargarán las partes")
                for i in partes:
                    printt(u"\n")
                    printt(u"[ Descargando %d parte ]" % (int(i)))
                    printt(u"[ Destino ] %s" % self.outputName[int(i)-1])
                    
                    command = "rtmpdump"
                    if sys.platform == "win32":
                        command += ".exe"
                    
                    args = [command, "--resume", "-o", self.outputName[int(i)-1], "-r", self._URL[int(i)-1]]
                    if self._otros: args[len(args):] = self._otros
                    
                    #for ss in args: print ss, 
        
                    try:
                        printt(u"\nLanzando rtmpdump...\n")
                        out = None
                        err = 0
                        while out != 0:
                            out = subprocess.call(args)
                            if out == 0: # Descarga realizada con éxito
                                printt(u"[OK] Descarga realizada con éxito")
                            else:
                                err += 1
                                printt(u"\n[!!!] Se ha producido un error grave al descargar.")
                                printt(u"[INFO] Se intentará reiniciar la descarga pero no es seguro que funcione.")
                                printt(u"[INFO] Intentando reiniciar descarga en 3 segundos")
                                time.sleep(3)
                                if err == 5: salir(u"[!!!] Demasiados errores. Se aborta la descarga.")
                                if err == 2:
                                    remove(self.outputName[int(i)-1])
                                    printt(u"\n[ERROR] El vídeo no se puede descargar con RTMPDUMP.")
                                    printt(u"[INFO]  Se intenta descargar con MPLAYER/MENCODER:")
                                    time.sleep(3)
                                    command = "mencoder"
                                    args =  [command, "-oac", "pcm", "-ovc", "copy", self._URL[int(i)-1], "-o", self.outputName[int(i)-1]]
#                        printt(u"\nLanzando rtmpdump...\n")
#                        out = None
#                        err = 0
#                        while out != 0:
#                            out = subprocess.call(args)
#                            if out == 2: # Error grave
#                                err += 1
#                                if err > 3:
#                                    printt(u"\n[!!!] Demasiados errores.")
#                                    time.sleep(2)
#                                    printt(u"[INFO] Se intenta volver a descargar entero")
#                                    time.sleep(2)
#                                    printt(u"[INFO] Borrando", self.outputName[int(i)-1])
#                                    remove(self.outputName[int(i)-1])
#                                if err > 5:
#                                    printt(u"[!!!] ERROR irrecuperable. Se aborta la descarga. Sorry :(")
#                                    break
#                                    
#                                printt(u"\n[!!!] Se ha producido un error grave al descargar.")
#                                time.sleep(1)
#                                printt(u"[INFO] Se intentará reiniciar la descarga pero no es seguro que funcione.")
#                                time.sleep(1)
#                                printt(u"[INFO] Intentando reiniciar descarga en 3 segundos")
#                                time.sleep(3)
#                                
#                            if out == 0: # Descarga realizada con éxito
#                                pass
#                            else: # Error recuperable
#                                err += 1
#                                if err > 3:
#                                    printt(u"\n[!!!] Demasiados errores.")
#                                    time.sleep(2)
#                                    printt(u"[INFO] Se intenta volver a descargar entero")
#                                    time.sleep(2)
#                                    printt(u"[INFO] Borrando", self.outputName[int(i)-1])
#                                    remove(self.outputName[int(i)-1])
#                                if err > 5:
#                                    printt(u"\n[!!!] ERROR irrecuperable. Se aborta la descarga. Sorry :(")
#                                    err = 0
#                                    break
#                                    
#                                printt(u"\n[!!!] Se ha producido un error con Rtmpdump, se intenta recuperar...")
#                                time.sleep(1)
#                                printt(u"[INFO] Se reinicia en 3 segundos")
#                                time.sleep(3)
                    except OSError, e:
                        printt(u"[!!!] ERROR. No se encuenta rtmpdump o mplayer:", e)
                    except KeyboardInterrupt:
                        salir(u"Bye!")
                        
                        print "\n"
            return
        
        ########### FIN RTMP  ###########################################################################################
                
        ########### MMS  ################################################################################################
        # Utilizar pylibmms si el protocoo es mms://
        if type(self._URL) != list and self._URL.startswith("mms://"):
            # Por ahora solo tengo libmms compilado para Mac OS X
            printt(u"")
            printt(u"DESCARGAR:")
            printt(u"----------------------------------------------------------------")
            printt(u"[ URL DE DESCARGA FINAL ]", self._URL)
            printt(u"[   DESTINO   ]", self.outputName)
            
            
            if sys.platform == "win32":
                msg = '''Protocolo MMS aun no disponible en Windows.
                La URL FINAL DE DESCARGA que se muestra, es la localización final del archivo.
                Puedes descargar el archivo mediante esta URL a través de algun gestor de
                descargas que soporte la descarga a través del protocolo mms://
                '''
                printt(msg)
                return
            
            try:
                from pylibmms import core as libmmscore
            except ImportError, e:
                print e
                salir(u"[!!!] ERROR al importar libmms")
            
            printt(u"\n[INFO] Presiona \"Ctrl + C\" para cancelar\n")
            options = [self._URL, self.outputName]
            libmmscore.run(options)
            
            return
            
        ########### FIN MMS  ############################################################################################
        
        ########### HTTP ################################################################################################
         
        #-->        ########## WINDOWS (NO PYAXEL) ##########
        # Solo en descara normal (para no utilizar pyaxel) por eso los protocolos rtmp:// y mms://
        # NO están incluídos aquí y están antes
        if sys.platform == "win32":
            self.descargarVideoWindows(self.outputName)
            return
        #-->        ######## FIN WINDOWS (NO PYAXEL) ########
        
        #-->        ######## UNIX (USANDO PYAXEL)  ##########
        
        printt(u"")
        printt(u"DESCARGAR:")
        printt(u"----------------------------------------------------------------")
        if type(self._URL) == list:
            b=1
            for i in self._URL:
                printt(u"[ URL DE DESCARGA FINAL ] [Parte %d] %s" % (b, i))
                b += 1
        else:
            printt(u"[ URL DE DESCARGA FINAL ]", self._URL)

        
        printt(u"[INFO] Presiona \"Ctrl + C\" para cancelar (Por partes)")
        printt(u"")
        if type(self._URL) == list:
            printt(u"[?] Quieres descargar todas las partes? [s/n]:")
            opc = ""
            while opc != "s" and opc != "n":
                opc = raw_input()
                if opc is not "s" or opc is not "n":
                    printt(u"[!!!] [s/n]")
            
            if opc is "s":
                for i in range(0, len(self._URL)):
                    printt(u"[Descargando %d parte]" % (int(i) + 1))
                    options = {"output_file": self._outputName[i], "verbose": True, "max_speed": None, "num_connections": 4}
                    pyaxel.download(self._URL[i], options)
                    print "\n"
            elif opc is "n":
                printt(u"\n[?] Qué partes quieres descargar?")
                printt(u"[INFO] Puedes introducir varias partes separadas por comas")
                
                ERROR = True
                while ERROR is True: 
                    ERROR = False
                    printt(u"[INFO] Partes:")
                    b = 1
                    for i in range(0, len(self._URL)):
                        printt(u"[Parte %s] %s" % (str(b), self._URL[i]))
                        b += 1
                    del b
                    printt(u"[?] --> ")
                    partes = raw_input()
                    partes = partes.split(",")
                    for i in partes:
                        if not i.isdigit():
                            printt(u"[!!!] ERROR. No se reconoce la parte \"%s\"" % i)
                            ERROR = True
                            break
                        if int(i) < 1 or int(i) > len(self._URL):
                            printt(u"[!!!] ERROR. La parte \"%s\" no existe" % int(i))
                            ERROR = True
                            break
                            
                printt(u"[OK] Se descargarán las partes")
                for i in partes:
                    printt(u"[Descargando %d parte]" % (int(i)))
                    options = {"output_file": self._outputName[int(i)-1], "verbose": True, "max_speed": None, "num_connections": 4}
                    pyaxel.download(self._URL[int(i)-1], options)
                    print "\n"
        else:
            options = {"output_file": self._outputName, "verbose": True, "max_speed": None, "num_connections": 4}
            pyaxel.download(self._URL, options)
        
        #-->        ###### FIN UNIX (USANDO PYAXEL)  ########
        ########### FIN HTTP ############################################################################################

        
        
        
    
