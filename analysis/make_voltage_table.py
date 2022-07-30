# -*- coding: utf-8 -*-
import os, sys
import numpy as np

R_high = 15000
R1_level = 256
R1_Value = 10000
R2_level = 256
R2_Value = 10000
R_low = 1000
Rw = 50

output_file = "E:\GitHub\W-Power\\analysis\\voltage_table.h"

R1 = []
R2 = []
i = 0
while (i < R1_level):
    R1.append(Rw + i * (R1_Value / R1_level))
    i += 1

i = 0
while (i < R2_level):
    R2.append(Rw + i * (R2_Value / R2_level))
    i += 1

r1_list = []
r2_list = []
for i in R1:
    for j in R2:
        if (20000 <= (R_low + i + j + R_high) <= 30000):
            r1_list.append(i)
            r2_list.append(j)

Uv = []
r1_select = []
r2_select = []
for i in range(len(r1_list)):
    U = round((1.2 * (1 + (r1_list[i] + R_high) / (r2_list[i] + R_low))), 2)
    if (U <= 28 and (any(np.isin(Uv, U)) == False)):
        Uv.append(U)
        r1_select.append(r1_list[i])
        r2_select.append(r2_list[i])

step = 0.1

U_ultima = []
R1_ultima = []
R2_ultima = []
i = 0
replacetime = 0
while (i <= 28):
    try:
        index = Uv.index(i)
    except:
        print("can not implement:", i)
        bias = 0
        while (bias < 10):
            i -= 0.01
            i = round(i, 2)
            try:
                index = Uv.index(i)
            except:
                bias += 1
            else:
                replacetime += 1
                print("use", i, " to replace, time:", replacetime)
                U_ultima.append(i)
                R1_ultima.append((int)((r1_select[index] - Rw) / (R1_Value / 256)))
                R2_ultima.append((int)((r2_select[index] - Rw) / (R2_Value / 256)))
                break
        i += bias * 0.01 + 0.01
        i = round(i, 1)
    else:
        U_ultima.append(i)
        R1_ultima.append((int)((r1_select[index] - Rw) / (R1_Value / 256)))
        R2_ultima.append((int)((r2_select[index] - Rw) / (R2_Value / 256)))

    i += 0.1
    i = round(i, 1)

f_open = open(output_file, "w+")
f_open.write("#ifndef __VOLTAGE_TABLA_H__\n#define __VOLTAGE_TABLA_H__\n\n")

f_open.write("/*********************\n")
f_open.write("*       Vout\n")
f_open.write("*       ___\n")
f_open.write("*        |\n")
f_open.write("*        _\n")
f_open.write("*       | | (R1 + R1b)\n")
f_open.write("*       |_|\n")
f_open.write("*  FB----|\n")
f_open.write("*        _\n")
f_open.write("*       | | (R2 + R2b)\n")
f_open.write("*       | |\n")
f_open.write("*        T\n")
f_open.write("*        |\n")
f_open.write("*       --- GND\n")
f_open.write("*        -\n")
f_open.write("*  Vout = 1.2 * (1 + (R1 + R1b) / (R2 + R2b))\n")
f_open.write("*\n")
f_open.write("*  The RESISTOR(R1b) above R1 has a resistance of " + str(R_high) + " ohm\n")
f_open.write("*  The RESISTOR(R2b) below R2 has a resistance of " + str(R_low) + " ohm\n")
f_open.write("*********************/\n")

f_open.write("\nconst float voltage_table[] = {\n    ")
for i in range(len(U_ultima)):
    if i == len(U_ultima) - 1:
        f_open.write(str(U_ultima[i]))
        break
    f_open.write(str(U_ultima[i]) + ", ")
    if ((i + 1) % 10 == 0):
        f_open.write("\n    ")
f_open.write("\n};\n")

f_open.write("\nconst int R1_table[] = {\n    ")
for i in range(len(R1_ultima)):
    if i == len(R1_ultima) - 1:
        f_open.write(str(R1_ultima[i]))
        break
    f_open.write(str(R1_ultima[i]) + ", ")
    if ((i + 1) % 10 == 0):
        f_open.write("\n    ")
f_open.write("\n};\n")

f_open.write("\nconst int R2_table[] = {\n    ")
for i in range(len(R2_ultima)):
    if i == len(R2_ultima) - 1:
        f_open.write(str(R2_ultima[i]))
        break
    f_open.write(str(R2_ultima[i]) + ", ")
    if ((i + 1) % 10 == 0):
        f_open.write("\n    ")
f_open.write("\n};\n")

f_open.write("\n#endif\n")

f_open.close()