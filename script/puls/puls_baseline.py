"""Baseline Korrektur der Daten.

Ziehe von jedem Wert den durchschnittlichen Puls des Probanden ab.
"""
import pandas as pd

if __name__ == "__main__":
    fname = "puls_long.tsv"
    df = pd.read_csv(fname, sep="\t")
    probanden = df["prob_nr"].unique()
    run = df["run"].unique()
    
    for p in probanden:
        for r in run:
            rows = (df["prob_nr"] == p) & (df["run"] == r)
            cols = "puls"
            mean = df.loc[rows, cols].mean()
            print(f"Proband {p:02}: run{r:1}: Mittelwert {mean:6.2f}")
            df.loc[rows, cols] = df.loc[rows, cols] - mean
    df.to_csv("puls_long_runcorrect.tsv", sep="\t", float_format="%0.2f", index=False)

