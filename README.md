# IceRiver KS0 Monitoring Tool

![IceRiver KS0 Monitoring Tool](k1.jpg)

## Überblick

Das **IceRiver KS0 Monitor Script** wurde entwickelt, um mehrere KS0 Miner zu überwachen. Es ermöglicht die automatisierte Anmeldung an den Minern und das Abrufen sowie Speichern von Statusdaten für eine einfachere Verwaltung und Überwachung.

### Wichtige Neuerungen im `ks0-monitor-multiple4.py`:

Das Skript `ks0-monitor-multiple4.py`, das ursprünglich von [ccadic/IceRiverKS0Monitor](https://github.com/ccadic/IceRiverKS0Monitor) geforkt wurde, wurde erheblich optimiert und bietet nun folgende Verbesserungen:

1. **Automatische Verwaltung von `ChromeDriver`:**
   - Das Skript verwendet jetzt `webdriver_manager`, um die richtige Version von `ChromeDriver` basierend auf der installierten Chrome-Version automatisch herunterzuladen und zu konfigurieren. Dies verhindert Inkompatibilitätsprobleme zwischen `ChromeDriver` und Google Chrome.

2. **Verbesserte Stabilität und Kompatibilität:**
   - Zusätzliche Optionen für den Headless-Modus wurden hinzugefügt, um die Stabilität des Skripts in automatisierten Umgebungen zu verbessern.

3. **Flexiblere Fehlerbehandlung:**
   - Das Skript wurde mit besseren Fehlerbehandlungsmechanismen ausgestattet, um den Umgang mit unterschiedlichen Situationen, wie zum Beispiel verzögerte Ladezeiten, zu verbessern.

## Installation und Konfiguration

1. **Dateien entpacken:**
   - Sie müssen die Dateien `ks0-monitor.zip` und `ks0-monitor.z01` entpacken.

2. **Konfigurationsdatei anpassen:**
   - Aktualisieren Sie die Datei `ksaconfig.cfg`, um die IP-Adressen und Anmeldeinformationen (Benutzername/Passwort) für Ihre KS0 Miner zu reflektieren.

3. **Systemvoraussetzungen:**
   - Dieses Skript wurde als Python-kompiliertes Exe erstellt. Es ist ein Windows-System erforderlich (getestet auf Windows 10 und 11).

4. **Nutzungshinweise:**
   - Stellen Sie sicher, dass Sie Python und die erforderlichen Abhängigkeiten installiert haben, falls Sie das Skript direkt in Python ausführen.

## Unterstützung

Falls Ihnen dieses Tool hilft, freue ich mich über eine kleine Belohnung in Form von KASPA:

`kaspa:qqz3ss00rytt338csdep5h30r4dgn5hptnvwwk92a5wmf433zwlm7awpstuk7 :)`

Viel Spaß beim Überwachen Ihrer Miner!

![IceRiver KS0 Monitoring Tool](k2.jpg)
