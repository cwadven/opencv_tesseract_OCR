<h1 align="center">👁‍🗨 OCR 프로그램</h1>

이미지에 있는 텍스트를 Tesseract-OCR 소프트웨어를 사용하여 OCR 하는 GUI 프로그램

<h3 align="center">프로그램</h3>
<p align="center">
<img alt="ocr" src="https://github.com/cwadven/opencv_tesseract_OCR/blob/master/assets/seq1.PNG"/>
</p>

## 사용 방법

<h3 align="center">이미지 불러오기</h3>
<p align="center">
<img alt="ocr" src="https://github.com/cwadven/opencv_tesseract_OCR/blob/master/assets/seq2.PNG"/>
</p>

~~~
왼쪽 위에 있는 메뉴 탭에서 '이미지불러오기'를 클릭한 후, Open을 이용하여 연다.
~~~

<h3 align="center">불러온 이미지 영역 설정</h3>
<p align="center">
<img alt="ocr" src="https://github.com/cwadven/opencv_tesseract_OCR/blob/master/assets/seq3.PNG"/>
</p>

~~~
마우스 드래그를 하여 영역을 선택한다.
~~~

<h3 align="center">이미지 텍스트화</h3>
<p align="center">
<img alt="ocr" src="https://github.com/cwadven/opencv_tesseract_OCR/blob/master/assets/seq4.PNG"/>
</p>

~~~
키보드 'c'를 눌러 텍스트화 시킨다.
~~~

<h3 align="center">이미지 텍스트화2</h3>
<p align="center">
<img alt="ocr" src="https://github.com/cwadven/opencv_tesseract_OCR/blob/master/assets/seq5.PNG"/>
</p>

~~~
한 영역 뿐만 아니라 여러개의 영역을 설정하여 OCR 할 수 있다!
~~~

## 개발자

**👤 이창우**

- Github : https://github.com/cwadven
- 기술스택 : PyQt5, Tesseract-OCR, Opencv
- 개발기간 : <br>
    - 2020년 6월 1일 ~ 2020년 6월 10일

## 환경 구축

~~~
[필요 소프트웨어 tesseract-ocr 설치]
1. tesseract-ocr 프로그램 다운로드
(windows 용)
https://github.com/UB-Mannheim/tesseract/wiki

32bit : https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0-alpha.20200328.exe

64bit : https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe

(다른 운영체제용)
https://github.com/tesseract-ocr/tesseract/wiki

2. 설치 도중에 Choose Components 선택창에서 Additional language data (download)에서 +를 눌러 Korean을 체크 후 설치


[실행 파일 사용 방법]
1. 다운로드 링크 : 
2. 압축파일 풀기 및 사용방법.txt 참조
3. 위의 '필요 소프트웨어 tesseract-ocr' 다운로드 및 설치


[python 실행 구축 방법]
1. python -m venv myvenv (가상환경 생성)
2. python source myvenv/Script/activates (가상환경 실행)
3. pip install -r requirements.txt (의존성 모듈 설치)
4. python select_copy_gui.py
~~~