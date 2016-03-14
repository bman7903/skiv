#!/usr/bin/env python
from sys import argv
from google import gsearch
from yahoo import ysearch
from bing import bsearch
from duck import dsearch
import subprocess
from os import path, mkdir, environ, remove
from time import sleep

join   = path.join
sep    = path.sep
exist  = path.exists

global rslt
rslt = []

def checkPath( localpath ):
  if not exist( localpath ):
     try:
       mkdir( localpath )
     except:
       print( 'Error creating ' + str( localpath ) )

global Home, project

Home    = join( sep, str( environ['HOME'] ), '.skiv' )
checkPath( Home )

if not exist( Home ):
  global Home
  Home  = environ['HOME']
  if not exist( Home ):
     Home = environ( '/tmp' )

Tmp     = join( sep, Home, 'tmp' )
Cache   = join( sep, Home, 'cache' )
dirs    = 'Home Tmp Cache'
for d in dirs.split(' '):
   f = eval( d )
   checkPath( f )

tfile   = join( sep, Tmp, 'search.tmp' )
trslt   = join( sep, Tmp, 'resaults.tmp' )
snew    = join( sep, Tmp, 'snew.tmp' )
if exist( trslt ) == True:
  remove( trslt )


p = subprocess.Popen(['/usr/bin/touch', trslt ], stdout = subprocess.PIPE)
output, err = p.communicate()
print( output )

def Search( s, i, Query):
  Query = str( Query )
  t = str( str(s) + 'search(' + str(i) + ', "' + Query + '")' )
  try:
     z = eval(t)
     for e in z:
        e = str( e + '\n' )
        with open( trslt, 'a' ) as a:
           a.write( e )
        a.close()
  except:
     print( 'Problem with ' + str(t) )

def All( i, Query ):
  types = 'b d g y'
  Query = str( Query ).strip()
  for t in types.split(' '):
    Search( t, i, Query )

i = 1
a = open( tfile, 'r' )
for Query in a.readlines():
  All( i, Query )
  break

def bash(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')


cat = '/bin/cat'
mv  = '/bin/mv'
sort = '/usr/bin/sort'

proc1 = str( cat + ' ' + trslt + '|' + sort + ' -g > ' + snew )
proc2 = str( mv + ' ' + snew + ' ' + trslt )
for e in 'proc1 proc2'.split(' '):
  e = eval( e )
  bash( e )
