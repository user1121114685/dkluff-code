#!/usr/bin/env python
import random
vopen=11.81
c=330
while c>0:
    vh=vopen*(1+random.random()*0.1)
    vl=vopen*(1-random.random()*0.1)
    vclose=vl+(vh-vl)*random.random()
    print "{:.2f} {:.2f} {:.2f} {:.2f} ".format(vopen,vclose,vh,vl)
    vopen=vclose
    c-=1
