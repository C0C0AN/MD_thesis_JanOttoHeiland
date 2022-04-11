"""Ziehe den Mittelwert pro Proband ab in den EDA Daten."""
import pandas as pd

from collect import baseline_correction

if __name__ == "__main__":
    df = pd.read_csv("eda_complete.tsv", sep="\t")
    if "index" in df.columns:
        df.drop(columns=["index"], inplace=True)
    df = baseline_correction(df, "eda")
    df.to_csv("eda_complete_baseline.tsv", sep="\t", index=False, float_format="%6.3f")
