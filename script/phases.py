"""
Analysiere die Phasen (wann wurde welcher Aufgabentyp geloest?).
Frage: ist dies bei jedem Probanden ungefaehr gleich?
"""
import pandas as pd
from itertools import groupby

from phases_fix import out_tsv as tsv_file


def phase_times(nr, exp):
    """Finde die Start- und Endzeitpunkte der Phasen."""
    df = pd.read_csv(tsv_file(nr, exp), sep="\t")
    df = df[["onset", "duration", "trial_type", "condition"]]
    mask = df.trial_type.str.startswith("stress")
    mask |= df.trial_type.str.startswith("relax")
    mask &= ~df.trial_type.str.endswith("gremium")
    df = df[mask]
    groups = (df.condition != df.condition.shift()).cumsum()
    tf = pd.DataFrame(
        data={
            g: {
                "start": float(t.onset.iloc[0]),
                "end": float(t.onset.iloc[-1] + t.duration.iloc[-1]),
                "trial_type": t.trial_type.iloc[0],
                "condition": t.condition.iloc[0],
            }
            for g, t in df.groupby(groups)
        }
    )
    tf = tf.T
    tf = tf.reindex(columns=["start", "end", "trial_type", "condition"])
    return tf
