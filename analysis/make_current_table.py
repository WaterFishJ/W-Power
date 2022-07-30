# -*- coding: utf-8 -*-
import os, sys
import numpy as np

R_low = 000
R18_level = 256
R18_Value = 50000
R19_level = 256
R19_Value = 50000
R_high = 31000
Rw = 50

output_file = "E:\GitHub\W-Power\\analysis\current_table.h"

R18 = []
R19 = []
i = 0
while (i < R18_level):
    R18.append(Rw + i * (R18_Value / R18_level))
    i += 1

i = 0
while (i < R19_level):
    R19.append(Rw + i * (R19_Value / R19_level))
    i += 1

r18_list = []
r19_list = []
for i in R18:
    for j in R19:
        if (50000 < (R_low + i + j + R_high) < 70000):
            r18_list.append(i)
            r19_list.append(j)

Ia = []
r18_select = []
r19_select = []
for i in range(len(r18_list)):
    I = round((480 * (r18_list[i] + R_low))/(7 * (r18_list[i] + R_low + r19_list[i] + R_high)), 2)
    if (I <= 15 and (any(np.isin(Ia, I)) == False)):
        Ia.append(I)
        r18_select.append(r18_list[i])
        r19_select.append(r19_list[i])

step = 0.1

I_ultima = []
R18_ultima = []
R19_ultima = []
i = 0
while (i <= 15):
    try:
        index = Ia.index(i)
    except:
        print("can not implement:", i)
        bias = 0
        while (bias < 10):
            i -= 0.01
            i = round(i, 2)
            try:
                index = Ia.index(i)
            except:
                bias += 1
            else:
                print("use", i, " to replace")
                I_ultima.append(i)
                R18_ultima.append((int)((r18_select[index] - Rw) / (R18_Value / 256)))
                R19_ultima.append((int)((r19_select[index] - Rw) / (R19_Value / 256)))
                break
        i += bias * 0.01 + 0.01
        i = round(i, 1)
    else:
        I_ultima.append(i)
        R18_ultima.append((int)((r18_select[index] - Rw) / (R18_Value / 256)))
        R19_ultima.append((int)((r19_select[index] - Rw) / (R19_Value / 256)))

    i += 0.1
    i = round(i, 1)

# for i in range(len(I_ultima)):
#     print(I_ultima[i], 1.2 * ((R18_ultima[i] * (R18_Value / R18_level) + Rw) / ((R18_ultima[i] * (R18_Value / R18_level) + Rw) + (R19_ultima[i] * (R19_Value / R19_level) + Rw) + 31000)) / 2.5 / 0.007)

f_open = open(output_file, "w+")
f_open.write("#ifndef __CURRENT_TABLA_H__\n#define __CURRENT_TABLA_H__\n")

f_open.write("\nconst float current_table[] = {\n    ")
for i in range(len(I_ultima)):
    if i == len(I_ultima) - 1:
        f_open.write(str(I_ultima[i]))
        break
    f_open.write(str(I_ultima[i]) + ", ")
    if ((i + 1) % 10 == 0):
        f_open.write("\n    ")
f_open.write("\n};\n")

f_open.write("\nconst int R18_table[] = {\n    ")
for i in range(len(R18_ultima)):
    if i == len(R18_ultima) - 1:
        f_open.write(str(R18_ultima[i]))
        break
    f_open.write(str(R18_ultima[i]) + ", ")
    if ((i + 1) % 10 == 0):
        f_open.write("\n    ")
f_open.write("\n};\n")

f_open.write("\nconst int R19_table[] = {\n    ")
for i in range(len(R19_ultima)):
    if i == len(R19_ultima) - 1:
        f_open.write(str(R19_ultima[i]))
        break
    f_open.write(str(R19_ultima[i]) + ", ")
    if ((i + 1) % 10 == 0):
        f_open.write("\n    ")
f_open.write("\n};\n")

f_open.write("\n#endif\n")

f_open.close()