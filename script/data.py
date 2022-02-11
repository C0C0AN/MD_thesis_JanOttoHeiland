"""Lade Konfiguration, finde die Verzeichnisse der Daten."""
import toml
from os import path


config = toml.load(path.join(path.dirname(path.realpath(__file__)), "config.toml"))
PREFIX = config["PREFIX"]
HOAF_DIR = path.join(PREFIX, "HOAF")
HOAF_BIDS = path.join(HOAF, "HOAF_BIDS")
