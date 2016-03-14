#!/usr/bin/env python
import subprocess, PyQt4
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *

from sys import exit, argv
from os import path, mkdir, environ, remove
from time import sleep
from urllib import unquote
from re import sub

join   = path.join
sep    = path.sep
exist  = path.exists

Pth    = path.dirname(path.abspath(__file__))
Img    = join( sep, Pth, 'img' )
Icn    = join( sep, Img, 'icn' )
Lib    = join( sep, Pth, 'lib' )
BGR    = join( sep, Img, 'box.png' )
ICN    = join( sep, Icn, 'mask.png' )
oogle  = join( sep, Icn, 'ogle.png' )
ahoo   = join( sep, Icn, 'ahoo.png' )
duck   = join( sep, Icn, 'duck.png' )
tube   = join( sep, Icn, 'tube.png' )
bing   = join( sep, Icn, 'ing.png' )
script = join( sep, Icn, 'script.png' )
pdf    = join( sep, Icn, 'pdf.png' )
git    = join( sep, Icn, 'git.png' )
ytube  = join( sep, Lib, 'youtube.py' )

PTH     = Pth
Py      = '/usr/bin/python'
PY      = "color:rgba(255, 132, 0, 255); background-color:rgba(75, 0, 130, 0);"
GR      = "color:rgba(200, 6, 0, 255); background-color:rgba(75, 0, 130, 0);"
scripts = '.py .pl .rb .exe .vb .sh .bsh .csh .js .cpp .c .h .deb .rpm .pkg .apkg'

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

font = QtGui.QFont("URW Chancery L")
font.setBold(True)
font.setWeight(75)
font1 = QtGui.QFont("URW Chancery L")
font1.setBold(True)
font1.setItalic(True)
font1.setWeight(100)

def bash(cmd):
  print(cmd)
  subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)

class Transparent(QtGui.QWidget):
  def __init__(self):
     QtGui.QWidget.__init__(self)
     self.setAttribute(Qt.WA_NoSystemBackground)
     self.setAutoFillBackground(True)
     self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
     pixmap = QtGui.QPixmap(BGR)
     width = pixmap.width()
     height = pixmap.height()
     self.setWindowTitle("Resaults")
     self.resize(width, height)
     self.label = QtGui.QLabel(self)
     self.label.setPixmap(QtGui.QPixmap(BGR))
     self.setMask(pixmap.mask())
     self.label.mouseReleaseEvent = self.OnMouseDown
     palette = QtGui.QPalette()
     palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)

     global model_a
     model_a = QStandardItemModel()
     self.search_resaults()
     self.rslt_v = QListView(self)
     self.rslt_v.setStyleSheet( PY )
     self.rslt_v.move(80, 275)
     self.rslt_v.resize(255,245)
     self.rslt_v.setModel( model_a )
     self.rslt_v = model_a
     model_a.connect(model_a, SIGNAL("itemChanged(QStandardItem *)"), self.rsltChanged)


  def Title( self, line ):
     tl = str( line )
     tl = str( sub('-','_',tl ) )
     tl = str( sub(':','',tl ) )
     tl = str( sub(' ', '_', tl ) ).strip()
     tl = str( sub('"','',tl ) )
     tl = str( sub('__','',tl ) )
     tl = str( sub(',', '', tl ) ).strip()
     tl = str( sub("'","",tl ) )
     tl = str( sub('_YouTube','', tl ) )
     return tl

  def dwn( self ):
     global urlz
     for u in urlz:
       url = str( str( u ).split('|')[0] )
       tl = str( str( str( u ).split(url)[-1] ).strip('| ') )
       tl = str( self.Title( tl ) )
       if 'youtube.com/watch' in url:
          proc = str( Py + ' ' + ytube + ' "' + url + '"  "' + tl + '"' )
          bash( proc )
       print(tl)

  def bws( self ):
     from webbrowser import open
     global urlz
     for u in urlz:
       url = str( str( u ).split('|')[0] )
       new = 2
       url = str( url )
       open(url,new=new)

  def search_resaults( self ):
     global model_a
     t = open( trslt, 'r' )
     for line in t.readlines():
       line = str( line ).decode('utf-8')
       if '|' in line:
          icn  = str( line.split('|')[1] ).strip()
          ic   = str(  icn + ' | ' )
          line = str( line.split( ic )[-1] )
          item = QStandardItem(line)
          check = Qt.Unchecked
          if 'google' in icn:
              ayecon = QIcon( oogle )
          if 'yahoo' in icn:
              ayecon = QIcon( ahoo )
          if 'bing' in icn:
              ayecon = QIcon( bing )
          if 'duck' in icn:
              ayecon = QIcon( duck )
          if 'youtube.com/watch' in line:
              ayecon = QIcon( tube )
          if line.endswith('.pdf') == True:
              ayecon = QIcon( pdf )
          if line.endswith('.git') == True:
              ayecon = QIcon( git ) 
          for s in scripts.split(' '):
              s = str( s )
              if line.endswith( s ) == True:
                 ayecon = QIcon( script )
          item.setIcon( ayecon )
          item.setCheckState(check)
          item.setCheckable(True)
          item.setFont(font)
          item.setSizeHint(QSize(125, 20))
          model_a.appendRow( item )

  def Proc( self, x, y ):
     print( str(x) + ' ' + str(y) ) 
     if x > 20 and x < 80 and y > 610 and y < 680:
       exit()
     if x > 25 and x < 60 and y > 190 and y < 245:
       print( 'Who' )
     if x > 380 and x < 645 and y > 605 and y < 680:
       print( 'Settings' )
     if x > 390 and x < 450 and y > 495 and y < 545:
       self.dwn()
     if x > 385 and x < 455 and y > 360 and y < 410:
       print( 'Stream' )
     if x > 380 and x < 455 and y > 175 and y < 255:
       print( 'Browse' )
       self.bws()


  def mousePressEvent(self, event):
     x = event.pos().x()
     y = event.pos().y()
     self.Proc( x, y )
     if (event.button() == QtCore.Qt.LeftButton):
         self.drag_position = event.globalPos() - self.pos();
     event.accept();

  def mouseMoveEvent(self, event):
     if (event.buttons() == QtCore.Qt.LeftButton):
           self.move(event.globalPos().x() - self.drag_position.x(),
            event.globalPos().y() - self.drag_position.y());
     event.accept();

  def paintEvent(self,event):
     self.setAttribute(Qt.WA_NoSystemBackground)

  def getPos(self , event):
     x = event.pos().x()
     y = event.pos().y()
     pos = str( str(x) + ' ' + str(y) )
     print( pos )

  def OnMouseDown( self, event ):
     pass

  def rsltChanged(self, item):
     global urlz, model_a
     urlz = []
     for row in range(model_a.rowCount()):
       item = model_a.item(row, 0)
       J=(str(item.text())).decode('utf-8', 'ignore')
       if item.checkState() == Qt.Checked:
           if not J in str( urlz ):
               global urlz
               urlz.append( J )
     for e in urlz:
        print( e )

  def Exit( self ):
     sys.exit()

if __name__ == "__main__":
     app = QtGui.QApplication(argv)
     app.setWindowIcon(QtGui.QIcon(ICN))
     x = Transparent()
     x.move(0, 0)
     x.show()
     app.exec_()
