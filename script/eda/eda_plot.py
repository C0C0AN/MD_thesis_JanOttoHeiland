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
df = df.loc[df.index[:29]]
plt.figure()
((df.T - df.mean(axis=1)) / df.std(axis=1)).plot()
plt.show()

# Definiere Phasen der Stressblöcke 
phases = [
    (6.53, 64.87),
    (94.43, 153.55),
    (182.38, 242),
    (270.34, 329.78),
    (358.33, 416.69),
    (446.23, 505.03),
    (534.17, 593.74),
    (622.14, 681.77)
    
]
#Methode zum Zugriff auf die Stress und Entspannungsphasen des Experiments
def plot_phases(colors=['0.3', '0.9'], alpha=0.06):
    for i, phase in enumerate(phases):
        plt.axvspan(phase[0], phase[1], facecolor=colors[i % 2], alpha=alpha)

df1=df.T - df.mean(axis=1)
plot_phases(colors=["green", "green"], alpha=0.05)
ax = (df.T - df.mean(axis=1)).plot(legend=False, alpha=0.1,ax=plt.gca(), color="blue") 
df1.mean(axis=1).plot(title = "EDA run-1", legend=True, label= "mean eda", linewidth=2, color="blue", ax=ax, xlabel = "time(s)", ylabel="eda(S)")
plt.show()
