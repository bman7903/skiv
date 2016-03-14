 #!/usr/bin/env python

import mechanize
from bs4 import BeautifulSoup
from re import sub
from urllib import unquote
from random import seed, randint
from time import sleep
seed()

avgTime = 3
Time = ( avgTime * 2)
UAS = 'Mozilla/5.0'

global brslt
brslt = []

def Title( line ):
  title   = str(line).split('title="')[-1]
  title   = str(title).split('"_blank">')[-1]
  title   = str(title).split('"')[0]
  title   = str( sub('<a>','',title) )
  title   = str( sub('</a>','',title) )
  title   = str( sub('<b>','',title) )
  title   = str( sub('</b>','',title) )
  title   = str( sub('</h2>','',title) )
  title   = str( sub('<strong>','',title) )
  title   = str( sub('</strong>','',title) )
  title   = str( sub('<h2>','',title) ).strip('|')
  title   = str( sub('-','_',title ) )
  title   = str( sub(':','',title ) )
  title   = str( sub(' ', '_', title ) ).strip()
  title   = str( sub('"','',title ) )
  title   = str( sub('__','',title ) )
  title   = str( sub(',', '', title ) ).strip()
  title   = str( sub("'","",title ) )
  title   = str( sub('_YouTube','', title ) )
  return title

def plink( link ):
  link = str( link )
  if 'href' in link:
    if '://' in link:
       bad   = 'microsoft.com r.msn.com bing'
       for b in bad.split(' '):
          b  = str( b )
          if b in link:
            return

       title = str( link.split('">')[-1] )
       title = str( Title( title ) ).strip('|')
       title = str( unquote(title) )#.decode('utf-8')
       if 'bing' in title:
          return

       url   = str( link.split('href="')[-1] ).split('"')[0]
       url   = str( unquote(url) )#.decode('utf-8')
#       url   = str( sub('&amp;','&', url ) )
       z = str( url + ' | ' + title  )#.decode('utf-8')
       global brslt
       brslt.append( z )

def Next( url, i, pages ):
  i = i + 1
  br = mechanize.Browser(factory=mechanize.RobustFactory())
  br.set_handle_robots(False)
  br.set_handle_equiv(False)
  br.addheaders = [('User-agent', UAS)]
  data = br.open( url )
  soup = BeautifulSoup(data.read())
  for item in (soup.select("h2")):
     plink(item)
  for item in(soup.select("a")):
     plink(item)
  if i == pages:
     return
  soup = str( soup )
  for b in soup.split('"'):
     b = str( b )
     if 'PORE' in b:
       url = str( 'https://bing.com' + str(b) )
       url = str( unquote(url) ).decode('utf-8')
       Next( url, i, pages )

def bsearch( pages, Query ):
  baselink = 'https://bing.com'
  br = mechanize.Browser(factory=mechanize.RobustFactory())
  br.set_handle_robots(False)
  br.addheaders = [('User-agent', UAS)]
  r = br.open(baselink)
  html = r.read()
  br.select_form(nr=0)
  br.form['q'] = Query
  br.submit()
  soup = BeautifulSoup(br.response().read())
  for item in (soup.select("h2")):
     plink(item)       
  for item in(soup.select("a")):
     plink(item)
  if pages > 1:
     soup = str( soup )
     for b in soup.split('"'):
       b = str( b )
       if 'PORE' in b:
           url = str( baselink + str(b) )
           url = str( unquote(url ) )#.decode('utf-8') )
           Next( url, 1, pages )

  nrslt = []
  global brslt
  lg = len( brslt )
  for e in range(1, lg):
      g = str( brslt[e] )
      e = str( e )
      z = str( e + ' | bing | ' + g ).decode('utf-8')
      nrslt.append(z)
  return nrslt

