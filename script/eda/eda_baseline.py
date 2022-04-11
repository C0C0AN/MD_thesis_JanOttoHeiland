"""Ziehe den Mittelwert pro Proband ab in den EDA Daten."""
import pandas as pd


def baseline_correction(df, column):
    probanden = df["prob_id"].unique()
    for i in probanden:
        mask = df["prob_id"] == i
        df.loc[mask, column] -= df.loc[mask, column].mean()
    df = df.astype({"age": int})
    return df


if __name__ == "__main__":
    df = pd.read_csv("eda_complete.tsv", sep="\t")
    if "index" in df.columns:
        df.drop(columns=["index"], inplace=True)
    df = baseline_correction(df, "eda")
    df.to_csv("eda_complete_baseline.tsv", sep="\t", index=False, float_format="%6.3f")
