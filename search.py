#!/usr/bin/env python
import PyQt4
from subprocess import Popen, PIPE
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *

from sys import exit, argv
from os import path, mkdir, environ, remove, chdir
from time import sleep

exist  = path.exists
join   = path.join
sep    = path.sep
exist  = path.exists

Pth     = path.dirname(path.abspath(__file__))
Img     = join( sep, Pth, 'img' )
Icn     = join( sep, Img, 'icn' )
Lib     = join( sep, Pth, 'lib' )
Show    = join( sep, Pth, 'show.py' )
Srch    = join( sep, Pth, 'srch' )
Skiv    = join( sep, Srch, 'skiv.py' )
BGR     = join( sep, Img, 'search.png' )
ICN     = join( sep, Icn, 'black.png' )

PTH     = Pth
Py      = '/usr/bin/python'
GR      = "background-color:rgba(255, 255, 0, 0); color:rgba(128, 8, 0, 255);"

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
if exist( trslt ) == True:
  remove( trslt )

font = QtGui.QFont("URW Chancery L")
font.setBold(True)
font.setItalic(True)
font.setWeight(100)

class Transparent(QtGui.QWidget):
  def __init__(self):
     QtGui.QWidget.__init__(self)
     self.setAttribute(Qt.WA_NoSystemBackground)
     self.setAutoFillBackground(True)
     self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
     pixmap = QtGui.QPixmap(BGR)
     width  = pixmap.width()
     height = pixmap.height()
     self.setWindowTitle("Search")
     self.resize(width, height)
     self.label = QtGui.QLabel(self)
     self.label.setPixmap(QtGui.QPixmap(BGR))
     self.setMask(pixmap.mask())
     self.label.mouseReleaseEvent = self.OnMouseDown
     palette = QtGui.QPalette()
     palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)

     self.srch_e = QtGui.QLineEdit(self)
     self.srch_e.setAutoFillBackground(True)
     self.srch_e.setStyleSheet( GR )
     self.srch_e.setGeometry(QtCore.QRect(25, 25, 280, 25))
     self.srch_e.setObjectName('bEdit')
     self.srch_e.setFont(font)
     self.srch_e.move( 130,30 )
     self.connect(self.srch_e, QtCore.SIGNAL("textChanged(QString)"), self.srch_chosen)

  def srch_chosen(self, chosen): 
     print( chosen )
     global srch
     srch = chosen
     return srch

  def Proc( self, x, y ):
     print( str(x) + ' ' + str(y) )
     if x > 20 and x < 70 and y > 20 and y < 60:
       global srch
       srch = str( str(srch) + '\n' )
       a = open( tfile, 'w' )
       a.write( srch )
       a.close()
       chdir( Srch )
       p = Popen([Py,Skiv], stdout = PIPE)
       out , err = p.communicate()
       print( out )
       chdir( PTH )
       sleep( 2 )
       p = Popen([Py,Show], stdout = PIPE)
       out, err = p.communicate()
       print( out )
     else:
       exit()

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
     x = ebvent.pos().x()
     y = event.pos().y()
     pos = str( str(x) + ' ' + str(y) )

  def OnMouseDown( self, event ):
     pass

  def Exit( self ):
     sys.exit()

if __name__ == "__main__":
     app = QtGui.QApplication(argv)
     app.setWindowIcon(QtGui.QIcon(ICN))
     x = Transparent()
     x.move(0, 0)
     x.show()
     app.exec_()


