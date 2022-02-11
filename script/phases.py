"""
Analysiere die Phasen (wann wurde welcher Aufgabentyp geloest?).
Frage: ist dies bei jedem Probanden ungefaehr gleich?
"""
import pandas as pd
import numpy as np

from phases_fix import out_tsv as tsv_file


def phase_times(nr, exp):
    """Finde die Start- und Endzeitpunkte der Phasen."""
    fn = tsv_file(nr, exp)
    if fn is None:
        return None
    df = pd.read_csv(fn, sep="\t")
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


if __name__ == "__main__":
    from functools import reduce

    ptimes = {(n, e): phase_times(n, 0) for n in range(1, 30) for e in range(2)}
    ptimes = {k: v for k, v in ptimes.items() if v is not None}

    mi = reduce(np.minimum, ptimes.values())
    ma = reduce(np.maximum, ptimes.values())
    diff = ma.copy()
    diff[["start", "end"]] = (ma[["start", "end"]] - mi[["start", "end"]])
    print("diff\n", diff)
