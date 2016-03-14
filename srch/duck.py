#!/usr/bin/env python
import mechanize
from sys import argv
from bs4 import BeautifulSoup
from re import sub
from random import randint, seed
from time import sleep
from urllib import unquote
seed()

avgTime = 3
Time = ( avgTime * 2)
UAS = 'Mozilla/5.0'

global drslt
drslt = []

def Title( line ):
  line   = str( line )
  title  = str( sub( '<a>', '', line ) )
  title  = str( sub( '</a>', '', title ) )
  title  = str( sub( '<b>', '', title ) )
  title  = str( sub( '</b>', '', title ) )
  title  = str( sub( '<span>', '', title ) )
  title  = str( sub('&amp;', '&', title ) )
  title = str( sub('-','_',title ) )
  title = str( sub(':','',title ) )
  title = str( sub(' ', '_', title ) ).strip()
  title = str( sub('"','',title ) )
  title = str( sub('__','',title ) )
  title = str( sub(',', '', title ) ).strip()
  title = str( sub("'","",title ) )
  title = str( sub('_YouTube','', title ) )
  title  = str( sub( '</span>', '', title ) ).strip('|')
  return title

def gparse( soup ):   
   for line in str( soup ).split('\n'):
      line = str( line )

      if not '<a rel="' in line:
        if 'class="large"' in line:
           line = str( 'h' + str( line.strip('<a class="large" href=') )) 
           url = str( line.split('"')[0] )
           url = str( unquote(url) ).decode('utf-8') 
  #           url = str( sub('&amp;', '&', url ) )
           ttl = line.split('nofollow">')[-1]
           ttl = str( Title( ttl ) )
           ttl = str( unquote(url) ).decode('utf-8')
           z = str( url + ' | ' + ttl )
           global drslt
           drslt.append(z)

      if '<a rel="' in line:
        if '<b>' in line:
           url = str( line.split('href=')[-1] )
           url = str( url.split('"')[1] )
           url = str( sub('&amp;', '&', url ) )
           ttl = str( line.split('">')[-1] )
           ttl = str( Title( ttl ) )
           z = str( url + ' | ' + ttl )
           global drslt
           drslt.append(z)


def Next( br, i, pages ):
     if i == pages:
       return

     i = i + 1
     t = randint(1, Time)
     sleep(t)
     pag2 = br.submit()
     html = pag2.read()
     gparse( html )
     try:
       br.select_form(nr=2)
       Next( br, i, pages )
     except:
       pass

def dsearch( pages, Query ):
  url  = 'https://duckduckgo.com/html/'
  br = mechanize.Browser(factory=mechanize.RobustFactory())
  br.set_handle_robots(False)
  br.set_handle_equiv(False)
  br.addheaders = [('User-agent', UAS)]
  br.open(url)
  br.select_form(name="x")
  br["q"] = Query
  rsp = br.submit()
  data = rsp.read()
  soup = BeautifulSoup(data)
  gparse( soup )
  if pages > 1:
     br.select_form(nr=2)
     Next( br, 1, pages )

  nrslt = []
  global drslt
  lg = len( drslt )
  for e in range(1, lg):
     g = str( drslt[e] )
     e = str( e )
     z = str( e + ' | duck | ' + g )
     nrslt.append(z)
  return nrslt

