from PIL import Image
import colorama
import numpy as np
import random
import os.path
import math as ma
##===========================================================================
'''def libary pixl'''
##===========================================================================
def truelenginfo(lenginfo): #определение длины данных
    lengslayer = []
    while lenginfo > 0:
        lengslayer.append(lenginfo % 256)
        lenginfo = lenginfo // 256
    for i in range(12 - len(lengslayer)):
        lengslayer.append(0)
    return lengslayer

def typefileinfo(file_name): #определение типа файла
    resulttype, typ = [], []
    f = file_name.split('.')
    typename = bytearray(f[-1], 'utf-8')
    for i in range(len(typename)):
        resulttype.append(typename[i])
    typ = resulttype
    for i in range(len(resulttype)%3):
        resulttype.append(0)
    return resulttype, typ

def lengofTFI(file_name): #длина типа данных
    typ, slayOftyp = typefileinfo(file_name)[1], []
    lengtyp = len(typ)
    while lengtyp > 0:
        slayOftyp.append(lengtyp % 256)
        lengtyp = lengtyp // 256
    for i in range(6 - len(slayOftyp)):
        slayOftyp.append(0)    
    return slayOftyp    

def info_file(file_name, lenginfo): #группировка информации о данных файла
    info_lengdata, info_typefile, info_lengtypedata = truelenginfo(lenginfo), typefileinfo(file_name)[0], lengofTFI(file_name)
    resultinfo = info_lengdata + info_lengtypedata + info_typefile
    resultinfo.append(0)
    for i in range(3-len(resultinfo)%3):
        resultinfo.append(0)
    return resultinfo
##===========================================================================
'''defs for unpixels'''
##===========================================================================
def searchdatainfo(pixeldata): #декодирование данных файла
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

def searchstartpoint(pixeldata): #поиск точки старта
    lengexpansion = searchdatainfo(pixeldata)[2]
    return 7+ma.ceil(lengexpansion//3)
##===========================================================================
'''PIXELATION'''
##===========================================================================
def PIXEL(file_name):
    fileData, pixelData, pictureData = [], [], []
    file = open(file_name, 'rb') # чтение данных файла в массив fileData
    while (byte := file.read(1)):
        fileData.append(byte[0])
    file.close
    fileLength = len(fileData)
    fileHeader = info_file(file_name, fileLength)
    pixelData = fileHeader + fileData # склеивание заголовка и данных в одно
    for i in range(3-len(pixelData)%3): # дополнение данных файла до длины кратной 3
        pixelData.append(random.randrange(0, 255))
    for i in range(len(pixelData) // 3): #создание трехмерного массива
        pix_cell = [(pixelData[i*3], pixelData[i*3+1], pixelData[i*3+2])]
        pictureData.append(pix_cell)
    array = np.array(pictureData, dtype=np.uint8) # преобразование в набор пикселей для создания картинки
    new_image = Image.fromarray(array)
    return new_image.save('pxl' + str(random.randrange(1, 10000000)) + '.png')
##===========================================================================
'''UNPIXELATION Hex_CoderV4.py'''
##===========================================================================
def UNPIXEL(file_name):
    im = Image.open(file_name, 'r') #чтение содержания файла
    lenght, width = im.size 
    pixel_values = list(im.getdata()) 
    im.close()
    fulldata, init, counter = [], 0, 0
    expansionline, truthlength, startpoint = searchdatainfo(pixel_values)[0], searchdatainfo(pixel_values)[1], searchstartpoint(pixel_values) #получение необходимых данных для поиска остального
    file_extension = bytearray(expansionline).decode() #получение имени 
    for i in range(len(truthlength)): #алгоритм преобразования байтов в числовые значения длины исходных данных изображения
        init += truthlength[i] * (256 ** i)    
    for i in range(startpoint, width): #зная длину данных, находим их из общего и записываем в отдельный список для дальнейшего декодирования
        for j in range(3):
            if counter != init:
                fulldata.append(pixel_values[i][j])
                counter +=1
            else:
                break
    file_out = open('result' + str(random.randrange(1, 10000000)) + '.' + file_extension, 'wb') #создаем файл, в который мы помещаем все полученное в функции
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
print('\033[31m --|{HEX CODER V4.1}|-- \033[31m')
print('\033[5;37;40m choose the type of script \033[0;37;40m')
print('\033[31m 1 -- encode file to png \033[31m')
print('\033[31m 2 -- decode png to file \033[31m')
print('\033[3;32;40m {My contacs: discord - Herman Garsky#2574 \033[3;32;40m')
print('\033[3;32;40m              telegram - https://t.me/morenskytm} \033[3;32;40m')
while True:
    choose = int(input('num type: '))
    if choose == 1:
        ff = input('write address file or namefile here >>> ')
        print(PIXEL(ff))
    elif choose == 2:
        ff = input('write address picture or namepicture here >>> ')
        print(UNPIXEL(ff))
    else:
        break