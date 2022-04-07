"""Ziehe den Mittelwert pro Proband ab in den EDA Daten."""
import pandas as pd

df = pd.read_csv("eda_complete.tsv", sep="\t")
probanden = df["prob_id"].unique()
for i in probanden:
    mask = df["prob_id"] == i
    df.loc[mask, "eda"] -= df.loc[mask, "eda"].mean()

df.drop(columns=["index"], inplace=True)
df = df.astype({"age": int})
df.to_csv("eda_complete_baseline.tsv", sep="\t", index=False, float_format="%6.3f")
