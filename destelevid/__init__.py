#!/usr/bin/python
# -*- coding: utf-8-*-
class downloader():
    def __init__(self,url):
        self.url = url
    def conseguirUrlVideo(self):
        try:
            url = self.url.split('/')[2]
        except IndexError:
            return [u"No es una dirección",1]
        if url.find('rtve.es') != -1:
            """rtve.es/alacarta"""
            return [self.rtvees(self.url),0]
        elif url.find('mitele.es') != -1:
            """[PyDownTV]Mi Tele(Mediaset)"""
            return [self.mitele(self.url),0]
        elif url.find('rtvv') != -1:
            """rtvv"""
            return [self.rtvv(self.url),0]
        else:
            return [u"La dirección que has introducido no está en los servicios soportados",1]
    def rtvees(self,url):
        from rtvees import rtvees_alacarta
        return rtvees_alacarta().descifrarUrl(url)
    def rtvv(self,url):
        from rtvv import rtvv_mediateca
        return rtvv_mediateca().descifrarUrl(url)
    def mitele(self,url):
        print "MiTele"
        from mitele import MiTele
        #mitele = MiTele(url)
        #mitele.setUrl(url)
        #return mitele.procesarDescarga()[0]
        return MiTele(url).procesarDescarga()[0]
    def nada(self):
        print "Nada"
