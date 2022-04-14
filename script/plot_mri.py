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

