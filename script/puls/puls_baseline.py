"""Baseline Korrektur der Daten.

Ziehe von jedem Wert den durchschnittlichen Puls des Probanden ab.
"""
import pandas as pd

if __name__ == "__main__":
    fname = "puls_long.tsv"
    df = pd.read_csv(fname, sep="\t")
    probanden = df["prob_nr"].unique()
    for p in probanden:
        # wähle alle Zeilen mit entsprechender `prob_nr` in der Spalte `puls`
        rows, cols = df["prob_nr"] == p, "puls"
        mean = df.loc[rows, cols].mean()
        print(f"Proband {p:02}: Mittelwert {mean:6.2f}")
        df.loc[rows, cols] = df.loc[rows, cols] - mean
    df.to_csv("puls_long_basecorrect.tsv", sep="\t", float_format="%0.2f", index=False)
