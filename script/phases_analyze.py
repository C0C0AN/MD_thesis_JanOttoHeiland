"""Analysiere die Start- und Endzeitpunkte der Phasen."""
import pandas as pd

from collect import load_phasen

if __name__ == "__main__":
    runs = load_phasen("phasen.tsv", means=True)
    r1, r2 = runs.loc[1], runs.loc[2]
    print(
        "maximale Abweichung zwischen den Runs",
        abs(r1.values - r2.values).round(3).max(),
    )
    runs.round(3).to_html("phasen_zeiten.html")
