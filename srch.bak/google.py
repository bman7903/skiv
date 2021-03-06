import mechanize
from bs4 import BeautifulSoup
from re import sub
from random import seed, randint
from time import sleep
seed()

avgTime = 3
Time = ( avgTime * 2)
UAS = 'Mozilla/5.0'

global grslt
grslt = []

def Title( line ):
  line   = str( line )
  title  = str( line.split('">')[1] )
  title  = str( sub( '<a>', '', title ) )
  title  = str( sub( '</a>', '', title ) )
  title  = str( sub( '<b>', '', title ) )
  title  = str( sub( '</b>', '', title ) ).strip('|')
  return title

def gparse( soup ):
   for line in soup.select('.r a'):
      line   = str( line )
      url    = str( str( line.split('"')[1] ).strip('/url?q=') )
#      url    = str( sub('&amp;','&', url ) )
      url = str( unquote(url) ).decode('utf-8')
      title  = str( Title( line ) )
      title = str( unquote(title) ).decode('utf-8')
      z = str( url + ' | ' + title  )
      global grslt
      grslt.append( z )      

def Next( url, i, pages ):
  if i == pages:
     return
  i = i + 1
  br = mechanize.Browser()
  br.set_handle_robots(False)
  br.set_handle_equiv(False)
  br.addheaders = [('User-agent', UAS)]
  data = br.open( url )
  soup = BeautifulSoup(data.read())
  gparse(soup)
  soup = str( soup )
  for a in soup.split('"'):
     aye = str( 'start=' + str(i) + '0' )
     if aye in str(a):
       url = str( 'https://encrypted.google.com' + str(a) )
       Next( url, i, pages )

def gsearch( pages, Query ):
    url = 'https://encrypted.google.com'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_equiv(False)
    br.addheaders = [('User-agent', UAS)]
    br.open( url )
    br.select_form(name='f')
    br.form['q'] = Query
    data = br.submit()
    soup = BeautifulSoup(data.read())
    gparse( soup )
    if pages > 1:
     soup = str( soup )
     for a in soup.split('"'):
       aye = str( 'start=10' )
       if aye in str(a):
          url = str( url + str(a) )
          Next( url, 1, pages )

    nrslt = []
    global grslt
    lg = len( grslt )
    for e in range(1, lg):
       g = str( grslt[e] )
       e = str( e )
       z = str( e + ' | google | ' + g )
       nrslt.append(z)
    return nrslt

