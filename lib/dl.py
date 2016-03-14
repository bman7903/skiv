#!/usr/bin/env python

import requests,sys,getpass
import logging
from os import environ, chdir, path, mkdir
from subprocess import Popen, PIPE

join  = path.join
sep   = path.sep
exist = path.exists

Pth    = path.dirname(path.abspath(__file__))
h2t    = join( sep, Pth, 'h2t.py' )
Py     = '/usr/bin/python'

def checkPath( localpath ):
  if not exist( localpath ):
     try:
       mkdir( localpath )
     except:
       print( 'Error creating ' + str( localpath ) )

global Home, project
Home    = str( environ['HOME'] )
#Home    = join( sep, home, 'Downloads' )   
checkPath( Home )
if not exist( Home ):
  global Home
  Home  = home
  if not exist( Home ):
     Home = environ( '/tmp' )
ARGS  = sys.argv
lA    = ( len( ARGS ) - 1 )
Usage = './download.py <url>'

def Exit():
  print( Usage )
  sys.exit()
if lA < 1:
  Exit()

pics  = join( sep, Home, 'Pictures' )
vids  = join( sep, Home, 'Videos' )
music = join( sep, Home, 'Music' )
dwnld = join( sep, Home, 'Downloads' )
docs  = join( sep, Home, 'Documents' )

for d in 'pics vids music dwnld docs'.split(' '):
   d = eval(d)
   checkPath( d )

DOCS  = 'txt pdf py doc bin c h pl rb torrent magnet'
VIDS  = 'mov mp4 avi mpg mpeg mkv swf wmv webm'
MUSIC = 'midi mp3 m4u ogg'
PICS  = 'png jpeg jpg bmp gif icn icon'


UAS   = {'User-Agent':' Mozilla/5.0'}
url   = sys.argv[1]
global local_filename
local_filename = str( str(url).split('/')[-1] )
global odir
odir = ''
chdir( Home )

print('Downloading ' + local_filename )

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1
logging.basicConfig() 
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

def getHTML( url ):
  url = str( url )
  doc = str( url.split('/')[-1] )
  print( 'Fetching HTML to Documents' )
  odoc = str( join( sep, docs, doc ) )
  chdir( docs )
  p = Popen( [Py,h2t,url], stdout = PIPE )
  output , err = p.communicate()
  output = str( output )
  g = open(odoc,'w')
  g.write( output )
  g.close()
  exit()

def Head( z, url ):
  z = str( z )
  print( 'value ' + z )
  print
  if 'image' in z:
     print( 'Downloading Image' )
     global odir
     odir = pics
  if 'html' in z:
     getHTML( url )
  for d in VIDS.split(' '):
     if d in z:
        global odir
        odir = vids
        return
  for d in DOCS.split(' '):
     if d in z:
        global odir
        odir = docs
        return
  for d in PICS.split(' '):
     if d in z:
        global odir
        odir = pics
        return
  for d in MUSIC.split(' '):
     if d in z:
        global odir
        odir = music
        return
  global odir
  odir = dwnld



def Download( url, r ):
    global local_filename

    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename

def file( url ):
    try:
       r = requests.get(url, stream=True , headers=UAS)
       g = str( r.raise_for_status() )
       h = r.headers
       for key, value in h.iteritems():
          z = ( key + ' ' + value )
          if 'content-type' in z:
              Head( z, url )          
       global odir
       if exist( odir ) == True:
          chdir( odir)
          print( 'to dir ' + str(odir) )
       Download( url, r )
    except requests.exceptions.ConnectionError as e:
       print("These aren't the domains we're looking for.")
       print(e)

file( url )
