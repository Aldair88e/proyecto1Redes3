#!/usr/bin/env python

import rrdtool

def crearBD(nombre):
    ret = rrdtool.create(nombre + ".rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:inUcastPkts:COUNTER:120:U:U",
                     "DS:inPktsIp:COUNTER:120:U:U",
                     "DS:outEchoesICMP:COUNTER:120:U:U",
                     "DS:inSegsTCP:COUNTER:120:U:U",
                     "DS:inDatagrams:COUNTER:120:U:U",
                     "RRA:AVERAGE:0.5:1:24",
                     "RRA:AVERAGE:0.5:5:10")

    if ret:
        print (rrdtool.error())
