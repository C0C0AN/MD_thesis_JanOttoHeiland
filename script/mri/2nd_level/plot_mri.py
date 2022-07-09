#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 12:38:41 2022

@author: jan
"""

import matplotlib.pyplot as plt
import pandas as pd

data = {'superior parietaler Gyrus (P1)': [0.603, 0.5],
        'middle occipital lobe (O2) [left]': [0.361, 0.357],
        'Thalamus': [0.195, 0.186],
        'middle occipital lobe [right]': [0.543, 0.49],
        'middle frontal gyrus': [0.299, 0.21]
        }

data_relax = {'Gyrus praecentralis' :[0.322,0.349],
              'middle occipital lobe (O2) [left]': [0.28,0.409], 
              'middle occipital lobe (O2) [right]':[0.358, 0.489],
              'Gyrus parietalis inferior': [0.357, 0.434]}

df = pd.DataFrame(data, index=['run1','run2'])
df_relax = pd.DataFrame(data_relax, index=['run1','run2'])



plt.plot(df,"o-", label=df.columns)
plt.legend(loc='upper right')
plt.ylabel('beta value')
plt.show()
plt.savefig("runvsrun_stress.png")


plt.plot(df_relax,"o-", label=df_relax.columns)
plt.legend(loc='upper left')
plt.ylabel('beta value')
plt.show()
plt.savefig("runvsrun_relax.png")



data1 = {'T3  ': [0.202, 0.171],
        'AG': [0.271, 0.200],
        'RO ': [0.194, 0.107],
        'PCL ': [0.197, 0.103],
        'MCIN': [0.301, 0.221],
        'FR ': [0.223, 0.270]
        }


df1 = pd.DataFrame(data1, index=['run1','run2'])

plt.plot(df1,"o-", label=df1.columns)
plt.legend(loc='lower left')
plt.ylabel('beta value')
plt.show()
plt.savefig("runvsrun_stress_neu.png")

data_stress = {'LING left' :[0.091, 0.241],
              'Thalamus': [0.225, 0.250], 
              'ACIN':[0.097, 0.253],
              'F3T left': [0.193, 0.187],
              'T3 left':[0.106, 0.166],
              'LING right':[0.17, 0.251],
              'F3T right':[0.162, 0.169],
              'T2 right':[0.234, 0.156],              
              }


df2 = pd.DataFrame(data_stress, index=['run1','run2'])

plt.plot(df2,"o-", label=df2.columns)
plt.legend(loc=('lower right'), ncol = 2)
plt.ylabel('beta value')
plt.show()
plt.savefig("runvsrun_relax_neu.png")