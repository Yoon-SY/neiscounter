# Copyright 2022 Yoon Sung-Yong
# NIHONGOKA SAIKOU!

import sys
import time
import string
from PyQt5 import uic
from PyQt5.QtWidgets import *

form_class = uic.loadUiType('panel.ui')[0]

def fileanalyze(f):
    ret = ''
    while True:
        s = f.readline()
        if s == '':
            return ret
        ret += s

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Buttons
        self.copybtn.clicked.connect(self.clipcopy)
        self.delbtn.clicked.connect(self.cleantext)
        self.pastebtn.clicked.connect(self.pastetext)
        self.undobtn.clicked.connect(self.undo)
        self.redobtn.clicked.connect(self.redo)
        self.loadbtn.clicked.connect(self.load)
        self.savebtn.clicked.connect(self.save)

        # Input
        self.inputtext.textChanged.connect(self.calc)
    
    # Copies text into clipboard. Identical to Ctrl+A,C
    def clipcopy(self):
        self.inputtext.selectAll()
        self.inputtext.copy()
    
    # Deletes input text & history
    def cleantext(self):
        self.inputtext.clear()
    
    # Pastes text into clipboard. Identical to Ctrl+V
    def pastetext(self):
        self.inputtext.paste()
    
    # Undoes action. Identical to Ctrl+Z
    def undo(self):
        self.inputtext.undo()
    
    # Redoes action. Identical to Ctrl+Y or Ctrl+Shift+Z
    def redo(self):
        self.inputtext.redo()
    
    # Loads .txt files into the input area
    def load(self):
        try:
            fname = QFileDialog.getOpenFileName(self, "파일 선택", "", "텍스트 파일(*.txt)", "")
            if fname[0]:
                self.inputtext.clear()
                self.inputtext.insertPlainText(fileanalyze(open(fname[0], encoding='utf-8')))
                self.statmsg.setText("파일을 불러왔습니다.")
            else:
                self.statmsg.setText("파일이 선택되지 않았습니다.")
                raise FileNotFoundError
        except FileNotFoundError:
            pass
        except Exception as e:
            self.statmsg.setText("알 수 없는 오류. 콘솔창을 확인해주세요.")
            print(e)
    
    # Saves the input text into a *.txt file
    def save(self):
        try:
            len_bytes = int(self.v3.text()[:-4])
            fname = "바이트계산기 %s (%d 바이트).txt" % (time.strftime("%m-%d %H%M%S"), len_bytes)
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(self.inputtext.toPlainText())
            self.statmsg.setText("정상적으로 저장되었습니다.")
            print("현재 내용이 %s 파일로 저장되었습니다." % fname)
        except Exception as e:
            self.statmsg.setText("알 수 없는 오류. 콘솔창을 확인해주세요.")
            print(e)
    
    # Length & utf-8 byte calculation
    def calc(self):
        contents = self.inputtext.toPlainText()
        whitespace = 0
        for ws in string.whitespace:
            whitespace += contents.count(ws)
        self.v1.setText("%d자" % (len(contents)))
        self.v2.setText("%d자" % (len(contents)-whitespace))
        self.v3.setText("%d 바이트" % (len(bytearray(contents,encoding='utf-8'))))
        if self.statmsg.text() != "정상":
            self.statmsg.setText("정상")

if __name__ == '__main__':
    print("프로그램 준비 중...")
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    print("프로그램 준비 완료")
    app.exec_()
