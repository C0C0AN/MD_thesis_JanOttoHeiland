# coding: utf-8
"""Find the Response blocks."""
import warnings
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from resp import find_vhdrs, load_vhdr

RESPONSE = "Response/R128"
BLOCKS_CSV = path.join(path.dirname(path.realpath(__file__)), "blocks.csv")


def plot_block_hist(ann):
    """
    mask: array wann eine Response Antwort vorhanden ist.
    """
    mask = ann.description == RESPONSE
    response_times = ann.onset[mask]
    plt.hist(response_times, cumulative=True, bins=200)


def find_blocks(ann, delta=1.5):
    """
    hier wird definiert nach welchen Kriterien die Anfangs und Endzeiten der
    Blöcke gefunden werden
    s0 wann kommt die erste und t_last wann die letze Response Antwort,
    ausgehend davon wird untersucht wann die Response Antwort nicht mehr vorhanden ist
    delta: in welchem Zeitintervall wird nach den REponse Antworten gesucht
    """
    mask = ann.description == RESPONSE
    s0 = np.argmax(mask)
    t_last = len(ann) - np.argmax(np.flipud(mask)) - 1

    response_times = ann.onset[mask]
    crit = np.where(np.diff(response_times) > delta)[0]
    times = [s0]
    for c in crit:
        times.append(np.where(mask)[0][c + 0])
        times.append(np.where(mask)[0][c + 1])
    times.append(t_last)
    return times


def get_blocktimes(fname, delta=1.5, show_raw=False, filter=False):
    """
    Methode um eine Liste der End und Startpunkte der Bloecke zu generieren.

    filter: Sollen die gefundenen Blöcke gefiltert werden auf mehr als 3?
    """
    data, times, raw = load_vhdr(fname, verbose=False)
    ann = raw.annotations
    blocks = find_blocks(ann, delta=delta)
    blocks = list(ann.onset[blocks])
    if filter:
        if len(blocks) < 6:
            return None
        elif len(blocks) > 6:
            # Finde den Block, mit der kürzesten Länge, d.h. kürzesten Differenz
            min_block_idx = np.argmin(np.diff(blocks)[::2])
            del blocks[2 * min_block_idx]
            del blocks[2 * min_block_idx]
        if len(blocks) != 6:
            warnings.warn("length != 6 in " + fname)

    print(",".join([path.basename(fname)] + map(str, blocks)))

    if show_raw:
        raw.plot()
        plt.show()

    if False:
        plot_block_hist(ann)
        plt.show()

    return blocks


def load_blocks(csv_file=BLOCKS_CSV):
    """
    Lade Informationen über Blocklängen in DataFrame.
    """
    return pd.read_csv(csv_file, index_col=0, header=None)


"""
Hauptmethode die mir eine Liste von allen Blockzeiten von allen Probanden erstellt
"""
if __name__ == "__main__":
    process_all = True

    if process_all:
        for fname in find_vhdrs("../../Daten/BekJan/"):
            b = get_blocktimes(fname, filter=True)
    else:
        get_blocktimes("../../Daten/BekJan/HOAF_13.vhdr", show_raw=False, filter=True)
