"""Lade Konfiguration, finde die Verzeichnisse der Daten."""
import toml
from os import path


config = toml.load(path.join(path.dirname(__file__), "config.toml"))
PREFIX = config["PREFIX"]
