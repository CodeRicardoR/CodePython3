#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
JOSE GM
Programa que calcula delta de D,H,Z  de cualquier par de estaciones
para luego guardarlo en home/cesar/isr/magnetometer/**nombre_de_la_nueva_estacion
V1.2 - 2016/08/29 - Se corrigio en la funcion copiar, se cambio el try por el if, para ver si existe tal archivo.
V1.3 - 2016/08/31 - Se corregio problema cuando no habia data de Piura, lo que hace ahora, es cuando el archivo no tiene data, no copia el archivo deltaH a lisn.igp.gob.pe/home/cesar/isr/magnetometer/dejp/año
V1.4 - 201703/01  - se modifico script para que corriera con cualquier par de estacion
V1.5 - 2017/03/28 - se modifico condicion de copiado de archivos delta, solo se copian si el tamaño del archivo es mayor a 120 bytes.(este valor es un promedio de tamaño de archivos solo con cabecera)
'''
import os
import numpy as np
import time
from numpy import matrix
from ftplib import FTP
import shutil
import commands
import datetime

def copiar(anio, mes, dia, estaciones, estacion1_4, estacion2_4, estacion1_3, estacion2_3):#(2016,may,9)
    d2_anio = anio%100
    print(d2_anio," ",anio," ", mes," ", dia, estaciones[0][0:3].upper())
    print(str(datetime.datetime.now().timetuple().tm_yday))
    
    print("/home/cesar/isr/magnetometer/"+str(estacion2_4)+"/"+str(anio)+"/"+str(estacion2_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m")
    if os.path.exists("/home/cesar/isr/magnetometer/"+str(estacion2_4)+"/"+str(anio)+"/"+str(estacion2_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m"):
        os.system("cp /home/cesar/isr/magnetometer/"+str(estacion2_4)+"/"+str(anio)+"/"+str(estacion2_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m /data_server/temp/delta/")
        print("se realizo copia1")


    print("/home/cesar/isr/magnetometer/"+str(estacion1_4)+"/"+str(anio)+"/"+str(estacion1_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m")
    if os.path.exists("/home/cesar/isr/magnetometer/"+str(estacion1_4)+"/"+str(anio)+"/"+str(estacion1_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m"):
        os.system("cp /home/cesar/isr/magnetometer/"+str(estacion1_4)+"/"+str(anio)+"/"+str(estacion1_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m /data_server/temp/delta/")
        print("se realizo copia2")


def crear(anio, mes, dia,nombre_3):
    d2_anio = str(anio%100)
    File_name = str(nombre_3) + str(dia) + str(mes) + "." + str(d2_anio) + "m"
    archi = open(File_name, 'w')
    archi.close()
    print( File_name + " Creado!")

def grabar(anio, mes, dia, estaciones, nombre_3):
    d2_anio = str(anio%100)
    archi=open(str(nombre_3) + str(dia) + str(mes) + "." + str(d2_anio) + "m",'a')
    archi.write("DELTA "+str(estaciones[0].upper())+"-"+str(estaciones[1].upper())+" <"+str(datetime.datetime.now().timetuple().tm_yday)+"> 1 Min. Reported data\n")
    archi.write('\n')
    archi.write("DD MM YYYY HH MM   D(deg)   H(nT)    Z(nT)    I(deg)   F(nT)\n")
    archi.write("\n")
    archi.close()

def valores_iniciales(anio, mes, dia, estacion): #valores_iniciales(dia,jic)
    print("valores in iciales :", str(anio), str(mes), str(dia), str(estacion))
    d2_anio = str(anio%100)
    print(str(estacion) + str(dia) + str(mes) + "." + str(d2_anio)+"m")
    archij = open(str(estacion) + str(dia) + str(mes) + "." + str(d2_anio) + "m", 'r')

    i=1
    flag0 = 0
    flag1 = 0
    flag2 = 0
    for line in range(1,8):
        linea = archij.readline()#leemos cada linea
        try:
            b = linea.split()
            print("b_val1 :" + str(b))
            if (i == 5) and (str(b[3])=="00") and (str(b[4])=="00"):#si la fila 5 tiene al minuto cero
                y0dj = b[5]
                print("y0dj"+str(y0dj))
                y0hj = b[6]
                print("y0hj"+str(y0hj))
                y0zj = b[7]
                print("y0zj"+str(y0zj))
                flag0 = "ab"
                return y0dj, y0hj, y0zj
            else:
                try:
                    b = linea.split()
                    print("b_val2 :" + str(b))
                    if (str(b[3]) == "00") and (str(b[4]) == "01"):
                        #print "existe el minuto 1"
                        x1j=b[4]
                        y1dj=b[5]
                        y1hj=b[6]
                        y1zj=b[7]
                        flag1="ab"
                        #print x1,y1d,y1d,y1z
                    if (str(b[3]) == "00") and (str(b[4]) == "02"):
                        #print "existe el minuto 2"
                        x2j=b[4]
                        y2dj=b[5]
                        y2hj=b[6]
                        y2zj=b[7]
                        flag2="ab"
                        #print x2,y2d,y2d,y2z
                except:
                    pass
        except:
            pass

        i = i + 1

    if (flag1 == "ab") and (flag2 == "ab"):
        y0dj=((0-float(x1j))*(float(y2dj)-float(y1dj))/(float(x2j)-float(x1j)))+float(y1dj)
        y0hj=((0-float(x1j))*(float(y2hj)-float(y1hj))/(float(x2j)-float(x1j)))+float(y1hj)
        y0zj=((0-float(x1j))*(float(y2zj)-float(y1zj))/(float(x2j)-float(x1j)))+float(y1zj)
        print("---------------------------", y0dj, y0hj, y0zj)
        return y0dj,y0hj,y0zj

    archij.close()

    
def crear_matriz(anio, mes, dia, estacion):#crear_matriz(dia,"jic"):
    d2_anio = str(anio%100)

    dj = np.empty((24,60))
    hj = np.empty((24,60))
    zj = np.empty((24,60))

    archij = open(str(estacion) + str(dia) + str(mes) + "." + str(d2_anio) + "m", 'r')

    for line in range(1,1500):
        lineaj=archij.readline()
        bj = lineaj.split()
        print(str(estacion) + 'AQUI ' + str(bj))
        try:
            dj[int(bj[3]), int(bj[4])] = float(bj[5])
            hj[int(bj[3]), int(bj[4])] = float(bj[6])
            zj[int(bj[3]), int(bj[4])] = float(bj[7])
        except:
            pass
    try:
        y0dj, y0hj, y0zj = valores_iniciales(anio, mes, dia, estacion)
        dj[0,0] = y0dj
        hj[0,0] = y0hj
        zj[0,0] = y0zj
    except:
        pass

    archij.close()
    return dj, hj, zj

def cuantos_digitos(n):
    
    if n<0:
        n = -1*n

    i = 1
    while int(n/10) >= 1:
        i = i+1
        n = int(n/10)
       
    bg = ""
    for a in range(5 - int(i)):
        bg = str(bg) + "0"
    
    return bg

def completar(n):
    if n >= 0:
        n1 = format(n, '.1f')
        en1 = cuantos_digitos(float(n1))
        n1 = "+" + en1 + n1
    if n < 0:
        n1 = -1*n
        n1 = format(n1,'.1f')
        en1 = cuantos_digitos(float(n1))
        n1 = "-" + en1 + n1

    return n1


def delta(anio, mes, dia, estaciones, nombre_3, estacion1_4, estacion2_4, estacion1_3, estacion2_3):
    d2_anio=str(anio%100)
    
    copiar(anio, mes, dia, estaciones, estacion1_4, estacion2_4, estacion1_3, estacion2_3)
    
    os.chdir("/data_server/temp/delta/")
    
    crear(anio, mes, dia, nombre_3)
    grabar(anio, mes, dia, estaciones, nombre_3) 

    month = ["", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    mes1 = int(month.index(str(mes)))
    
    #linea=archi.readline()
    #PARA EL CASO DE JICAMARCA, CUANDO TIENE EL MINUTO CERO, LOS VALORES INICIALES SON LOS DEL CERO,
    #CUANDO LE FALTA LOS VALORES INICIALES, SE INTERPOLA PARA EL VALOR DEL CERO.  
    esta1 = estaciones[0][0:3]
    esta2 = estaciones[1][0:3]
    print("Esta1 : "+str(esta1))
    print("Esta2 : "+str(esta2))
    
    try:
        y0dj, y0hj, y0zj = valores_iniciales(anio, mes, dia, estacion1_3)
        try:
            y0dp, y0hp, y0zp = valores_iniciales(anio, mes, dia, estacion2_3)
            dj, hj, zj = crear_matriz(anio, mes, dia, estacion1_3)
            dp, hp, zp = crear_matriz(anio, mes, dia, estacion2_3)
            djp = (dj-float(y0dj)) - (dp-float(y0dp))
            hjp = (hj-float(y0hj)) - (hp-float(y0hp))
            zjp = (zj-float(y0zj)) - (zp-float(y0zp))
            tempp=0
            temph=0
            tempz=0
            count=0
            archi = open(str(nombre_3) + str(dia) + str(mes) + "." + str(d2_anio) + "m", 'a')
            for h in range(24):
                if h<10:
                    h = "0" + str(h)
                for i in range(60):
                    if i<10:
                        i = "0" + str(i)
                    if (djp[h,i] >= 0) and (djp[h,i] < 10):
                        djphi = "+0" + format(djp[h,i],'.4f')
                    if (djp[h,i] < 0) and (djp[h,i] > -9):
                        djphi = -1*djp[h,i]
                        djphi = "-0" + format(djphi,'.4f')
                    #vemos si los datos diferen mucho, no hay nada
                    difp = abs(float(djphi) - float(tempp))
                    difh = abs(float(completar(hjp[h,i])) - float(temph))
                    difz = abs(float(completar(zjp[h,i])) - float(tempz))
                    #temp4=djphi
                    print(count," ",difp," ", difh," ", difz)
			
                    if (abs(difp) < 0.015) and (abs(difh) < 50) and (abs(difz) < 10):
                        print("entra a condicion")
                        count = int(count) + 1
                        if mes1 < 10:
                            mese = "0"+str(mes1)
                        if mes1 >= 10:
                            mese = str(mes1)

                        f_d = djphi
                        tempp = djphi

                        f_h = completar(hjp[h,i])
                        temph = completar(hjp[h,i])

                        f_z = completar(zjp[h,i])
                        tempz = completar(zjp[h,i])

                        #print f_d
                        tfila = " " + str(dia) + " " + str(mese) + " " + str(anio) + "  " + str(h) + " " + str(i) + "  " + f_d + " " + f_h + " " + f_z + " 0 0"
                        print(tfila)
                        archi.write(str(tfila)+"\n")
                    else:
                        pass

            archi.close()
        except:
            pass
    except:
        pass

def main1(estaciones, nombre_3, nombre_4, estacion1_4, estacion2_4, estacion1_3, estacion2_3):
	   
    f = datetime.datetime.now()
    print(str(type(f)) + ": fecha FORMATO")

    month = ["", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    if f.day < 10:
        day = "0" + str(f.day)
    else:
        day = str(f.day)

    delta(f.year, month[f.month], day, estaciones, nombre_3, estacion1_4, estacion2_4, estacion1_3, estacion2_3)

    nombre = str(nombre_3) + str(day) + str(month[f.month]) + "." + str(f.year%100) + "m"
    print("Name file: " + str(nombre))
    size_delta = os.path.getsize(nombre)
    print("size_delta : " + str(size_delta))
    
    if int(size_delta) > 120:
        try:
            os.system("cp /data_server/temp/delta/" + str(nombre) + " /home/cesar/isr/magnetometer/" + str(nombre_4) + "/" + str(f.year))
        except:
            pass

        os.chdir("/home/cesar/isr/magnetometer/" + str(nombre_4) + "/" + str(f.year))
        try:
            os.popen("sudo chown cesar:cesar " + str(nombre), "w").write("Leaatduscuee1GP")
            os.system("chown cesar:cesar " + str(nombre))
        except:
            pass


main1(["Jicamarca", "Tarapoto"], "djt", "dejt", "jica", "tara", "jic", "tar")
