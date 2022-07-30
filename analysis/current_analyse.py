# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

matplotlib.rc("font",family='KaiTi')

R_low = 000
R18_level = 256
R18_Value = 50000
R19_level = 256
R19_Value = 100000
R_high = 50000
Rw = 50

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


x = []
y = []
r18_list = []
r19_list = []
x_index = 0
y_index = 0
for i in R18:
    y_index = 0
    for j in R19:
        if (60000 <= (R_low + i + j + R_high) <= 80000):
            x.append(x_index)
            y.append(y_index)
            r18_list.append(i)
            r19_list.append(j)
        y_index += 1
    x_index += 1

plt.figure()
plt.xlabel('R18 level', fontsize = 15, color = 'r')
plt.ylabel('R19 level', fontsize = 15, color = 'r')
plt.scatter(x, y, marker='.', s = 1)
plt.xlim((0,R18_level))
plt.ylim((0,R19_level))

Ia = []
x_index = 0
count = 0
for i in range(len(r18_list)):
    count += 1
    I = round((480 * (r18_list[i] + R_low))/(7 * (r18_list[i] + R_low + r19_list[i] + R_high)), 2)
    if (I <= 15):
        if (any(np.isin(Ia, I)) == False):
            x_index += 1
            Ia.append(I)
            # print(I, "R18:", (int)((r18_list[i] - Rw) / (R18_Value / 256)), "R19:", (int)((r19_list[i] - Rw) / (R19_Value / 256)))
Ia.sort()
print(len(Ia))
I_leval = np.linspace(0.0, 1.0, x_index)

plt.figure()
plt.xlabel('I_leval', fontsize = 15, color = 'r')
plt.ylabel('Ia', fontsize = 15, color = 'r')
plt.scatter(I_leval, Ia, marker='.', s = 1)
plt.xlim((0,1))
plt.ylim((0,15))

plt.figure()
plt.hist(Ia, 15)
plt.xlabel('I_leval', fontsize = 15, color = 'r')
plt.ylabel('Ia', fontsize = 15, color = 'r')

plt.figure()
pdIa = pd.Series(Ia)
pdIa.plot(kind = 'hist', bins = 15, edgecolor = 'black', density = True, label = '分布直方图')
pdIa.plot(kind = 'kde', color = 'red', label = '密度')
plt.legend()
plt.show()

                
            
