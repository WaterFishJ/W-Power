# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

matplotlib.rc("font",family='KaiTi')

R_high = 10000
R1_level = 256
R1_Value = 10000
R2_level = 256
R2_Value = 10000
R_low = 0
Rw = 50

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


x = []
y = []
r1_list = []
r2_list = []
x_index = 0
y_index = 0
for i in R1:
    y_index = 0
    for j in R2:
        if (20000 <= (R_low + i + j + R_high) <= 30000):
            x.append(x_index)
            y.append(y_index)
            r1_list.append(i)
            r2_list.append(j)
        y_index += 1
    x_index += 1

plt.figure()
plt.xlabel('R1 level', fontsize = 15, color = 'r')
plt.ylabel('R2 level', fontsize = 15, color = 'r')
plt.scatter(x, y, marker='.', s = 1)
plt.xlim((0,R1_level))
plt.ylim((0,R2_level))

Uv = []
x_index = 0
count = 0
for i in range(len(r1_list)):
    count += 1
    U = round((1.2 * (1 + (r1_list[i] + R_high) / (r2_list[i] + R_low))), 2)
    if (U <= 28):
        if (any(np.isin(Uv, U)) == False):
            x_index += 1
            Uv.append(U)
Uv.sort()
print(len(Uv))
I_leval = np.linspace(0.0, 1.0, x_index)

plt.figure()
plt.xlabel('U_leval', fontsize = 15, color = 'r')
plt.ylabel('Uv', fontsize = 15, color = 'r')
plt.scatter(I_leval, Uv, marker='.', s = 1)
plt.xlim((0,1))
plt.ylim((0,28))

plt.figure()
plt.hist(Uv, 15)
plt.xlabel('U_leval', fontsize = 15, color = 'r')
plt.ylabel('Uv', fontsize = 15, color = 'r')

plt.figure()
pdIa = pd.Series(Uv)
pdIa.plot(kind = 'hist', bins = 15, edgecolor = 'black', density = True, label = '分布直方图')
pdIa.plot(kind = 'kde', color = 'red', label = '密度')
plt.legend()
plt.show()

                
            
