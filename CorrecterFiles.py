
import sys

#23 06 2023 15 28 -06.2215 +22930.0 -04378.3 -10.8100 +23344.3
#23 06 2023 15 29 -06.2213 +22930.6 -04378.3 -10.8099 +23344.9

#23 06 2023 15 37 -06.4465 +23063.8 -04343.8 -10.6658 +23469.2



#D_inc = (-06.2213) - (-06.2215)
#H_inc = (+22930.6) - (+22930.0)
#Z_inc = (-04378.3) - (-04378.3)
#I_inc = (-10.8099) - (-10.8100)
#F_inc = (+23344.9) - (+23344.3)

#D_normal = (-06.2213) + D_inc
#H_normal = (+22930.6) + H_inc
#Z_normal = (-04378.3) + Z_inc
#I_normal = (-10.8099) + I_inc
#F_normal = (+23344.9) + F_inc

#D_error = (-06.4465) - D_normal
#H_error = (+23063.8) - H_normal
#Z_error = (-04343.8) - Z_normal
#I_error = (-10.6658) - I_normal
#F_error = (+23469.2) - F_normal

#print("D_error: ", D_error)
#print("H_error: ", H_error)
#print("Z_error: ", Z_error)
#print("I_error: ", I_error)
#print("F_error: ", F_error)

#-----------------------------------------
#D_error:  -0.2253999999999996
#H_error:  132.60000000000218
#Z_error:  34.5
#I_error:  0.14400000000000013
#F_error:  123.69999999999709

D_error = -0.2253999999999996
H_error = 132.60000000000218
Z_error = 34.5
I_error = 0.14400000000000013
F_error = 123.69999999999709
#-----------------------------------------


f1 = open(sys.argv[1], 'r')
lines1 = f1.readlines()
f1.close()

f2 = open(sys.argv[1][:-4] + "cor.txt", 'w')

for i in lines1:
    a = i.split()
    
    if len(a) != 10:
        continue
    try:
        #Corrigiendo
        DataD = float(a[5]) - D_error
        DataH = float(a[6]) - H_error
        DataZ = float(a[7]) - Z_error
        DataI = float(a[8]) - I_error
        DataF = float(a[9]) - F_error
        a[5] = "%+08.4f"%DataD
        a[6] = "%+08.1f"%DataH
        a[7] = "%+08.1f"%DataZ
        a[8] = "%+08.4f"%DataI
        a[9] = "%+08.1f"%DataF
        #excribiendo
        linea = " ".join(a)
        f2.write(linea + "\n")
    except:
        continue

f2.close()
