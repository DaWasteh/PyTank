import subprocess
import sys
import time

print("Starte PyTank.exe...")
start_time = time.time()

try:
    # exe ausführen
    result = subprocess.run(
        ["dist\\PyTank.exe"],
        timeout=10,
        capture_output=True,
        text=True
    )
    elapsed = time.time() - start_time

    print(f"Exit Code: {result.returncode}")
    print(f"Laufzeit: {elapsed:.2f}s")

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.stdout:
        print("STDOUT:")
        print(result.stdout)

    if result.returncode == 0:
        print("SUCCESS: exe hat normal beendet")
    else:
        print(f"FAILURE: exe mit Exit Code {result.returncode} beendet")

except subprocess.TimeoutExpired:
    print("TIMEOUT: exe läuft noch nach 10 Sekunden")
except Exception as e:
    print(f"Fehler: {e}")
    sys.exit(1)
