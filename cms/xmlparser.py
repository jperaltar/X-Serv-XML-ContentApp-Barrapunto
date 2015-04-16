#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.Content = ""
        self.Html = ""
        self.Title = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title' or name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.Title += self.Content
                # To avoid Unicode trouble
                self.inContent = False
                self.Content = ""
            elif name == 'link':
                self.Html += ("<a href='" + self.Content + "'>"
                        + self.Title + "</a><br/>\n")
                self.inContent = False
                self.Content = ""
                self.Title = ""

    def characters (self, chars):
        if self.inContent:
            self.Content = self.Content + chars
            
# --- Main prog
def getNews():  
    # Load parser and driver

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    # Ready, set, go!

    theParser.parse("http://barrapunto.com/index.rss")
    return "<br/>News:<br/>" + theHandler.Html