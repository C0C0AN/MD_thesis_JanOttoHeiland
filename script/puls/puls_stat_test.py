import scipy.stats
import pandas as pd


df = pd.read_csv("musik_vs_sound_under_relex.tsv", sep="\t")
print("mean\n", df.groupby("trial").mean())
print("std\n", df.groupby("trial").std())


a = df[df.trial == "Musik"]["puls"]
b = df[df.trial == "Sound"]["puls"]

print(scipy.stats.ttest_ind(a, b))

