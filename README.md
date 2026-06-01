# PyTank - Tank Battle Arena

PyTank ist ein modernes 2D-Tank-Spiel in Python/Pygame mit synthetischem Sound, State-Machine-KI, Powerups, dynamischen Maps und drei klar getrennten Spielarten: **Free For All**, **Horde** und **Missionen**.

## Features

- **Drei Spielmodi**: FFA, Horde und Missionen
- **Co-op als Add-on**: per Toggle für alle Modi aktivierbar, kein eigener Modus
- **KI-Schwierigkeiten**: Leicht, Mittel, Schwer und Mixed
- **Mixed-KI**: mehrere KI-Logiken gleichzeitig auf der Map
- **FFA-Teamsystem**: solo jeder gegen jeden, mit Co-op feste 2er-Teams bei gleicher Tankanzahl
- **Horde-Modus**: Wellen überleben, solo oder zu zweit
- **Missionen**: drei kurze Tutorial-/Quest-Maps mit Pythaner-vs.-Rusts-Comic-Story
- **Powerups**: Shield, Double Shot, Repair
- **Dynamische und handgebaute Maps** mit thematischen Varianten
- **Synthetisierte Sounds** ohne externe Audiodateien

## Spielmodi

### Free For All

- **Solo**: 1 Spieler + KI-Tanks, jeder gegen jeden.
- **Co-op**: 2 Spieler im selben Team; die KI wird ebenfalls in 2er-Teams verteilt.
- Die Gesamtanzahl der Tanks bleibt gleich.
- Ziel: Als letztes Team bzw. letzter Tank überleben.

### Horde

- Solo oder Co-op spielbar.
- Überlebe Gegnerwellen bis zur finalen Welle.
- Gegner spawnen wellenbasiert und werden mit späteren Wellen gefährlicher.

### Missionen

Drei kleine Tutorial-Quests mit eigenen Maps und Comic-Texten:

1. **Mission 1: Tor** - super leicht
2. **Mission 2: Rostpass** - leicht
3. **Mission 3: Ferrum-Brücke** - mittel

Story-Kurzfassung: Die Pythaner werden von den Rusts angegriffen. Der Kommandant schickt Pythy-Wan `Player 1` als letzte Hoffnung in drei Einsätze.

## Schwierigkeit

Für FFA und Horde wählbar:

- **Leicht**: langsamere, ungenauere KI
- **Mittel**: Standard-KI
- **Schwer**: aggressivere, schnellere und präzisere KI
- **Mixed**: jeder KI-Panzer bekommt zufällig bzw. verteilt eine Leicht-/Mittel-/Schwer-Variante

Missionen nutzen ihre eigene Story-Schwierigkeit.

## Steuerung

### Menü

| Aktion | Taste |
| --- | --- |
| Modus/Map wählen | Pfeile oder WASD |
| Bestätigen / Starten | Enter oder Leertaste |
| Co-op umschalten | C |
| Schwierigkeit wechseln | D |
| Zurück | ESC / Backspace |
| Vollbild | F |

### Spieler 1

| Aktion | Taste |
| --- | --- |
| Bewegung | WASD |
| Schießen | Leertaste |

### Spieler 2 / Co-op

| Aktion | Taste |
| --- | --- |
| Bewegung | Pfeiltasten |
| Schießen | Enter |

### Im Spiel

| Aktion | Taste |
| --- | --- |
| Pause | ESC oder P |
| Musik leiser/lauter | V / C |
| SFX leiser/lauter | B / N |
| Mute | M |
| Vollbild | F |

## Installation

### Voraussetzungen

- Python **3.10 bis 3.12** empfohlen
- Pygame aus `requirements.txt`

> Hinweis: Für dieses Projekt wird lokal Python 3.12 verwendet. Python 3.14 ist aktuell für Pygame/CI nicht empfohlen.

### Setup

```bash
git clone https://github.com/DaWasteh/pytank.git
cd pytank
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Starten

```bash
python pytank.py
```

Oder direkt ohne aktivierte Umgebung:

```bash
.venv\Scripts\python.exe pytank.py
```

## Tests und Checks

```bash
python -m py_compile pytank.py
python -m flake8 pytank.py tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
python -m flake8 pytank.py tests/ --count --statistics --max-line-length=120
python tests/test_start.py
python tests/test_sound.py
python tests/test_exe.py
```

In Headless-Umgebungen können SDL-Dummy-Treiber genutzt werden:

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python tests/test_start.py
```

## Standalone-EXE erstellen

PyInstaller installieren:

```bash
pip install pyinstaller
```

EXE bauen:

```bash
pyinstaller --onefile --windowed pytank.py
```

Die fertige Datei liegt danach in `dist/`.

Optional mit Icon:

```bash
pyinstaller --onefile --windowed --icon=icon.ico pytank.py
```

## Projektstruktur

```text
pytank/
├── pytank.py              # Hauptspiel-Datei
├── README.md              # Dokumentation
├── requirements.txt       # Python-Abhängigkeiten
├── tests/                 # Start-/Sound-/EXE-Tests
├── .github/workflows/     # GitHub Actions CI
├── dist/                  # Lokale Build-Ausgaben
└── build/                 # Temporäre PyInstaller-Dateien
```

## GitHub Actions

Der CI-Workflow lintet und testet das Projekt unter unterstützten Python-Versionen. Für Pygame werden Dummy-SDL-Treiber bzw. Headless-kompatible Einstellungen verwendet.

## Lizenz

Siehe Repository-Lizenzdatei.
