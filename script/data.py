"""Lade Konfiguration, finde die Verzeichnisse der Daten."""
import toml
from os import path


config_dir = path.dirname(path.realpath(__file__))
config_toml = path.join(config_dir, "config.toml")
if not path.exists(config_toml):
    # Wenn keine Konfiguration `config.toml` erstellt wurde, nehme die Beispielkonfiguration
    config_toml = path.join(config_dir, "config.example.toml")
config = toml.load(config_toml)

PREFIX = config["PREFIX"]
if not path.isabs(PREFIX):
    # Bei einem relativen Pfad: füge das Konfigurationsverzeichnis vorne dran
    PREFIX = path.join(config_dir, PREFIX)
HOAF_DIR = path.join(PREFIX, "HOAF")
HOAF_BIDS = path.join(HOAF_DIR, "HOAF_BIDS")
DATEN_DIR = config["DATEN"]
