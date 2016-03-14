#!/usr/bin/env python

import sys, subprocess, os, pwd, re
from PyQt4 import QtCore, QtGui, QtNetwork
Pth    = os.path.dirname(os.path.abspath(__file__))
Rnt    = os.path.abspath( os.path.join( Pth, os.pardir ) )
Lib    = os.path.join( os.path.sep, Pth, 'lib' )
Img    = os.path.join( os.path.sep, Rnt, 'img' )
Tmp    = os.path.join( os.path.sep, Rnt, 'tmp' )
Dl     = os.path.join( os.path.sep, Pth, 'dl.py' )
Lck    = os.path.join( os.path.sep, Tmp, 'dwn.lck' )
Tdl    = 'youtube-dl'

font   = QtGui.QFont("eufm10")
font.setBold(True)
font.setWeight(125)
GY = "color:rgba(120, 6, 66, 255); background-color:rgba(255, 165, 0, 175);"

ARGS =  sys.argv
lA   =  ( len( ARGS ) - 1 )

def Usage():
  print( 'Usage: ./youtube.py url filename' )
  sys.exit()

if lA < 2:
  Usage()

global qual
qual = 'best'
global url
url     = sys.argv[1]
global l_file
l_file  = str( str(sys.argv[2]) + '.mp4' )

def bash(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')

def Exit():
    sys.exit()

class Downloader(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet( GY )
        logoicon = QtGui.QIcon(os.path.join( os.path.sep, Img, 'dwn.png'))
        self.setWindowIcon (logoicon)
        self.urlLineEdit = QtGui.QLineEdit( url )
        self.urlLineEdit.setFont( font )    

        self.urlLabel = QtGui.QLabel(self.tr("&URL:"))
        self.urlLabel.setBuddy(self.urlLineEdit)
        self.urlLabel.setFont( font )
        self.connect(self.urlLineEdit, QtCore.SIGNAL("textChanged(QString)"), self.update_url)
        self.statusLabel = QtGui.QLineEdit(self.tr(l_file))
        self.statusLabel.setGeometry(QtCore.QRect(9, 20, 125, 20))
        self.statusLabel.setObjectName(("statusLabel"))
        self.statusLabel.setFont( font )
        self.connect(self.statusLabel, QtCore.SIGNAL("textChanged(QString)"), self.label_chosen )
        self.quitButton = QtGui.QPushButton(self.tr("Quit"))
        self.quitButton.setFont( font )

        self.downloadButton = QtGui.QPushButton(self.tr("Download"))
        self.downloadButton.setDefault(True)
        self.downloadButton.setFont( font )

        self.qualBox = QtGui.QComboBox(self)
        self.qualBox.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.qualBox.setGeometry(QtCore.QRect(65, 16, 65, 20))
        self.qualBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.qualBox.setFont(font)
        QS = 'best notbest audio'
        for S in QS.split(' '):
            self.qualBox.addItem(str(S))
        self.connect(self.qualBox, QtCore.SIGNAL("activated(QString)"), self.qual_chosen )

        self.progressDialog = QtGui.QProgressDialog(self)
    
        self.http = QtNetwork.QHttp(self)
        self.outFile = None
        self.httpGetId = 0
        self.httpRequestAborted = False
    
        self.connect(self.urlLineEdit, QtCore.SIGNAL("textChanged(QString &)"),
                     self.enableDownloadButton)
        self.connect(self.http, QtCore.SIGNAL("requestFinished(int, bool)"),
                     self.httpRequestFinished)
        self.connect(self.http, QtCore.SIGNAL("dataReadProgress(int, int)"),
                     self.updateDataReadProgress)
        self.connect(self.http, QtCore.SIGNAL("responseHeaderReceived(QHttpResponseHeader &)"),
                     self.readResponseHeader)
        self.connect(self.progressDialog, QtCore.SIGNAL("canceled()"),
                     self.cancelDownload)
        self.connect(self.downloadButton, QtCore.SIGNAL("clicked()"),
                     self.downloadFile)

        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"),
                     self, QtCore.SLOT("close()"))
    
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.urlLabel)
        topLayout.addWidget(self.urlLineEdit)
    
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.qualBox)
        buttonLayout.addWidget(self.downloadButton)
        buttonLayout.addWidget(self.quitButton)
    
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
    
        self.setWindowTitle(self.tr("downloader"))
        self.urlLineEdit.setFocus()

    def cancelDownload(self):
        self.statusLabel.setText(self.tr("Download canceled."))
        self.httpRequestAborted = True
        self.http.abort()
        self.downloadButton.setEnabled(True)

    def httpRequestFinished(self, requestId, error):
        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None

            self.progressDialog.hide()
            return

        if requestId != self.httpGetId:
            return
    
        self.progressDialog.hide()
        self.outFile.close()
    
        if error:
            self.outFile.remove()
            QtGui.QMessageBox.information(self, self.tr("downloader"),
                                          self.tr("Download failed: %1.")
                                          .arg(self.http.errorString()))
        else:
            fileName = QtCore.QFileInfo(QtCore.QUrl(self.urlLineEdit.text()).path()).fileName()
            self.statusLabel.setText(self.tr("Downloaded %1 to current directory.").arg(fileName))
        self.downloadButton.setEnabled(True)
        self.outFile = None

    def readResponseHeader(self, responseHeader):
        if responseHeader.statusCode() != 200:
            QtGui.QMessageBox.information(self, self.tr("downloader"),
                                          self.tr("Download failed: %1.")
                                          .arg(responseHeader.reasonPhrase()))
            self.httpRequestAborted = True
            self.progressDialog.hide()
            self.http.abort()
            return

    def label_chosen( self ):
        global l_file
        l_file = self.statusLabel.text()
        return l_file

    def qual_chosen( self, text ):
        global qual
        qual = 'best'
        file = str( self.statusLabel.text() )
        if 'audio' in text:
          l_file = re.sub('.mp4','.m4a',file)
          self.statusLabel.setText( l_file )
          global qual
          qual = str( l_file )
          return qual
        if 'best' in text:
          l_file = re.sub('.m4a','.mp4',file)
          self.statusLabel.setText( l_file )
          global qual
          qual = str( l_file )
          return qual
        if 'notbest' in text:
          l_file = re.sub('.m4a','mp4',file)
          self.statusLabel.setText( l_file )
          global qual
          qual = str( l_file )
          return qual

    def update_url( self ):
        global url
        text = self.urlLineEdit.text()
        return url

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return

        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(bytesRead)

    def enableDownloadButton(self):
        self.downloadButton.setEnabled(not self.urlLineEdit.text().isEmpty())

    def Dload( self, url, dir, l_file ):
        proc = str( Dl +  ' ' + url + ' ' + l_file + ' ' + dir )
        print( 'proc %s' % proc )
        bash( proc )
        sys.exit()    

    def downloadFile(self):
       Home = os.environ['HOME']
       file = str( self.statusLabel.text() )
       Dir = os.path.join( os.path.sep, Home, 'Videos' )
       if os.path.exists( Dir ) == False:
           Dir = Home
       if '.m4a' in file:
         Dir = os.path.join( os.path.sep, Home, 'Videos' )
         if os.path.exists( Dir ) == False:
              Dir = Home
       dir = str( str(Dir) + '/' + str(l_file) )
       pr = str(Tdl + ' ' + str(url) + ' -o ' + str(dir) )
       if qual == 'best':
          proc = str( pr + ' -f bestvideo+bestaudio' )
          bash( proc )
          Exit()
       if qual == 'audio':
          proc = str( pr + ' -x' )
          bash( proc )
          Exit()
       if qual == 'notbest':
          proc = pr
          bash( proc )
          Exit()
       bash( pr )
       Exit()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    httpWin = Downloader()
    httpWin.setStyleSheet( GY )
    httpWin.move(QtGui.QApplication.desktop().screen().rect().center()- httpWin.rect().center())
    sys.exit(httpWin.exec_())
