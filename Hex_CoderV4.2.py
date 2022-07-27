from PIL import Image
import colorama
import numpy as np
import random
import os.path
from math import ceil
##===========================================================================
'''def libary pixl'''
##===========================================================================
def sizeinfo(AllData): #определение размерности картинки
    sizedata = len(AllData)
    y = ceil((3*sizedata)**0.5 / 4) 
    x = ceil((16/9)*y) 
    return x, y

def truelenginfo(lenginfo): #преобразование длины исходных данных в набор пиксельных данных формата RGB
    lengslayer = []
    while lenginfo > 0:
        lengslayer.append(lenginfo % 256)
        lenginfo = lenginfo // 256
    for i in range(12 - len(lengslayer)):
        lengslayer.append(0)
    return lengslayer

def typefileinfo(file_name): #определение и сохранение в байтах расширения исходных данных
    resulttype, typ = [], []
    f = file_name.split('.')
    typename = bytearray(f[-1], 'utf-8')
    for i in range(len(typename)):
        resulttype.append(typename[i])
    typ = resulttype
    for i in range(len(resulttype)%3):
        resulttype.append(0)
    return resulttype, typ

def lengofTFI(file_name): #преобразование длины расширения в набор пиксельных данных формата RGB
    typ, slayOftyp = typefileinfo(file_name)[1], []
    lengtyp = len(typ)
    while lengtyp > 0:
        slayOftyp.append(lengtyp % 256)
        lengtyp = lengtyp // 256
    for i in range(6 - len(slayOftyp)):
        slayOftyp.append(0)    
    return slayOftyp    

def info_file(file_name, lenginfo): #создания линии данных на основе вышенайденного
    info_lengdata, info_typefile, info_lengtypedata = truelenginfo(lenginfo), typefileinfo(file_name)[0], lengofTFI(file_name)
    resultinfo = info_lengdata + info_lengtypedata + info_typefile
    resultinfo.append(0)
    for i in range(3-len(resultinfo)%3):
        resultinfo.append(0)
    return resultinfo
##===========================================================================
'''defs for unpixels'''
##===========================================================================
def searchdatainfo(pixeldata): # поиск расширения и длины данных
    expansionline, truthlength, lengExpline, preexpansionline = [], [], [], []
    init, counter = 0, 0
    for i in range(4, 6): #поиск длины расширения
        for j in range(3):
            if pixeldata[i][j] != 0:
                lengExpline.append(pixeldata[i][j])
    for i in range(len(lengExpline)): #перевод из байтового в 10ричное
        init += lengExpline[i]*(256**i)
    for i in range(6, len(pixeldata)): #поиск имени расширения данных
        for j in range(3):
            if counter != init:
                preexpansionline.append(pixeldata[i][j])
                counter +=1
            else:
                break
    for i in range(len(preexpansionline)): #дополнительная проверка
        if preexpansionline[i] != 0:
            expansionline.append(preexpansionline[i])
    for i in range(4): #поиск длины данных
        for j in range(3):
            truthlength.append(pixeldata[i][j])
    return expansionline, truthlength, init

def searchstartpoint(pixeldata): #поиск точки старта обработки
    lengexpansion = searchdatainfo(pixeldata)[2]
    return 7+ceil(lengexpansion//3)
##===========================================================================
'''PIXELATION'''
##===========================================================================
def PIXL(file_name): #кодирование файла в картинку RGB
    fileData, pixData = [], []
    file = open(file_name, 'rb') #чтение файла
    while (byte := file.read(1)):
        fileData.append(byte[0])
    file.close
    lengdata = len(fileData) #исходная длина данных
    infoData = info_file(file_name, lengdata) #получение списка данных 
    AllData = infoData + fileData
    width, leng = sizeinfo(AllData)[1], sizeinfo(AllData)[0] #размеры картинки
    for i in range(leng*width*3 - len(AllData)): #заполняем остатки для формирования картинки
        AllData.append(random.randrange(0, 255))
    for i in range(width): #формируем трехмерный список, создавая тем самым каркас картинки
        linepix = []
        for j in range(leng):
            point = (i*leng+j)*3
            pix = (AllData[point], AllData[point+1], AllData[point+2])
            linepix.append(pix)
        pixData.append(linepix)
    array = np.array(pixData, dtype=np.uint8) # окончательное формирование картинки
    new_image = Image.fromarray(array)
    return new_image.save('pxl' + str(random.randrange(1, 10000000)) + '.png')
##===========================================================================
'''UNPIXELATION'''
##===========================================================================
def UNPIXL(file_name): #декодирование данных, содержащиеся в картинке
    im = Image.open(file_name, 'r') #открытие и чтение картинки
    length, width = im.size 
    pixelData = list(im.getdata()) 
    im.close()
    fulldata, init, counter = [], 0, 0
    lengdata, expansionline, startpoint = searchdatainfo(pixelData)[1], searchdatainfo(pixelData)[0], searchstartpoint(pixelData) #получение данных для декодировки
    file_extension = bytearray(expansionline).decode() # получаем расширение данных
    for i in range(len(lengdata)): #исходная длина данных
        init += lengdata[i] * (256 ** i)
    for i in range(startpoint, width*length): #сборка данных из картинки
        for j in range(3):
            if counter != init:
                fulldata.append(pixelData[i][j])
                counter +=1
            else:
                break
    file_out = open('result' + str(random.randrange(1, 10000000)) + '.' + file_extension, 'wb') #получаем исходный файл с его данными
    file_out.write(bytearray(fulldata))  
    file_out.close()
##===========================================================================
colorama.init()
print("\033[3;32;40m                      _        _                                             \033[0;32;40m")
print("\033[3;32;40m                     | |      | |                                            \033[0;32;40m")
print("\033[3;32;40m  _ __ ___   __ _  __| | ___  | |__  _   _   _ __ ___   ___  _ __ ___ _ __   \033[0;32;40m")
print("\033[31m | '_ ` _ \ / _` |/ _` |/ _ \ | '_ \| | | | | '_ ` _ \ / _ \| '__/ _ \ '_ \  \033[31m")
print("\033[31m | | | | | | (_| | (_| |  __/ | |_) | |_| | | | | | | | (_) | | |  __/ | | | \033[31m")
print("\033[3;32;40m |_| |_| |_|\__,_|\__,_|\___| |_.__/ \__, | |_| |_| |_|\___/|_|  \___|_| |_| \033[0;32;40m")
print("\033[3;32;40m                                      __/ |                                  \033[0;32;40m")
print("\033[3;32;40m                                     |___/                                   \033[0;32;40m")
print('\033[31m --|{HEX CODER V4.2}|-- \033[31m')
print('\033[5;37;40m choose the type of script \033[0;37;40m')
print('\033[31m 1 -- encode file to png \033[31m')
print('\033[31m 2 -- decode png to file \033[31m')
print('\033[3;32;40m {My contacs: discord - Herman Garsky#2574 \033[3;32;40m')
print('\033[3;32;40m              telegram - https://t.me/morenskytm} \033[3;32;40m')
while True:
    choose = int(input(' num type: ')) 
    if choose == 1:
        print(PIXL(input(' write address file or namefile here >>> ')))
    elif choose == 2:
        print(UNPIXL(input(' write address picture or namepicture here >>> ')))
    else:
        break    