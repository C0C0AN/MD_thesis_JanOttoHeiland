import matplotlib.pyplot as plt
import pandas as pd

lf = pd.read_csv("eda_long.tsv", sep="\t")

block2 = lf[lf.block == 1].drop(columns=["block"]).copy()
prob_ids = sorted(block2.prob_id.unique())
for p in prob_ids:
    rows = block2.prob_id == p
    block2.loc[rows, "time"] -= block2.loc[rows, "time"].min()

df = pd.pivot(block2, index="prob_id", columns=["time"])
df.T.plot()
plt.show()
