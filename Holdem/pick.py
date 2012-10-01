#!/usr/bin/python
import sys

def Pick(k,kmax,n,inList):
#    print k, inList

    if k==kmax:
        for i in range(1,n+1):
            inList[k-1]=i
            Pick(k-1, kmax, n, inList)        
    if (k>0) & (k<kmax):
#        print 'here %d %d' % (k, kmax)
        for i in range(inList[k]+1,n+1):
            inList[k-1]=i
            Pick(k-1, kmax, n, inList)
        
    if k==0:
        print inList



inList=[0, 0, 0, 0, 0]
Pick(5,5,7,inList)
