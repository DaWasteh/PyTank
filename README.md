# PyTank - Tank Battle Arena

Ein modernes 2D-Tank-Spiel mit verbessertem Audio-System, intelligenter KI und ansprechendem Design.

## 📋 Features

- **Hochwertige synthetisierte Sounds** (32/64 Bit Audio)
- **Intelligente Gegner-KI** mit State-Machine-System
- **Mehrere Spielmodi**: FFA, Horde und Co-op
- **Dynamische Level-Generation** mit thematischen Variationen
- **Verbessertes UI** mit animierten Elementen
- **Powerups-System** (Shield, Double Shot, Repair)
- **Wave-basiertes Gameplay** mit steigendem Schwierigkeitsgrad

## 🚀 Installation

### Voraussetzungen

- Python 3.10 oder neuer
- Pygame (`pip install pygame`)

### Installation

1. Klone das Repository:

   ```bash
   git clone https://github.com/dein-benutzername/pytank.git
   cd pytank


2. Installiere die Abhängigkeiten:

   ```bash
    pip install -r requirements.txt

3. Starte das Spiel:

   ```bash
    python pytank.py

🎮 Spielsteuerung
FFA Mode (2 Spieler)

    Spieler 1:
        Bewegung: WASD
        Schießen: Leertaste
    Spieler 2:
        Bewegung: Pfeiltasten
        Schießen: Enter

Horde Mode (Singleplayer)

    Bewegung: WASD
    Schießen: Leertaste

Allgemeine Steuerung

    Pause: ESC
    Vollbild: F
    Musik lauter/leiser: W/V
    SFX lauter/leiser: N/B
    Stummschaltung: M

🔧 Standalone EXE erstellen

Um eine ausführbare Windows-EXE zu erstellen, kannst du PyInstaller verwenden:

1. PyInstaller installieren

   ```bash

pip install pyinstaller

1. EXE erstellen

Führe folgenden Befehl im Projektverzeichnis aus:
bash

pyinstaller --onefile --windowed --icon=icon.ico pytank.py

Optionale Parameter:

    --add-data "data;data": Falls du zusätzliche Dateien hast (z.B. Sounds)
    --clean: Zwischendateien bereinigen
    --debug=all: Debug-Informationen anzeigen

3. EXE finden

Die erstellte EXE findest du im dist-Ordner.
Alternative: Auto PY to EXE

Eine benutzerfreundlichere Lösung ist das Tool "Auto PY to EXE":

    Installiere es:

   ```bash
    pip install auto-py-to-exe

    Führe es aus:
   ```bash
    auto-py-to-exe

    Wähle in der GUI:
        Script location: pytank.py
        Onefile: ✓
        Window based: ✓
        Icon file: (optional)
        Output directory: (wähle einen Ordner)

📁 Projektstruktur
text

pytank/
├── pytank.py          # Hauptspiel-Datei
├── README.md          # Diese Datei
├── requirements.txt   # Abhängigkeiten
├── dist/              # (Erstellt von PyInstaller) EXE-Datei
└── build/             # (Erstellt von PyInstaller) temporäre Dateien

🎯 Spielziele

    FFA Mode: Besiege alle Gegner und überlebe länger als dein Gegner
    Horde Mode: Überlebe 10 Wellen von Gegnern
    Co-op Mode: Arbeite mit einem Freund zusammen, um die Wellen zu besiegen

🏆 Highscores

Das Spiel speichert keine Highscores permanent. Die beste Punktzahl wird während einer Session angezeigt.
🐛 Fehler melden

Falls du einen Fehler findest oder eine Verbesserung vorschlagen möchtest, erstelle bitte ein Issue auf GitHub.
🤝 Mitwirken

Pull Requests sind willkommen! Bitte achte darauf:

    Fork das Projekt
    Erstelle einen neuen Branch (git checkout -b feature/neue-funktion)
    Commit deine Änderungen (git commit -am 'Neue Funktion hinzugefügt')
    Push auf den Branch (git push origin feature/neue-funktion)
    Erstelle einen Pull Request

📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die LICENSE-Datei für Details.
📞 Kontakt

Projekt-Link: https://github.com/DaWasteh/pytank
text


### Wichtige Hinweise zur EXE-Erstellung:

1. **Icon-Datei**: Erstelle eine `icon.ico`-Datei (z.B. mit einem Online-Converter) und legen sie im Projektverzeichnis ab.

2. **Abhängigkeiten**: Falls du zusätzliche Dateien hast (z.B. Sounddateien), musst du diese mit `--add-data` einbinden:
   ```bash
   pyinstaller --onefile --windowed --icon=icon.ico --add-data "sounds;." pytank.py

    Testen: Teste die erstellte EXE gründlich, da manchmal Pfadprobleme auftreten können.

    Größe reduzieren: Für eine kleinere EXE kannst du folgende Optionen verwenden:
   ```bash
    pyinstaller --onefile --windowed --icon=icon.ico --clean --upx-dir=upx-3.96-win64 pytank.py

    (Erfordert UPX: pip install upx)

    64-Bit vs 32-Bit: Verwende Python 64-Bit für die beste Kompatibilität mit modernen Systemen.

Diese README.md bietet eine vollständige Dokumentation für dein Spiel und enthält alle wichtigen Informationen für GitHub, inklusive der Anleitung zur EXE-Erstellung.
