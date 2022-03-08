import matplotlib.pyplot as plt
import pandas as pd

lf = pd.read_csv("eda_long.tsv", sep="\t")

block2 = lf[lf.block == 1].drop(columns=["block"]).copy()
block2 = block2.reset_index().drop(columns=["index"])
prob_ids = sorted(block2.prob_id.unique())
for p in prob_ids:
    rows = block2.prob_id == p
    block2.loc[rows, "time"] -= block2.loc[rows, "time"].min()

df = pd.pivot(block2, index="prob_id", columns=["time"], values="eda")
df_complete = df

(df.T - df.mean(axis=1)).plot()
df = df.loc[df.index[:5]]
plt.figure()
((df.T - df.mean(axis=1)) / df.std(axis=1)).plot()
plt.show()
