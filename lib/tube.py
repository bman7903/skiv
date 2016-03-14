import mechanize
from sys import argv
from bs4 import BeautifulSoup
from re import sub
from random import randint, seed
from time import sleep
from urllib import unquote

url  = 'https://www.youtube.com/watch?v=vjW8wmF5VWc'
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-agent', 'Mozilla/5.0')]
rsp = br.open(url)
data = rsp.read()
soup = BeautifulSoup(data)

for line in str( soup ).split('url='):
  line = str( line )
  if 'googlevideo' in line:
     line = str( str( unquote( line ) ).decode('utf-8') )
     print line
     print
