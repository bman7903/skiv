#!/usr/bin/env python
import mechanize
from bs4 import BeautifulSoup
from urllib import unquote
from re import sub, compile, findall
from sys import argv

UAS         = 'Mozilla/5.0'
global yrslt
yrslt = []

def Title( line ):
  title   = str(line).split('title="')[-1]
  title   = str(title).split('"_blank">')[-1]
  title   = str(title).split('"')[0]
  title   = str( sub('<a>','',title) )
  title   = str( sub('</a>','',title) )
  title   = str( sub('<b>','',title) )
  title   = str( sub('</b>','',title) )
  title   = str( sub('</h3>','',title) )
  title   = str( sub('</sup>','',title) )
  title   = str( sub('<sup>','',title) ).strip('|')
  title   = str( sub('|','',title) )
  title   = str( sub('-','_',title ) )
  title   = str( sub(':','',title ) )
  title   = str( sub(' ', '_', title ) ).strip()
  title   = str( sub('"','',title ) )
  title   = str( sub('__','',title ) )
  title   = str( sub(',', '', title ) ).strip()
  title   = str( sub("'","",title ) )
  title   = str( sub('_YouTube','', title ) )
  return title

def gparse( soup ):
  r1 = compile("http://r.search.yahoo.com")
  r2 = compile("r.msn.com")
  for item in (soup.select("h3")):
     string = str(item)
     ttle = str( Title( string ) )
     ttle = str( str( unquote(ttle) ).decode('utf-8') ).strip('|')
     a = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
     if a:
          string = str( a )
          if r1.search(string):
            stringnew = string.split("RU=")
            stringlink = str(stringnew[1])
            stringnew = stringlink.split("RK=")
            stringlink = str(stringnew[0])
            stringlink = unquote(stringlink).decode('utf-8')
            stringlink = sub( '//','/', stringlink)
            if r2.search(stringlink):
                pass
            else:
               stringlink = str( stringlink )
               if not 'gemini' in stringlink:
                  stringlink = str( sub( '//','/', stringlink ) )
                  stringlink = str( unquote(stringlink) ).decode()
                  new = str( stringlink + ' | ' + ttle)
                  new = str( unquote(new) ).decode('utf-8')
                  global yrslt
                  yrslt.append(new)
     else:
          pass

def Next( url, i, pages ):
     if i == pages:
        return
     i = i + 1
     br = mechanize.Browser(factory=mechanize.RobustFactory())
     br.set_handle_robots(False)
     br.set_handle_equiv(False)
     br.addheaders = [('User-agent', UAS)]
     data = br.open( url )
     soup = BeautifulSoup(data.read())
     gparse(soup)
     soup = str( soup )
     for e in soup.split('<a'):
       e = str( e )
       if 'class="next"' in str(e):
          url = str( sub(' class="next" href=', '', e ) )
          url = str( url.split('"')[1] )
          url = str( unquote(url) ).decode()
#          url = str( sub( '&amp;', '&', url ) )
          try:
             Next( url, i, pages )
          except:
             return

def ysearch( pages, Query ):
  url = 'https://search.yahoo.com'
  br = mechanize.Browser(factory=mechanize.RobustFactory())
  br.set_handle_robots(False)
  br.addheaders = [('User-agent', UAS)]
  r = br.open( url )
  html = r.read()
  br.select_form(nr=0)
  br.form['p'] = Query
  br.submit()
  soup = BeautifulSoup(br.response().read())
  gparse( soup )
  if pages > 1:
     soup = str( soup )
     for e in soup.split('<a'):
       e = str( e )
       if 'class="next"' in str(e):
          url = str( sub(' class="next" href=', '', e ) )
          url = str( url.split('"')[1] )
          url = str( unquote(url) ).decode()
#          url = str( sub( '&amp;', '&', url ) )
          Next( url, 1, pages )

  nrslt = []
  global yrslt
  i = 1
  lg = len( yrslt )
  for e in range(1, lg):
     g = str( yrslt[e] )
     e = str( e )
     z = str( e + ' | yahoo | ' + g )
     nrslt.append(z)
  return nrslt
