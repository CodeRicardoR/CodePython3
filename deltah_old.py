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
def copiar(anio,mes,dia,estaciones,estacion1_4,estacion2_4,estacion1_3,estacion2_3):#(2016,may,9)
    d2_anio=anio%100
    print d2_anio," ",anio," ", mes," ", dia, estaciones[0][0:3].upper()
    print str(datetime.datetime.now().timetuple().tm_yday)
    print "/home/cesar/isr/magnetometer/"+str(estacion2_4)+"/"+str(anio)+"/"+str(estacion2_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m"
    if os.path.exists("/home/cesar/isr/magnetometer/"+str(estacion2_4)+"/"+str(anio)+"/"+str(estacion2_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m"):
        os.system("cp /home/cesar/isr/magnetometer/"+str(estacion2_4)+"/"+str(anio)+"/"+str(estacion2_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m /data_server/temp/delta/")
        print "se realizo copia1"
    else:
        pass
    print "/home/cesar/isr/magnetometer/"+str(estacion1_4)+"/"+str(anio)+"/"+str(estacion1_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m"
    if os.path.exists("/home/cesar/isr/magnetometer/"+str(estacion1_4)+"/"+str(anio)+"/"+str(estacion1_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m"):
        os.system("cp /home/cesar/isr/magnetometer/"+str(estacion1_4)+"/"+str(anio)+"/"+str(estacion1_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m /data_server/temp/delta/")
        print "se realizo copia2"
    else:
        pass
def crear(anio,mes,dia,nombre_3):
    d2_anio=str(anio%100)
    archi=open(str(nombre_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m",'w')
    print "se creo"
    #archi=open("djp"+str(dia)+str(mes)+str(anio)+".m",'w')
    archi.close()
def grabar(anio,mes,dia,estaciones,nombre_3):
    d2_anio=str(anio%100)
    archi=open(str(nombre_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m",'a')
    archi.write("DELTA "+str(estaciones[0].upper())+"-"+str(estaciones[1].upper())+" <"+str(datetime.datetime.now().timetuple().tm_yday)+"> 1 Min. Reported data\n")
    archi.write('\n')
    archi.write(" DD MM YYYY  HH MM  D(Deg)  H(nT)  Z(nT)   I(Deg)  F(nT)\n")
    archi.write("\n")
    print "se grabo"
    archi.close()
def valores_iniciales(anio,mes,dia,estacion): #valores_iniciales(dia,jic)
    #try:
    print "valores in iciales :",str(anio),str(mes),str(dia),str(estacion)
    d2_anio=str(anio%100)
    print str(estacion)+str(dia)+str(mes)+"."+str(d2_anio)+"m"
    archij=open(str(estacion)+str(dia)+str(mes)+"."+str(d2_anio)+"m",'r')
    i=1
    for line in range(1,8):
        linea=archij.readline()#leemos cada linea
        try:
            b=linea.split(" ")#separamos la linea por espacios
            print "b_val :"+str(b)
	    if str(estacion)=='jic':
		b.insert(4,'')
            if i==5 and str(b[5])=="00" and str(b[6])=="00":#si la fila 5 tiene al minuto cero
                y0dj=b[8]
		print "y0dj"+str(y0dj)
                y0hj=b[9]
		print "y0hj"+str(y0hj)
                y0zj=b[10]
		print "y0zj"+str(y0zj)
                flag0="ab"
                flag1=0
                flag2=0
                return y0dj,y0hj,y0zj
            else:
                try:
                    b=linea.split(" ")
                    print str(b)
                    print "b[3] : "+str(b[3]) + b[4] : "+str(b[4])+"b[5] : "+str(b[5])+" b[6] : "+str(b[6])
                    #if str(b[4])=="":
                    #    print "vacio 4"
                    if str(b[3])=="00" and str(b[4])=="01":
                        #print "existe el minuto 1"
                        print "vacio X"
                        x1j=b[4]
                        y1dj=b[5]
                        y1hj=b[6]
                        y1zj=b[7]
                        flag1="ab"
                        #print x1,y1d,y1d,y1z
                    if str(b[3])=="00" and str(b[4])=="02":
                        #print "existe el minuto 2"
                        x2j=b[4]
                        y2dj=b[5]
                        y2hj=b[6]
                        y2zj=b[7]
                        flag2="ab"
                        #print x2,y2d,y2d,y2z
                    #if str(b[5])=="00":
                    #print "vacio 6"
                    if str(b[4])=="00" and str(b[5])=="01":#si la fila 5 tiene al minuto 1
                        print "vacio 6, minuto 1"
                        x1j=b[5]
                        y1dj=b[7]
                        y1hj=b[8]
                        y1zj=b[9]
                        flag1="ab"
                        #print x1,y1d,y1d,y1z
                    if str(b[4])=="00" and str(b[5])=="02":
                        #print "existe el minuto 2"
                        print "vacio 6, minuto 2"
                        x2j=b[5]
                        y2dj=b[7]
                        y2hj=b[8]
                        y2zj=b[9]
                        flag2="ab"
                        #print x2,y2d,y2d,y2z
                except:
                    flag1=""
                    flag2=""
        except:
            flag1=""
            flag2=""
        i=i+1
    #if flag0=="ab":
        #print "este es el caso de piura"
    if flag1=="ab" and flag2=="ab":
        y0dj=((0-float(x1j))*(float(y2dj)-float(y1dj))/(float(x2j)-float(x1j)))+float(y1dj)
        y0hj=((0-float(x1j))*(float(y2hj)-float(y1hj))/(float(x2j)-float(x1j)))+float(y1hj)
        y0zj=((0-float(x1j))*(float(y2zj)-float(y1zj))/(float(x2j)-float(x1j)))+float(y1zj)
        #flag1=="0"
        #flag2=="0"
    #print y0d,y0h,str(y0z).zfill(8)
        #tfila=" "+str(b[1])+" "+str(b[2])+" "+str(b[3])+"  "+str(b[5])+" 00  "+"-0.0".zfill(8)+" "+"-0.0".zfill(7)+" "+"-0.0".zfill(8)
        #grabartexto(dia,tfila)
        print "---------------------------",y0dj,y0hj,y0zj
        return y0dj,y0hj,y0zj
    #print tfila
    #del y0dj,y0hj,y0zj
    archij.close()
    #except:
    #    pass
    
def crear_matriz(anio,mes,dia,estacion):#crear_matriz(dia,"jic"):
    d2_anio=str(anio%100)
    dj=np.empty((24,60))
    hj=np.empty((24,60))
    zj=np.empty((24,60))
    archij=open(str(estacion)+str(dia)+str(mes)+"."+str(d2_anio)+"m",'r')
    for line in range(1,1500):
        lineaj=archij.readline()
        bj=lineaj.split(" ")
	if str(estacion)=='jic':
        
            bj.insert(4,'')
	print str(estacion)+'AQUI '+str(bj)
        try:
            #print int(bj[5])," ",int(bj[6])
            dj[int(bj[5]),int(bj[6])]=float(bj[8])
            #a=np.around((bj[8]) , decimals=3)
            #print a
            hj[int(bj[5]),int(bj[6])]=float(bj[9])
            zj[int(bj[5]),int(bj[6])]=float(bj[10])
        except:
            pass
    #print dj[0,0]
    #print hj[0,0]
    #print zj[0,0]
    #if int(dj[0,0])==0 and int(hj[0,0])==0 and int(zj[0,0])==0:
        #print "este es"
    try:
        y0dj,y0hj,y0zj=valores_iniciales(anio,mes,dia,estacion)
        dj[0,0]=y0dj
        hj[0,0]=y0hj
        zj[0,0]=y0zj
    except:
        pass
    #print valores_iniciales(dia,estacion)
    
    #else:
    #   pass
    #for i in range(24):
    #    print i
    #    print dj[i,:]
    #   print hj[i,:]
    #    print zj[i,:]
    archij.close()
    return dj,hj,zj
def cuantos_digitos(n):
    
    if n<0:
        n=-1*n
    i = 1
    while int(n/10)>=1:
        i=i+1
        n=int(n/10)
       
    bg=""
    for a in range(5-int(i)):
        bg=str(bg)+"0"
    return bg
def completar(n):
    if n>=0:
        n1=format(n,'.1f')
        en1=cuantos_digitos(float(n1))
        n1="+"+en1+n1
    if n<0:
        n1=-1*n
        n1=format(n1,'.1f')
        en1=cuantos_digitos(float(n1))
        n1="-"+en1+n1
    return n1
    #def borararchivo(anio,mes,dia):
def delta(anio,mes,dia,estaciones,nombre_3,estacion1_4,estacion2_4,estacion1_3,estacion2_3):
    d2_anio=str(anio%100)
    #print anio,mes, dia
    #print "d1"
    
    copiar(anio,mes,dia,estaciones,estacion1_4,estacion2_4,estacion1_3,estacion2_3)
    #print "Conexion Exitosa"
    #print "d12"
    
    os.chdir("/data_server/temp/delta/")
    
    #print os.getcwd()
    crear(anio,mes,dia,nombre_3)
    grabar(anio,mes,dia,estaciones,nombre_3) 
    #grabartexto(dia)
    month=["","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    mes1=int(month.index(str(mes)))
    
    #linea=archi.readline()
    #PARA EL CASO DE JICAMARCA, CUANDO TIENE EL MINUTO CERO, LOS VALORES INICIALES SON LOS DEL CERO,
    #CUANDO LE FALTA LOS VALORES INICIALES, SE INTERPOLA PARA EL VALOR DEL CERO.  
    esta1=estaciones[0][0:3]
    esta2=estaciones[1][0:3]
    print "esta1 : "+str(esta1)
    print "esta2 : "+str(esta2)   
    
    try:
        y0dj,y0hj,y0zj=valores_iniciales(anio,mes,dia,estacion1_3)
        try:
            y0dp,y0hp,y0zp=valores_iniciales(anio,mes,dia,estacion2_3)
            dj,hj,zj=crear_matriz(anio,mes,dia,estacion1_3)
            dp,hp,zp=crear_matriz(anio,mes,dia,estacion2_3)
            djp=(dj-float(y0dj))-(dp-float(y0dp))
            hjp=(hj-float(y0hj))-(hp-float(y0hp))
            zjp=(zj-float(y0zj))-(zp-float(y0zp))
            tempp=0
            temph=0
            tempz=0
            count=0
            archi=open(str(nombre_3)+str(dia)+str(mes)+"."+str(d2_anio)+"m",'a')
            for h in range(24):
                if h<10:
                    h="0"+str(h)
                for i in range(60):
                    if i<10:
                        i="0"+str(i)
                    if djp[h,i]>=0 and djp[h,i]<10:
                        djphi="+0"+format(djp[h,i],'.4f')
                    if djp[h,i]<0 and djp[h,i]>-9:
                        djphi=-1*djp[h,i]
                        djphi="-0"+format(djphi,'.4f')
                    #vemos si los datos diferen mucho, no hay nada
                    
                    
                    difp=abs(float(djphi)-float(tempp))
                    difh=abs(float(completar(hjp[h,i]))-float(temph))
                    difz=abs(float(completar(zjp[h,i]))-float(tempz))
                    #temp4=djphi
                    print count," ",difp," ", difh," ", difz
                    #signal=count," ",difp," ", difh," ", difz
		    #archi.write(str(signal)+"\n")
		    #print "Signal"
			
                    if abs(difp)<0.015 and abs(difh)<50 and abs(difz)<10:
                        print "entra a condicion"
                        count=int(count)+1
                        if mes1<10:
                            mese="0"+str(mes1)
                        if mes1>=10:
                            mese=str(mes1)
                        f_d=djphi
                        tempp=djphi
                        f_h=completar(hjp[h,i])
                        temph=completar(hjp[h,i])
                        f_z=completar(zjp[h,i])
                        tempz=completar(zjp[h,i])
                        #print f_d
                        tfila=" "+str(dia)+" "+str(mese)+" "+str(anio)+"  "+str(h)+" "+str(i)+"  "+f_d+" "+f_h+" "+f_z+" 0 0"
                        print tfila
                        archi.write(str(tfila)+"\n")
                    else:
                        pass
                        '''
                        tfila=" "+str(dia)+" "+str(mese)+" "+str(anio)+"  "+str(h)+" "+str(i)+"  "+"+99.999"+" "+"+99999.9"+" "+"+99999.9"+" 0 0"
                        print tfila
                        archi.write(str(tfila)+"\n")
                        '''
                    #print mes1, type(mes1)
            archi.close()
        except:
            pass
    except:
        pass
    #os.system("pwd")
    #por aqui me quede, REVISAR!!!!!!!!!!!!!!!!!!
    #if os.path.isfile(str(stat)+"_"+str(d2_anio)+str(smes)+str(sdia)+".min"):
    #print y0dj,y0hj,y0zj ,"Jica"
    #valores_iniciales(dia,"piu")
    
#leertexto(dia)
def main1(estaciones,nombre_3,nombre_4,estacion1_4,estacion2_4,estacion1_3,estacion2_3):
	   
    #os.chdir("/data_server/temp/delta/")
    f = datetime.datetime.now()
    #f= datetime.date(2015,06,14)
    print str(type(f))+"fecha FORMATO"
    month=["","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    #print "3"
    if f.day<10:
        day="0"+str(f.day)
    else:
        day=str(f.day)
    delta(f.year,month[f.month],day,estaciones,nombre_3,estacion1_4,estacion2_4,estacion1_3,estacion2_3)
    nombre=str(nombre_3)+str(day)+str(month[f.month])+"."+str(f.year%100)+"m"
    print "nombre: "+str(nombre)
    d2_anio=f.year%100
    #print d2_anio," ",anio," ", mes," ", dia
    size_delta=os.path.getsize(nombre)
    print "size_delta : "+str(size_delta)
    
    if int(size_delta)>120:
        print "no tamanio cero"
        try:
            os.system("cp /data_server/temp/delta/"+str(nombre)+" /home/cesar/isr/magnetometer/"+str(nombre_4)+"/"+str(f.year))
        except:
            pass
        os.chdir("/home/cesar/isr/magnetometer/"+str(nombre_4)+"/"+str(f.year))
        try:
            os.popen("sudo chown cesar:cesar "+str(nombre),"w").write("Leaatduscuee1GP")
            os.system("chown cesar:cesar "+str(nombre))
        except:
            pass
    elif int(size_delta)<=120:
        pass
    else:
        pass
def main2():
    month=["","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    for ii in range(1,7): #meses
        for i in range(1,32): #dias
            if i<10:
                i="0"+str(i)
            else:
                i=str(i)
            delta(2016,month[ii],i)#delta(2016,month[5],26)
            nombre="djp"+str(i)+str(month[ii])+"."+str(16)+"m"
            try:
                os.system("cp /data_server/temp/delta/"+str(nombre)+" /home/cesar/isr/magnetometer/dejp/"+str(2016))
            except:
                pass
            os.chdir("/home/cesar/isr/magnetometer/dejp/"+str(2016))
            try:
                os.popen("sudo chown cesar:cesar "+str(nombre),"w").write("L3upicf33lfI")
                os.system("chown cesar:cesar "+str(nombre))
            except:
                pass
        ii=ii+1
def main3():
    '''
    Programa que escribe todos los deltaH en la carpeta /home/cesar/isr/magnetometer/dejp
    PASOS
    1. Ejecutar este script con solo este main
    2. Ejecutar el programa getmag.py(Ejemplo: ./get_mag.py -S montecillo -s dejp -w 2019,01,01 2019,03,23)  que esta en RAID!!! para que actualice todos los datos del deltaH
   
'''
    month=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    for anio in range(2019,2019+1):
        for mes in month:
            for dia in range(1,2):
                print "anio : "+str(anio)+ " mes : "+str(mes)+" dia : ",str(dia)
                #day=12 
                #month="jun"
                #year=2016    
                if dia<10:
                    dia="0"+str(dia)
                nombre="djp"+str(dia)+str(mes)+"."+str(anio%100)+"m"

		#delta(anio,mes,dia,estaciones,nombre_3,estacion1_4,estacion2_4,estacion1_3,estacion2_3)
                delta(anio,mes,dia,["Jicamarca","Piura"],"djp","jica","piur","jic","piu")
                try:
                    os.system("cp /data_server/temp/delta/"+str(nombre)+" /home/cesar/isr/magnetometer/dejp/"+str(anio))
                except:
                    pass
                os.chdir("/home/cesar/isr/magnetometer/dejp/"+str(anio))
                try:
                    os.popen("sudo chown cesar:cesar "+str(nombre),"w").write("L3upicf33lfI")
                    os.system("chown cesar:cesar "+str(nombre))
                except:
                    pass
                
def main4():    
    '''Script que cambia de nombre a archivos, en especial a los que estan en
    lisn.igp.gob.pe/data/users/magnetometer/Data/dj-p/2000 y tienen el nombre j-p02oct.00m cambiarlos a dejp02oct.00m
    
    '''
    os.chdir("/data/users/magnetometer/Data/dejp/2000")
    #os.system("pwd")
    archi=open("j-p01dec.00m","r")
    contenido = archi.read()
    #print contenido
    archi.close()
    archi1=open("djp01dec.00m",'w')
    archi1.write(str(contenido))
    archi1.close()
    month=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    #month=["sep"]
    for anio in range(2000,2017):
        print anio
        d2_anio=anio%100
        if d2_anio<10:
            d2_anio="0"+str(d2_anio)
        else:
            d2_anio=str(d2_anio)
        os.chdir("/data/users/magnetometer/Data/dejp/"+str(anio))
        os.system("pwd")
        #os.chdir("/data/users/magnetometer/Data/dejp/2000")
        for mes in month:
            for i in range(0,32): #dias de mes
                #print str(i)
                if i<10:
                    dia="0"+str(i)
                else:
                    dia=str(i)
                nombre_original="j-p"+dia+mes+"."+str(d2_anio)+"m"
                #print nombre_original,os.path.isfile(str(nombre_original))
                if os.path.isfile(str(nombre_original))==True:
                    try:
                        archi2=open(nombre_original,"r")
                        archi3=open("djp"+dia+mes+"."+str(d2_anio)+"m",'w')
                        for line in range(1,5):
                            linea=archi2.readline()#leemos cada linea
                            archi3.write(str(linea))
                        for line in range(5,1445):
                            linea=archi2.readline()
                            b=linea.split(" ")
                            c=[]
                            l1=len(b)
                            for ii in range(0,l1):
                                if str(b[ii])=="":
                                    pass
                                else:
                                    c.append(str(b[ii]))
                            #print str(c), len(c)
                            if str(c[5])=="99.9990":
                                pass
                            else:
                                linea2=" "+str(c[0])+" "+str(c[1])+" "+str(c[2])+"  "+str(c[3])+" "+str(c[4])+"  "+str(c[5])+" "+str(c[6])+" "+str(c[7][:-2])+" 0 0"+"\n"
                                archi3.write(str(linea2))
                                print str(linea2)
                            #archi3.write(str(linea2))
    
                        archi2.close()
                        archi3.close()
                     
                    except:
                        pass
                    #print os.path.isfile(str(nombre_original))+" Existe"
            #print os.path.isfile("j-p01dec.00m")
#main1(["Nombre de la estacion 1","Nombre de la estacion 2"],"se pone "d" al inicio, luego se siguen las iniciales las estaciones","se pone "de" al inicio, luego se siguen las iniciales las estaciones","nombre de carpeta de la estacion1 como en /home/cesar/isr/magnetometer/"jica"/2017","parecido al anterior","jic","piu")


main1(["Jicamarca","Piura"],"djp","dejp","jica","piur","jic","piu")
main1(["Alta Floresta","Cuiaba"],"dac","deac","alta","cuib","alf","cba")


#main3()
