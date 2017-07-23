# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import youtube_dl
import pafy
from pydub import AudioSegment
import numpy as np
import cv2
import sys
import os.path
import operator
import datetime
import io

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

try:
    from PyQt4.phonon import Phonon
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "Music Player",
            "Your Qt installation does not have Phonon support.",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
            QtGui.QMessageBox.NoButton)
    sys.exit(1)

#ydl option but deprecated cuz bit lame
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
}
#youtube download folder
ytfolder = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation) + "\\Youtube\\"


class RedirectText(object):
    def __init__(self, cmd):
        self.out = cmd
    def write(self, string):
        self.out.append(string)
    def flush(self):
        pass
    def encoding(self):
        return QtGui.QApplication.UnicodeUTF8

    #def encode(self):
     #   return "utf8"
    #def __getattr__(self, attr):
     #   return getattr(self.stream, attr)


class Ui_MainWindow(object):
    source = None
    player = None
    title = None
    score=None
    level=20
    scoreLine={}
    notes=None
    listindex=0
    frame=None
    vwidth=640
    vheight=480
    totaltime=0
    lrbnd=70
    ubnd=100
    fgbg = cv2.BackgroundSubtractorMOG()
    transition = 'mid'
    ctransition=None
    minsize=10
    font = cv2.FONT_HERSHEY_SIMPLEX
    correct=0

    leftval = 0
    midval = 0
    rightval = 0
    upval = 0

    lenl = vheight * lrbnd
    lenm = (vheight - ubnd) * (vwidth - (2 * lrbnd))
    lenr = vheight * lrbnd
    lenu = (vwidth - (2 * lrbnd)) * ubnd

    t_minus = cv2.cvtColor(np.zeros((vheight, vwidth, 3), np.uint8), cv2.COLOR_RGB2GRAY)
    t =cv2.cvtColor(np.zeros((vheight, vwidth, 3), np.uint8), cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(np.zeros((vheight, vwidth, 3), np.uint8), cv2.COLOR_RGB2GRAY)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(820, 635)
        MainWindow.setMinimumSize(820, 635)
        MainWindow.setMaximumSize(820, 635)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.lineEdit = QtGui.QTextEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 475, 800, 105))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit.setReadOnly(True)

        redir = RedirectText(self.lineEdit)
        sys.stdout = redir

        self.lineEdit.append(u'Microsoft Imagine Cup 2017 - ARshaker에 오신 것을 환영합니다.')
        self.lineEdit.append(u'음악 파일이나 기 생성된 악보 파일(*.jhw)을 열어주세요!')
        self.lineEdit.append(u'JHW=김주현(JH)+황혜원(HW) 제작')

        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(650, 5, 160, 465))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))

        self.seekSlider = Phonon.SeekSlider(self.centralwidget)
        self.seekSlider.setGeometry(QtCore.QRect(220, 6, 241, 22))
        self.seekSlider.setObjectName(_fromUtf8("seekSlider"))

        paletteb = QtGui.QPalette()
        paletteb.setBrush(QtGui.QPalette.Light, QtCore.Qt.black)

        paletteg = QtGui.QPalette()
        paletteg.setBrush(QtGui.QPalette.Light, QtCore.Qt.green)

        palettegl = QtGui.QPalette()
        palettegl.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkYellow)

        paletter = QtGui.QPalette()
        paletter.setBrush(QtGui.QPalette.Light, QtCore.Qt.red)

        palettem = QtGui.QPalette()
        palettem.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkMagenta)

        palettebl = QtGui.QPalette()
        palettebl.setBrush(QtGui.QPalette.Light, QtCore.Qt.darkBlue)

        palettebb = QtGui.QPalette()
        palettebb.setBrush(QtGui.QPalette.Light, QtCore.Qt.blue)

        palettebc = QtGui.QPalette()
        palettebc.setBrush(QtGui.QPalette.Light, QtCore.Qt.cyan)

        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setPalette(paletteb)
        self.lcdNumber.setGeometry(QtCore.QRect(580, 5, 64, 23))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.lcdNumber.display("00:00")

        self.lcdr = QtGui.QLCDNumber(self.centralwidget)
        self.lcdr.setPalette(palettegl)
        self.lcdr.setGeometry(QtCore.QRect(15, 420, 80, 23))
        self.lcdr.setObjectName(_fromUtf8("lcdr"))
        self.lcdr.display("00:00")
        self.rlab=QtGui.QLabel(self.centralwidget)
        self.rlab.setText(u'남은 시간')
        self.rlab.setGeometry(QtCore.QRect(23, 445, 100, 22))

        self.lcda = QtGui.QLCDNumber(self.centralwidget)
        self.lcda.setPalette(paletteb)
        self.lcda.setGeometry(QtCore.QRect(110, 420, 80, 23))
        self.lcda.setObjectName(_fromUtf8("lcdAccu"))
        self.lcda.display("00000")
        self.alab = QtGui.QLabel(self.centralwidget)
        self.alab.setText(u'현재 비트')
        self.alab.setGeometry(QtCore.QRect(118, 445, 100, 22))

        self.lcdo = QtGui.QLCDNumber(self.centralwidget)
        self.lcdo.setPalette(palettebb)
        self.lcdo.setGeometry(QtCore.QRect(205, 420, 80, 23))
        self.lcdo.setObjectName(_fromUtf8("lcdCorrect"))
        self.lcdo.display("00000")
        self.olab = QtGui.QLabel(self.centralwidget)
        self.olab.setText(u'맞은 비트')
        self.olab.setGeometry(QtCore.QRect(213, 445, 100, 22))

        self.lcdx = QtGui.QLCDNumber(self.centralwidget)
        self.lcdx.setPalette(palettem)
        self.lcdx.setGeometry(QtCore.QRect(300, 420, 80, 23))
        self.lcdx.setObjectName(_fromUtf8("lcdWrong"))
        self.lcdx.display("00000")
        self.xlab = QtGui.QLabel(self.centralwidget)
        self.xlab.setText(u'틀린 비트')
        self.xlab.setGeometry(QtCore.QRect(308, 445, 100, 22))

        self.lcdl = QtGui.QLCDNumber(self.centralwidget)
        self.lcdl.setPalette(paletteg)
        self.lcdl.setGeometry(QtCore.QRect(395, 420, 80, 23))
        self.lcdl.setObjectName(_fromUtf8("lcdLeft"))
        self.lcdl.display("00000")
        self.llab = QtGui.QLabel(self.centralwidget)
        self.llab.setText(u'남은 비트')
        self.llab.setGeometry(QtCore.QRect(403, 445, 100, 22))

        self.lcdpg = QtGui.QLCDNumber(self.centralwidget)
        self.lcdpg.setPalette(palettebc)
        self.lcdpg.setGeometry(QtCore.QRect(490, 420, 70, 23))
        self.lcdpg.setObjectName(_fromUtf8("lcdProgress"))
        self.lcdpg.display("00000")
        self.pglab = QtGui.QLabel(self.centralwidget)
        self.pglab.setText(u'진행률(%)')
        self.pglab.setGeometry(QtCore.QRect(491, 445, 100, 22))

        self.lcdg = QtGui.QLCDNumber(self.centralwidget)
        self.lcdg.setPalette(paletter)
        self.lcdg.setGeometry(QtCore.QRect(572, 420, 70, 23))
        self.lcdg.setObjectName(_fromUtf8("lcdPercent"))
        self.lcdg.display("00000")
        self.glab = QtGui.QLabel(self.centralwidget)
        self.glab.setText(u'정확도(%)')
        self.glab.setGeometry(QtCore.QRect(573, 445, 100, 22))

        self.lrlab=QtGui.QLabel(self.centralwidget)
        self.lrlab.setText(u'좌,우(L,R)크기')
        self.lrlab.setGeometry(QtCore.QRect(13, 380, 100, 22))
        self.lrsl = QtGui.QSlider(QtCore.Qt.Horizontal,self.centralwidget)
        self.lrsl.setGeometry(QtCore.QRect(117, 380, 120, 22))
        self.lrsl.setMinimum(30)
        self.lrsl.setMaximum(200)
        self.lrsl.setValue(30)
        self.lrsl.setObjectName(_fromUtf8("lrsl"))
        self.lrsl.valueChanged.connect(self.lrslchange)


        self.ulab = QtGui.QLabel(self.centralwidget)
        self.ulab.setText(u'위(U) 경계')
        self.ulab.setGeometry(QtCore.QRect(244, 380, 100, 22))
        self.usl = QtGui.QSlider(QtCore.Qt.Horizontal,self.centralwidget)
        self.usl.setGeometry(QtCore.QRect(317, 380, 120, 22))
        self.usl.setMinimum(100)
        self.usl.setMaximum(400)
        self.usl.setValue(100)
        self.usl.setObjectName(_fromUtf8("usl"))
        self.usl.valueChanged.connect(self.uslchange)

        self.dlab = QtGui.QLabel(self.centralwidget)
        self.dlab.setText(u'색상 경계값')
        self.dlab.setGeometry(QtCore.QRect(441, 380, 100, 22))
        self.dsl = QtGui.QSlider(QtCore.Qt.Horizontal,self.centralwidget)
        self.dsl.setGeometry(QtCore.QRect(524, 380, 120, 22))
        self.dsl.setMinimum(1)
        self.dsl.setMaximum(255)
        self.dsl.setValue(10)
        self.dsl.setObjectName(_fromUtf8("dsl"))
        self.dsl.valueChanged.connect(self.dslchange)

        #음악 재생 부분
        self.volumeSlider =Phonon.VolumeSlider(self.centralwidget)
        #self.volumeSlider.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.volumeSlider.setGeometry(QtCore.QRect(460, 3, 113, 26))
        self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        self.menu_4 = QtGui.QMenu(self.menubar)
        self.menu_4.setObjectName(_fromUtf8("menu_4"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.action.setShortcut("Ctrl+O")
        self.action.setStatusTip(u'음악 파일을 엽니다. 악보가 이전에 생성되지 않은 음악일 경우, 악보 생성에 시간이 소요됩니다.')
        self.action.triggered.connect(lambda :self.openMusic(True))

        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.action_2.setShortcut("Ctrl+S")
        self.action_2.setStatusTip(u'악보 파일을 엽니다. 파일 확장자가 *.jhw로 끝나며 .jhw 앞에 붙은 숫자가 클 수록 난이도가 쉽습니다.')
        self.action_2.triggered.connect(self.openScore)

        self.action_y = QtGui.QAction(MainWindow)
        self.action_y.setObjectName(_fromUtf8("action_y"))
        self.action_y.setShortcut("Ctrl+Y")
        self.action_y.setStatusTip(u'YouTube 주소를 입력합니다. YouTube에서 음악을 받아 악보파일을 자동으로 생성합니다.')
        self.action_y.triggered.connect(lambda :self.openMusic(False))

        self.action_3 = QtGui.QAction(MainWindow,checkable=True)
        self.action_3.setObjectName(_fromUtf8("action_3"))

        self.action_4 = QtGui.QAction(MainWindow,checkable=True)
        self.action_4.setObjectName(_fromUtf8("action_4"))
        self.action_4.setChecked(True)

        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName(_fromUtf8("action_5"))


        self.action_6 = QtGui.QAction(MainWindow)
        self.action_6.setObjectName(_fromUtf8("action_6"))
        self.action_6.setShortcut("Ctrl+H")
        self.action_6.setStatusTip(u'간략한 정보와 사용방법을 수록 하고 있습니다.')
        self.action_6.triggered.connect(self.help)

        ag = QtGui.QActionGroup(MainWindow, exclusive=True)
        self.action_7 = ag.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action_7.setChecked(True)
        self.action_8 = ag.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action_9 = ag.addAction(QtGui.QAction(MainWindow, checkable=True))

        #self.action_7 = QtGui.QAction(MainWindow)
        self.action_7.setObjectName(_fromUtf8("action_7"))
        self.action_7.setStatusTip('Easy: *.20.jhw')
        self.action_7.triggered.connect(self.easy)

        #self.action_8 = QtGui.QAction(MainWindow)
        self.action_8.setObjectName(_fromUtf8("action_8"))
        self.action_8.setStatusTip('Medium: *.15.jhw')
        self.action_8.triggered.connect(self.medi)

        #self.action_9 = QtGui.QAction(MainWindow)
        self.action_9.setObjectName(_fromUtf8("action_9"))
        self.action_9.setStatusTip('Hard: *.10.jhw')
        self.action_9.triggered.connect(self.hard)

        ag2 = QtGui.QActionGroup(MainWindow, exclusive=True)
        self.action_10 = ag2.addAction(QtGui.QAction(MainWindow, checkable=True))
        self.action_10.setChecked(True)
        self.action_11 = ag2.addAction(QtGui.QAction(MainWindow, checkable=True))

        self.action_10.setObjectName(_fromUtf8("action_10"))
        self.action_10.setStatusTip(u'인식 방법을 잔상 인식 모드로 설정합니다.')
        self.action_10.triggered.connect(self.shadow)

        self.action_11.setObjectName(_fromUtf8("action_11"))
        self.action_11.setStatusTip(u'인식 방법을 배경 제거 인식 모드로 설정합니다.')
        self.action_11.triggered.connect(self.bgrm)


        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_y)
        self.menu.addAction(self.action_6)
        self.menu_2.addAction(self.action_3)
        self.menu_2.addAction(self.action_4)


        self.menu_3.addAction(self.action_7)
        self.menu_3.addAction(self.action_8)
        self.menu_3.addAction(self.action_9)
        self.menu_4.addAction(self.action_10)
        self.menu_4.addAction(self.action_11)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.camera = QtGui.QWidget(self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(0, 20, 655, 365))
        self.camera.setMinimumSize(QtCore.QSize(655, 365))
        self.camera.setMaximumSize(QtCore.QSize(655, 365))
        self.camera.setObjectName(_fromUtf8("camera"))

        self.startButton = QtGui.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(10, 5, 91, 23))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.pauseButton = QtGui.QPushButton(self.centralwidget)
        self.pauseButton.setGeometry(QtCore.QRect(101,5, 111, 23))
        self.pauseButton.setObjectName(_fromUtf8("pauseButton"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #UI 부분 완성 이제 영상 부분

        self.capture = None
        self.fps = 29.97
        self.timer=None
        self.startButton.clicked.connect(self.start)
        self.startButton.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1), self.centralwidget), QtCore.SIGNAL('activated()'),self.start)
        self.monitor = QtGui.QVBoxLayout(self.camera)
        self.startCapture()

        # QProcess object for external app
        self.process = QtCore.QProcess()
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyRead.connect(self.dataReady)
        # Just to prevent accidentally running multiple times
        # Disable the button when process starts, and enable it when it finishes
        self.process.started.connect(lambda: self.menu.setEnabled(False))
        self.process.started.connect(lambda: self.startButton.setEnabled(False))
        self.process.finished.connect(lambda: self.menu.setEnabled(True))
        self.process.finished.connect(lambda: self.startButton.setEnabled(True))
        self.process.finished.connect(self.scoremade)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ARshaker", None))
        self.menu.setTitle(_translate("MainWindow", "&파일", None))
        self.menu_2.setTitle(_translate("MainWindow", "&화면 반전", None))
        self.menu_3.setTitle(_translate("MainWindow", "&난이도", None))
        self.menu_4.setTitle(_translate("MainWindow", "&인식 모드", None))
        self.action.setText(_translate("MainWindow", "&음악 열기", None))
        self.action_2.setText(_translate("MainWindow", "&악보 열기", None))
        self.action_y.setText(_translate("MainWindow", "&Youtube에서 열기", None))
        self.action_3.setText(_translate("MainWindow", "&상하 반전", None))
        self.action_4.setText(_translate("MainWindow", "&좌우 반전", None))
        self.action_5.setText(_translate("MainWindow", "&배경삭제", None))
        self.action_6.setText(_translate("MainWindow", "&도움말", None))
        self.action_7.setText(_translate("MainWindow", "&쉬움", None))
        self.action_8.setText(_translate("MainWindow", "&보통", None))
        self.action_9.setText(_translate("MainWindow", "&어려움", None))
        self.action_10.setText(_translate("MainWindow", "&잔상 인식", None))
        self.action_11.setText(_translate("MainWindow", "&배경 제거", None))
        self.startButton.setText(_translate("MainWindow", "시작(F1)", None))
        self.pauseButton.setText(_translate("MainWindow", "일시정지(F2)", None))

    #위 경계값 가져오기
    def uslchange(self):
        self.ubnd = self.usl.value()
        self.lenl = self.vheight * self.lrbnd
        self.lenm = (self.vheight - self.ubnd) * (self.vwidth - (2 * self.lrbnd))
        self.lenr = self.vheight * self.lrbnd
        self.lenu = (self.vwidth - (2 * self.lrbnd)) * self.ubnd

    #좌,우 경계값 가져오기
    def lrslchange(self):
        self.lrbnd = self.lrsl.value()
        self.lenl = self.vheight * self.lrbnd
        self.lenm = (self.vheight - self.ubnd) * (self.vwidth - (2 * self.lrbnd))
        self.lenr = self.vheight * self.lrbnd
        self.lenu = (self.vwidth - (2 * self.lrbnd)) * self.ubnd


    #인식 크기 경계값 가져오기
    def dslchange(self):
        self.minsize = self.dsl.value()

    # 악보생성용 서브 프로세스 호출 및 결과 기입
    def dataReady(self):
        cursor = self.lineEdit.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str(self.process.readAll()))
        self.lineEdit.ensureCursorVisible()

    # 악보를 처음 생성했을때
    def scoremade(self):
        self.lineEdit.clear()
        self.lineEdit.append(self.score)
        if self.level is 20:
            self.lineEdit.append(u'난이도: 쉬움')
        elif self.level is 15:
            self.lineEdit.append(u'난이도: 보통')
        elif self.level is 10:
            self.lineEdit.append(u'난이도: 어려움')
        self.sequencer()
        self.lineEdit.append(u'위의 악보가 생성되었습니다. 시작(F1)을 눌러 리듬게임을 시작하세요!')
        self.stop()

    #사용자 조정 인식 값 라벨 변경 및 인지
    def bgrm(self):
        self.dlab.setText(u'인식 최소값')
        self.lineEdit.append(u'인식 방법이 배경 제거 인식 모드로 설정 되었습니다.')
        self.dsl.setMinimum(1)
        self.dsl.setMaximum(1000)
        self.dsl.setValue(1)
        self.minsize=1


    def shadow(self):
        self.dlab.setText(u'색상 경계값')
        self.lineEdit.append(u'인식 방법이 잔상 인식 모드로 설정 되었습니다.')
        self.dsl.setMinimum(1)
        self.dsl.setMaximum(255)
        self.dsl.setValue(10)
        self.minsize = 10


    #난이도 3개
    def easy(self):
        self.level=20
        self.lineEdit.append(u'난이도가 쉬움으로 변경되었습니다.')

    def medi(self):
        self.level = 15
        self.lineEdit.append(u'난이도가 보통으로 변경되었습니다.')

    def hard(self):
        self.level = 10
        self.lineEdit.append(u'난이도가 어려움으로 변경되었습니다.')

    #음악 여는 함수
    def openMusic(self,type):
        name = None
        if type:
            name = QtGui.QFileDialog.getOpenFileNames(None, u'음악 선택 - mp3, wav, wma 확장자를 가진 파일 하나를 열어주세요',  QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation),"Music (*.mp3 *.wav *.wma)")
        else:
            url, ok = QtGui.QInputDialog.getText(None, u'음악 선택 - YouTube 주소를 입력하세요', u'예시:https://www.youtube.com/watch?v=DVuRGCuFoa0')
            if not str(url).startswith('https://www.youtube.com/watch?v=') or not ok:
                self.lineEdit.append(u'올바르지 않은 YouTube 주소 입니다. 다시 시도하세요.')
                return
            else:
                self.lineEdit.append(u'음원 추출 중입니다. 조금만 기다려주세요.')
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                   ydl.download([str(url)])

                video = pafy.new(url)
                for a in reversed(video.audiostreams):
                    if not str(a.extension).__contains__("webm"):
                        songtitle = a.title+ "." + a.extension
                        self.lineEdit.append(songtitle)
                        self.lineEdit.append(u'음원 추출 중입니다. 조금만 기다려주세요.')
                        if not os.path.isfile(songtitle):
                            downloader=QtCore.QThread()
                            #변환 subprocess 미완
                            #sys.stdout = open(os.devnull, "w")
                            #a.download(quiet=True)
                            #sys.stdout= saved_stdout

                        #name=ytfolder+a.title+ ".mp3"


        if not name:
            return
        else:
            print (name)
            self.source=name[0]
            self.lineEdit.clear()
            self.lineEdit.append(self.source)
            self.lineEdit.append(u'음악 파일이 성공적으로 열렸습니다. 악보를 생성합니다. 완료될 때 까지 기다려 주세요.')
            self.lineEdit.append(" ")
            #self.player = Phonon.createPlayer(Phonon.MusicCategory,Phonon.MediaSource(self.source))
            self.player=Phonon.MediaObject()
            self.player.setCurrentSource(Phonon.MediaSource(self.source))
            self.player.setTickInterval(100)
            self.player.tick.connect(self.tick)
            self.seekSlider.setMediaObject(self.player)
            self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
            Phonon.createPath(self.player, self.audioOutput)
            self.volumeSlider.setAudioOutput(self.audioOutput)
            self.title=self.source.split('\\')[self.source.count('\\')]
            self.score=self.source + "." + str(self.level)+ ".jhw"
            cmd='mnb '+str(self.level)+' "'+self.source+'" "'+self.score+'"'
            if os.path.exists(self.score):
               self.sequencer()
               self.lineEdit.append(u'이미 생성된 악보가 있습니다. 시작(F1)을 눌러 리듬게임을 시작하세요!')
               self.stop()
            else:
                self.process.start(cmd)

    #시퀀서
    def sequencer(self):
        self.correct=0
        f = open(self.score, 'r')
        while True:
            line = f.readline()
            if not line: break
            self.scoreLine[(int)(line.split(" ")[0])] = line.split(" ")[1].split("\n")[0]
        f.close()
        self.notes = sorted(self.scoreLine.items(), key=operator.itemgetter(0))
        self.lineEdit.append(u'비트 개수: '+str(len(self.notes))+u'개' )
        self.listWidget.clear()
        self.listindex=0
        for note in self.notes:
            bits=str(datetime.timedelta(milliseconds=note[0])).split(":")
            if bits[2].endswith("000"):
                bits[2]=bits[2].rstrip("000")
            if len(bits[2])<6:
                i=len(bits[2])
                while i <6:
                    bits[2]=bits[2]+'0'
                    i+=1
            self.listWidget.addItem(str(bits[1])+":"+str(bits[2]).replace(".",":")+" - "+note[1])
            if self.notes.index(note)==len(self.notes)-1:
                self.totaltime=note[0]
                self.lineEdit.append(u'예상 운동 시간: ' + str(bits[1])+u'분 '+str(bits[2]).replace(".",u'초 '))


    #악보 여는 함수
    def openScore(self):
        name = QtGui.QFileDialog.getOpenFileNames(None, u'악보 선택 - .jhw 앞에 붙은 숫자가 클 수록 난이도가 쉽습니다. (20:쉬움 15:보통 10:어려움)', QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.MusicLocation), "Score (*.jhw)");
        if not name:
            return
        else:
            self.score = name[0]
            if ".mp3" in self.score:
                self.source=self.score.split('.mp3')[0]+'.mp3'
            elif ".wma" in self.score:
                self.source=self.score.split('.wma')[0]+'.wma'
            elif ".wav" in self.score:
                self.source = self.score.split('.wav')[0] + '.wav'
            self.title=self.source.split('\\')[self.source.count('\\')]
            self.lineEdit.clear()
            self.lineEdit.append(self.score)
            self.lineEdit.append(u'악보 파일이 성공적으로 열렸습니다. 해당 악보에 맞는 음악을 로딩합니다.')
            if os.path.exists(self.source):
                self.player = Phonon.MediaObject()
                self.player.setCurrentSource(Phonon.MediaSource(self.source))
                self.player.setTickInterval(100)
                self.player.tick.connect(self.tick)
                self.seekSlider.setMediaObject(self.player)
                self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
                Phonon.createPath(self.player, self.audioOutput)
                self.volumeSlider.setAudioOutput(self.audioOutput)
                self.sequencer()
                self.stop()
                self.lineEdit.append(u'음악파일이 성공적으로 로드되었습니다. 시작(F1)을 눌러 리듬게임을 시작하세요!')
            else:
                self.lineEdit.append(u'악보 파일에 해당하는 음악파일이 없습니다. 음악파일을 먼저 열어주세요')

    #도움말 함수
    def help(self):
        QtGui.QMessageBox.information(None, u'팀 JHW -ARSHAKER',
                                      u'제10회 공개 SW 개발자대회 응용SW 부문 출품작\n\n제작자: 김주현 , 황혜원\n\n원만한 사용을 위해 게임 시작 전 좌,우,위 위치 슬라이더를 조절하여 초기에 초록색┌┐이 화면에 나오도록 해주시고,\n\n가급적 카메라가 있는 방향으로 몸을 뻗으세요.\n\n초록색┌┐상태로 전환이 잘 안되는 경우 인식 모드를 번갈아 바꾸어 보세요.',
                                      u'ARSHAKER 화이팅')
    #타이머 함수
    def tick(self, time):
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.lcdNumber.display(displayTime.toString('mm:ss'))
        timediff=self.totaltime-time
        if timediff<0:
            timediff=0
        displayTime2 = QtCore.QTime(0, (timediff / 60000) % 60, (timediff / 1000) % 60)
        self.lcdr.display(displayTime2.toString('mm:ss'))
        for note in self.notes:
          if note[0]<=self.player.currentTime() and note[0]>self.listindex:
              self.listindex=note[0]
              self.listWidget.setCurrentRow(self.notes.index(note))
              self.lcda.display(self.notes.index(note)+1)
              self.lcdl.display(len(self.notes)-self.notes.index(note)-1)
              self.lcdo.display(self.correct)
              self.lcdx.display(self.notes.index(note) + 1 - self.correct)
              percent=round((float(self.notes.index(note)) / float(len(self.notes))*100))
              perfect = round((float(self.correct) / float(self.notes.index(note)+1) * 100))
              self.lcdg.display(int(perfect))
              self.lcdpg.display(int(percent))
              #self.listWidget.setCurrentIndex(self.listWidget.model().index(self.notes.index(note)))
              if timediff>0:
                self.ctransition=note[1]
              else:
                self.ctransition = None
              if self.notes.index(note)+19<len(self.notes):
                self.listWidget.scrollTo(self.listWidget.model().index(self.notes.index(note)+19))

    #영상 관련 함수
    def diffImg(self,t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        return cv2.bitwise_and(d1, d2)

    def nextFrameSlot(self):
        ret, frame = self.cap.read()

        #상하, 좌우 반전; 기본 좌우 반전 선택
        if self.action_3.isChecked():
            frame=cv2.flip(frame,0)
        if self.action_4.isChecked():
            frame = cv2.flip(frame, 1)

        #배경 지우기 모드
        if self.action_11.isChecked():
            fgmask = self.fgbg.apply(frame)
            #fgmask = cv2.equalizeHist(fgmask)
            thrs1 = 2000
            thrs2 = 4000
            fgmask = cv2.Canny(fgmask, thrs1, thrs2, apertureSize=5)
            left = fgmask[0:self.vheight, 0:self.lrbnd]
            mid = fgmask[self.ubnd:self.vheight, self.lrbnd:self.vwidth - self.lrbnd]
            right = fgmask[0:self.vheight, self.vwidth - self.lrbnd:self.vwidth]
            up = fgmask[0:self.ubnd, self.lrbnd:self.vwidth - self.lrbnd]

        #잔상 인식 모드
        else:
            self.t_minus = self.t
            self.t = self.t_plus
            self.t_plus = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            blur = self.diffImg(self.t_minus, self.t, self.t_plus)
            masks = cv2.GaussianBlur(blur, (5, 5), 0)
            ret, mask = cv2.threshold(masks,self.minsize, 255, cv2.THRESH_TOZERO)

            left = mask[0:self.vheight, 0:self.lrbnd]
            mid = mask[self.ubnd:self.vheight, self.lrbnd:self.vwidth - self.lrbnd]
            right = mask[0:self.vheight, self.vwidth - self.lrbnd:self.vwidth]
            up = mask[0:self.ubnd, self.lrbnd:self.vwidth - self.lrbnd]


        leftval = cv2.countNonZero(left)
        midval = cv2.countNonZero(mid)
        rightval = cv2.countNonZero(right)
        upval = cv2.countNonZero(up)

        if (leftval is 0 and rightval is 0 and upval is 0) or (
                    leftval < self.minsize and rightval < self.minsize and upval < self.minsize):
            # if (leftval is 0 and rightval is 0 and upval is 0):
            # if (leftval is 0 and rightval is 0 and upval is 0):
            cv2.rectangle(frame, (self.lrbnd, self.ubnd), (self.vwidth - self.lrbnd, self.vheight), (0, 255, 0), 10)
            self.transition = 'mid'
        elif leftval is 0 and rightval is 0 and upval > 0 or (leftval < upval and rightval < upval):
            cv2.rectangle(frame, (self.lrbnd, 0), (self.vwidth - self.lrbnd, self.ubnd), (255, 255, 255), 10)
            if self.transition is not 'U':
                self.transition = 'U'
        elif leftval > 0 and rightval is 0 and upval is 0 or (leftval > upval and leftval > rightval):
            cv2.rectangle(frame, (0, 0), (self.lrbnd, self.vheight), (255, 0, 0), 10)
            if self.transition is not 'L':
                self.transition = 'L'
        elif rightval > 0 and leftval is 0 and upval is 0 or (rightval > upval and rightval > leftval):
            cv2.rectangle(frame, (self.vwidth - self.lrbnd, 0), (self.vwidth, self.vheight), (0, 0, 255), 10)
            if self.transition is not 'R':
                self.transition = 'R'

        cv2.putText(frame, str(leftval) + "/" + str(self.lenl), (3, 180), self.font, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, str(midval) + "/" + str(self.lenm), (270, 400), self.font, 0.5,
                    (0, 255, 0), 2)
        cv2.putText(frame, str(rightval) + "/" + str(self.lenr), (565, 180),
                    self.font, 0.5,
                    (0, 255, 0), 2)
        cv2.putText(frame, str(upval) + "/" + str(self.lenu), (280, 90), self.font, 0.5,
                    (0, 255, 0), 2)

        if self.ctransition==self.transition:
            self.ctransition=None
            self.correct+=1
        if self.ctransition is not None:
            if self.ctransition == 'L':
                cv2.putText(frame, self.ctransition, (250, 360), self.font, 7, (255, 0, 0), 7)
            elif self.ctransition == 'R':
                cv2.putText(frame, self.ctransition, (250, 360), self.font, 7, (0, 0, 255), 7)
            elif self.ctransition == 'U':
                cv2.putText(frame, self.ctransition, (250, 360), self.font, 7, (255, 255, 255), 7)

        #self.keyFix()
        if ret:
            # My webcam yields frames in BGR format
            self.frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)
        else:
            self.frame = np.zeros((480, 640, 3), np.uint8)
            cv2.putText(self.frame, "Please Rerun Program After Connecting Camera", (5, 240), self.font, 0.8, (0, 255, 0), 2)
            self.lineEdit.setText(u'컴퓨터에 카메라가 설치되지 않았습니다. 카메라를 연결 후 프로그램을 재 실행 시켜주세요')

        img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def startCapture(self):
        if not self.capture:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.vwidth)
            self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.vheight)
            self.video_frame = QtGui.QLabel()
            self.pauseButton.clicked.connect(self.stop)
            self.pauseButton.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F2), self.centralwidget),
                                     QtCore.SIGNAL('activated()'), self.stop)
            # self.capture.setFPS(1)
            # self.setParent(self)
            # self.setWindowFlags(QtCore.Qt.Tool)
            self.monitor.addWidget(self.video_frame)
            self.start()

    '''def endCapture(self):
        self.capture.deleteLater()
        self.capture = None'''

    def setFPS(self, fps):
        self.fps = fps

    def start(self):
        if self.timer is None:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.nextFrameSlot)
            self.timer.start(1000. / self.fps)
            if self.player is not None and self.player.state() != Phonon.PlayingState:
                self.player.play()

    def stop(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
            if self.player is not None and self.player.state() == Phonon.PlayingState:
                self.player.pause()

    def deleteLater(self):
        self.cap.release()
        super(QtGui.QWidget, self).deleteLater()

        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

