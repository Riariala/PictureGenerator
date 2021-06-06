import configparser
import sys
import os

class Config():

    def read():
        configal = configparser.RawConfigParser()
        configFilePath = 'configfiles/settings.ini'
        configal.read(configFilePath)
        x = configal.get('info',"SizeX")
        y = configal.get('info',"SizeY")
        MutationChance  = configal.get('info',"MutationChance")
        Howmuch = configal.get('info',"Howmuch")
        Ellipse = configal.get('info',"Ellipse")
        Rect = configal.get('info',"Rect")
        Lines = configal.get('info',"Lines")
        return [x, y, MutationChance, Howmuch, Ellipse, Rect, Lines]