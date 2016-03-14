import mechanize
from bs4 import BeautifulSoup
from re import sub
from random import seed, randint
from re import sub
from time import sleep
from urllib import unquote
from sys import argv
from os import path, environ, mkdir, chdir, remove
seed()

avgTime = 3
Time    = ( avgTime * 2)
UAS     = 'Mozilla/5.0'

join    = path.join
sep     = path.sep
exist   = path.exists

def checkPath( localpath ):
  if not exist( localpath ):
     try:
       mkdir( localpath )
     except:
       print( 'Error creating ' + str( localpath ) )

global Home, dwnd, urlz
Home    = join( sep, str( environ['HOME'] ), '.youtube' )
dwnd    = join( sep, str( environ['HOME'] ), 'Downloads' )
urlz    = []

for d in 'Home dwnd'.split(' '):
  t = eval( d )
  checkPath( t )
  if not exist( d ):
     d = '/tmp'
print('download dir ' + dwnd )

srch   = join( sep, Home, 'search.tmp' )
rslt   = join( sep, Home, 'resaults.tmp' )

def gparse( soup ):
       base = 'https://www.youtube.com'
       soup = str( soup )
       for e in soup.split('h3 class="yt-lockup-title'):
           e = str( e )
           if e.startswith(' "><a') == True:
              id      = str( e.split('data-context-item-id=')[-1] )
              id      = str( id.split('"')[1] ) 
              title   = str( e.split('title=')[1] )
              title   = str( title.split('"')[1] )
              title   = str( sub(r'\W+', '', title ) )
              watch   = str( base + '/watch?v=' + id )
              ag      = str( e.split('"yt-lockup-meta-info"><li>')[-1] )
              age     = str( ag.split('</li>')[0] )
              user    = str( e.split(' href="/user')[-1] )
              user    = str( user.split('"')[0] ).strip('/')
              views   = str( sub('</li><li>','', ag ) ).split('</')[0]
              views   = str( sub(age,'',views ) )
              if not 'views' in views:
                views = 'err'
              if len( views ) > 12:
                views = 'err'
              if len( user ) < 4:
                user  = 'None'
              if len( age ) > 12:
                age   = 'err'
              time    = str( e.split('video-time">')[-1] )
              time    = str( time.split('</')[0] )
              thumb   = str( 'https://i.ytimg.com/vi/' + id + '/mqdefault.jpg' )
              if not '<' in id:
                 z    = str( id + '|' + title + '|' + watch + '|' + thumb + '|' + views + '|' + age + '|' + time + '|' + user)
                 global urlz
                 urlz.append( z )

def Next( url, i, pages ):
  base = 'https://www.youtube.com'
  i = i + 1
  br = mechanize.Browser(factory=mechanize.RobustFactory())
  br.set_handle_robots(False)
  br.set_handle_equiv(False)
  br.addheaders = [('User-agent', UAS)]
  data = br.open( url )
  soup = BeautifulSoup(data.read())
  gparse(soup)
  if i == pages:
     return
  soup = str( soup )
  for a in soup.split('href='):
     a = str( a )
     strn = str( 'page=' + str( i ) )
     if strn in a:
        b = str( a.split('"')[1] )
        b = str( sub('&amp;','&',b) )
        url = str( base + b )
        Next( url, i, pages )
        break

def gsearch( pages, Query ):
    Query = str( Query )
    Query = str( sub(' ', '+', Query ) )
    base = 'https://www.youtube.com'
    url = str( base + '/results?search_query=' + Query )
    print( url )
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.set_handle_robots(False)
    br.set_handle_equiv(False)
    br.addheaders = [('User-agent', UAS)]
    data = br.open( url )
    soup = BeautifulSoup( data.read() )
    gparse( soup )
    if pages > 1:
     i = 2
     soup = str( soup )
     for a in soup.split('href='):
        a = str( a )
        strn = str( 'page=' + str( i ) )
        if strn in a:
            b = str( a.split('"')[1] )
            b = str( sub('&amp;','&',b) )
            url = str( base + b )
            Next( url, i, pages )
            break


Query = ''
for a in argv:
  a = str(a)
  if not 'None' in a:
     if not 'youtube.py' in a:
       Query = str( str( Query + ' ' + a ).strip() )
gsearch(1, Query )

global urlz
for e in urlz:
   print(e)
