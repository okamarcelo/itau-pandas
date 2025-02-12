import logging as l
import os
import sys

def getLogger(name):
    console = l.StreamHandler(sys.stdout)
    console.setLevel(l.INFO)
    formatter = l.Formatter('%(name)-13s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    l.getLogger().addHandler(console)
    return l.getLogger("app." + name)