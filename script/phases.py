"""
Analysiere die Phasen (wann wurde welcher Aufgabentyp geloest?).
Frage: ist dies bei jedem Probanden ungefaehr gleich?
"""
import pandas as pd
import numpy as np

from phases_fix import out_tsv as tsv_file


def phase_times_run(nr, run):
    """Finde die Start- und Endzeitpunkte der Phasen.

    - `run` sollte 0 oder 1 sein.
    """
    fn = tsv_file(nr, run)
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
    tf.trial_type = tf.trial_type.str.rstrip("_1")
    tf.trial_type = tf.trial_type.str.rstrip("_2")
    tf["repetition"] = [1] * 4 + [2] * 4
    tf.set_index(["repetition", "trial_type", "condition"], inplace=True)
    return tf


def phase_times(prob_nr):
    r1, r2 = (phase_times_run(prob_nr, i) for i in range(2))
    if r1 is None or r2 is None:
        return None
    r1["run"] = 1
    r2["run"] = 2
    both = pd.concat((r1, r2))
    idx = ["run", *both.index.names]
    both.reset_index(inplace=True)
    both.set_index(idx, inplace=True)
    return both


def load_all_phase_times():
    all_times = {i: phase_times(i) for i in range(2, 30)}
    assert all(t is not None for t in all_times.values())
    for i, t in all_times.items():
        t["prob_nr"] = i
    all_df = pd.concat([all_times[i] for i in range(2, 30)])
    idx = ["prob_nr", *all_df.index.names]
    all_df.reset_index(inplace=True)
    all_df.set_index(idx, inplace=True)
    return all_df


def find_max_deviation_times():
    from functools import reduce

    ptimes = {(n, e): phase_times_run(n, 0) for n in range(1, 30) for e in range(2)}
    ptimes = {k: v for k, v in ptimes.items() if v is not None}

    mi = reduce(np.minimum, ptimes.values())
    ma = reduce(np.maximum, ptimes.values())
    diff = ma.copy()
    diff[["start", "end"]] = ma[["start", "end"]] - mi[["start", "end"]]
    print("diff\n", diff)
    return diff


if __name__ == "__main__":
    all_df = load_all_phase_times()
    all_df.start = all_df.start.astype(float)
    all_df.end = all_df.end.astype(float)
    all_df.to_csv("phasen.tsv", sep="\t", float_format="%.3f")
