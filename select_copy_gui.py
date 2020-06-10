import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image
from pytesseract import *
import re
import io
import base64

drawing = False  # True 이면 마우스가 눌린 상태입니다.
mode = True  # True이면 사각형을 그립니다. 'm'을 누르면 곡선으로 변경(토글)됩니다
moving = False
ix, iy = -1, -1
sx, sy = -1, -1
area = [] #[[누른x좌표, 누른y좌표, 땐x좌표, 땐y좌표], ...] 여러 값들
cod_rec = [] #[누른x좌표, 누른y좌표, 땐x좌표, 땐y좌표]
trans_txt = []
tesseract = False



image_base64 = b"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"
# 파비콘 이미지 base64로 사용

# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

def iconFromBase64(base64):
    pixmap = QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QIcon(pixmap)
    return icon

try: #tesseract OCR해주는 프로그램이 없을 경우 혹은 있을 경우의 상태를 만들어서 확인
    f = open("C:/Program Files (x86)/Tesseract-OCR/tesseract.exe")
    f.close()
    pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    pytesseract.image_to_string(toRGB(stringToImage(image_base64)), lang='kor') #korean additional data를 설치했는지 확인
    tesseract = True
except:
    pass


try:
    f = open("C:/Program Files/Tesseract-OCR/tesseract.exe")
    f.close()
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.image_to_string(toRGB(stringToImage(image_base64)), lang='kor') #korean additional data를 설치했는지 확인
    tesseract = True
except:
    pass

    

class error(QWidget): #tesseract가 없을 경우의 ui형태
    def __init__(self):
        super().__init__()
        label1 = QLabel('Tesseract를 설치해주세요!\n사용방법을 참고하시면 됩니다!\n\n[설치후 문제]\n설치시 additional language data에서 korean을 추가하고 설치해주세요!\n자세한 내용은 "사용방법"참조', self)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        
        self.setLayout(layout)

        self.setGeometry(300, 100, 450, 150)# x, y, width, height
        self.setWindowTitle("QWidget")
        self.show()

class MyWidget(QWidget): #tesseract가 있을 경우의 초기 ui 형태
    def __init__(self):
        super().__init__()
        label1 = QLabel('사용방법 : 메뉴를 통해 이미지를 불러오세요! 마우스로 영역을 지정한 후, c를 눌러 텍스트화 하세요\n [키조작]\n ESC : 종료\n c : 이미지 -> 텍스트\n m : 돌아가기 \n d : 창 삭제\n r: 초기화', self)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        
        self.setLayout(layout)

        self.setGeometry(300, 100, 450, 150)# x, y, width, height
        self.setWindowTitle("QWidget")
        self.show()

class MyWidget2(QWidget): #tesseract가 있을 경우, OCR 검출후 숫자만틈의 ui를 만들기 위한 ui
    def __init__(self):
        super().__init__()
        label1 = QLabel('사용방법 : 메뉴를 통해 이미지를 불러오세요! 마우스로 영역을 지정한 후, c를 눌러 텍스트화 하세요\n [키조작]\n ESC : 종료\n c : 이미지 -> 텍스트\n m : 돌아가기 \n d : 창 삭제\n r: 초기화', self)
        
        for i in range(len(area)):
            globals()['qle{}'.format(i)] = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(label1)

        for i in range(len(area)):
            layout.addWidget(globals()['qle{}'.format(i)])

        self.setLayout(layout)

        self.setGeometry(300, 100, 450, 150)# x, y, width, height
        self.setWindowTitle("QWidget")
        self.show()

class MyApp(QMainWindow): #전체적인 틀의 ui
    def __init__(self):
        super().__init__()
        self.initUI()
        self.img = None
        self.simg = None

    def initUI(self):
        if tesseract:
            self.wg = MyWidget()
            openFile = QAction(QIcon('open.png'), 'Open', self)
            openFile.setShortcut('Ctrl+O')
            openFile.setStatusTip('Open New File')
            openFile.triggered.connect(self.showDialog)

            menubar = self.menuBar()
            menubar.setNativeMenuBar(False)
            fileMenu = menubar.addMenu('&이미지불러오기')
            fileMenu.addAction(openFile)
        else:
            self.wg = error()
        
        self.setCentralWidget(self.wg)
        self.statusBar()
        
        self.setWindowTitle('OCR 하기')
        self.setGeometry(300, 300, 450, 200)
        self.show()

    def draw(self ,event, x, y, flags, param):
        global ix, iy, drawing, mode, moving, sx, sy, simg, img, cod_rec, area, bimg, trans_txt

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            moving = False
            bimg = np.array(self.img, copy=True) # 전의 그림 저장 (깊은 복사를 해야된다 하지 않을 경우 계속 바뀐다)
            ix, iy = x, y #처음 클릭한 점 저장

        elif event == cv2.EVENT_MOUSEMOVE:
            sx, sy = x, y #움직여서 전에 있던 움직인 위치를 계속 저장
            can_save = True
            moving = True

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            moving = False
            if abs((sx - ix) * (sy - iy)) > 150: #일정 크기 이상이어야함 (절대값으로 나타냄)
                cod_rec.append(ix) #마우스를 때는 동시에 마우스 부분을 저장하는 코드 (처음 누른 x좌표)
                cod_rec.append(iy) #마우스를 때는 동시에 마우스 부분을 저장하는 코드 (처음 누른 y좌표)
                cod_rec.append(sx) #마우스를 때는 동시에 마우스 부분을 저장하는 코드 (나중 누른 x좌표)
                cod_rec.append(sy) #마우스를 때는 동시에 마우스 부분을 저장하는 코드 (나중 누른 y좌표)
                area.append(cod_rec.copy()) #하나의 리스트로 만듦
                cod_rec.clear()
            #elif 
            #print(area)
            self.img = np.array(self.simg, copy=True) #####마우스를 때면 원래대로 돌아오기 맨처음으로 돌아온다 (초기화)#####
            
            for a in area:
                cv2.rectangle(self.img, (a[0], a[1]), (a[2], a[3]), (0, 255, 0), True, cv2.LINE_4) #초기화 한 후, 리스트 안에 있는 xy좌표를 통해 그림을 그린다
    
    def showDialog(self): #이미지를 선택했을 경우 이미지 창이 나올 경우!
        area.clear()
        trans_txt.clear()
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', './')
            file_name = open(fname[0], 'rb')
            bytes = bytearray(file_name.read()) 
            numpyarray = np.asarray(bytes, dtype=np.uint8) #이거 해서 사진 돌아가는 경우 있음!

            self.img = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
            self.simg  = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)

            cv2.namedWindow('image')
            cv2.setMouseCallback('image', self.draw)

            while (self.img is not None):
                cv2.imshow('image', self.img)
                
                if moving == True and drawing == True: ######드래그해서 형태 보여주기 부분######
                    self.img = np.array(bimg, copy=True) #전의 그림 기준으로 불러온다! (깊은 복사를 해야된다 하지 않을 경우 계속 바뀐다)
                    cv2.rectangle(self.img, (ix, iy), (sx, sy), (0, 255, 0), True, cv2.LINE_4) #이거 하면 이미지 같에 자체적으로 img가 바뀜 / 드래그 할떄 보이기
                
                k = cv2.waitKey(1) & 0xFF
            ####################################################################################
                if k == ord('m'): #####뒤로가기 즉 수정하기#####
                    try:
                        area.pop()
                        trans_txt.pop()
                    except:
                        self.img = np.array(self.simg, copy=True) #맨처음 화면으로 초기화를 한다
                        for a in area:
                            cv2.rectangle(self.img, (a[0], a[1]), (a[2], a[3]), (0, 255, 0), True, cv2.LINE_4) #이미지를 pop해서 해당 영역만 색칠한다
            ####################################################################################
                elif k == ord('c'): #이 부분에 ORC 하는 거 집어 넣기
                    trans_txt.clear()
                    try: #있던 윈도우 없애기 (초기화)
                        page = 0
                        for pages in range(100): #20개의 윈도우까지 다 없애기
                            cv2.destroyWindow("Select_Area"+str(pages))
                    except:
                        pass
                    
                    self.wg2 = MyWidget2() #여러개의 택스트를 생성하기 위해서 적용
                    self.setCentralWidget(self.wg2)

                    for i in area: #영역 밖을 나갈 경우 예외 처리해야함 #[누른x좌표, 누른y좌표, 땐x좌표, 땐y좌표]
                        if self.img.shape[1] < i[2]:
                            i[2] = self.img.shape[1]
                        if 0 > i[2]:
                            i[2] = 0
                        if 0 > i[3]:
                            i[3] = 0
                        if self.img.shape[0] < i[3]:
                            i[3] = self.img.shape[0]
                        
                        if i[2] - i[0] > 0 and i[3] - i[1] > 0: #위 아래 - 왼쪽 오른쪽
                            Select_Area = self.simg[i[1]:i[3], i[0]:i[2]]
                        elif i[0] - i[2] > 0 and i[1] - i[3] > 0: #위 아래 - 오른쪽 왼쪽
                            Select_Area = self.simg[i[3]:i[1], i[2]:i[0]]
                        elif i[2] - i[0] > 0 and i[1] - i[3] > 0: #아래 위 - 왼쪽 오른쪽
                            Select_Area = self.simg[i[3]:i[1], i[0]:i[2]]
                        elif i[0] - i[2] > 0 and i[3] - i[1] > 0: #아래 위 - 오른쪽 왼쪽
                            Select_Area = self.simg[i[1]:i[3], i[2]:i[0]]

                        cv2.imshow("Select_Area"+str(page), Select_Area)

                        text = pytesseract.image_to_string(Select_Area, lang='kor')
                        trans_txt.append(text)
                        
                        page = page + 1

                        
                    for a in range(len(area)):
                        #영역 부분 ocr하기
                        globals()['qle{}'.format(a)].setText(trans_txt[a])
            ####################################################################################
                elif k == ord('d'): #있던 윈도우 없애기 (초기화)
                    try: #있던 윈도우 없애기 (초기화)
                        for pages in range(100): #20개의 윈도우까지 다 없애기
                            cv2.destroyWindow("Select_Area"+str(pages))
                    except:
                        pass
            ####################################################################################
                elif k == ord('r'): #모든 기능 처음으로
                    try: #있던 윈도우 없애기 (초기화)
                        for pages in range(100): #20개의 윈도우까지 다 없애기
                            cv2.destroyWindow("Select_Area"+str(pages))
                    except:
                        pass

                    self.img = np.array(self.simg, copy=True) #맨처음 화면으로 초기화를 한다
                    area.clear()
                    trans_txt.clear()
            ####################################################################################
                elif k == 27:
                    area.clear()
                    trans_txt.clear()
                    cv2.destroyAllWindows()
                    self.img = None
                    self.simg = None
                    break
        except:
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    icon = iconFromBase64(image_base64) # 파비콘 이미지 base64로 사용
    ex.setWindowIcon(icon)
    sys.exit(app.exec_())
    

#사용방법 만들기