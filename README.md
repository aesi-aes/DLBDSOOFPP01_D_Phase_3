# Course Dashboard

Ein Desktop-Dashboard zur Verwaltung eines Studienverlaufs.
Das Programm wurde mit **Python** und **Tkinter** entwickelt.

Das Dashboard ermöglicht unter anderem:

* Verwaltung von Semestern und Modulen
* Verwaltung von Prüfungsergebnissen
* Berechnung des aktuellen Notendurchschnitts
* Festlegung eines Ziel-Notendurchschnitts
* Anzeige des Studienfortschritts
* Speichern und Laden der Daten als JSON-Datei
* Demo-Modus ohne Speichern und Laden (Testdaten werden automatisch geladen)

## Repository

Der vollständige Quellcode befindet sich auf GitHub:

**https://github.com/aesi-aes/DLBDSOOFPP01_D_Phase_3**

---

## Voraussetzungen

* Windows 10 oder Windows 11
* Python 3.10 oder neuer
* Git (optional, falls das Repository als ZIP heruntergeladen wird)

Das Programm verwendet ausschließlich Python-Standardbibliotheken. Es müssen daher keine zusätzlichen Python-Pakete installiert werden.

---

## Installation unter Windows

### 1. Repository herunterladen

Repository über Git in einen <Zielordner> klonen:

```powershell
git clone https://github.com/aesi-aes/DLBDSOOFPP01_D_Phase_3.git
```

Anschließend in den Projektordner wechseln:

```powershell
cd <Zielordner>\DLBDSOOFPP01_D_Phase_3\Phase3
```

Alternativ kann das Repository auf GitHub über **Code → Download ZIP** heruntergeladen und anschließend entpackt werden.

### 2. Python überprüfen

In PowerShell oder der Eingabeaufforderung:

```powershell
python --version
```

Es sollte Python 3.10 oder neuer angezeigt werden.

### 3. Programm starten

Im Projektordner unter \DLBDSOOFPP01_D_Phase_3\Phase3:

```powershell
python main.py
```

Das Dashboard sollte sich anschließend als Desktop-Anwendung öffnen.

---

## Erster Start

Beim ersten Start existiert möglicherweise noch keine `dashboard.json`.

In diesem Fall wird automatisch ein **leeres Studienprogramm** angelegt.

Beim Beenden des Programms werden die aktuellen Daten automatisch in

```text
dashboard.json
```

gespeichert.

Beim nächsten Start werden diese Daten wieder geladen.

Die Datei `dashboard.json` wird automatisch erzeugt und muss nicht manuell angelegt werden.

---

## Demo-Modus

Für eine schnelle Demonstration kann das Programm mit vorbereiteten Beispieldaten gestartet werden:

```powershell
python main.py --demo
```

Der Demo-Modus enthält beispielhafte Semester, Module und Prüfungsergebnisse.

Die Demo-Daten werden **nicht in `dashboard.json` gespeichert**, sodass vorhandene eigene Daten nicht überschrieben werden.

---

## Bedienung

### Semester

Über die Semesterverwaltung können:

* neue Semester angelegt werden
* Semester gelöscht werden
* das aktuelle Semester festgelegt werden

Das aktuelle Semester wird im Modulbaum hervorgehoben.

### Module

Für ein ausgewähltes Semester können Module:

* hinzugefügt
* gelöscht
* bearbeitet

werden.

### Prüfungsergebnisse

Für ein ausgewähltes Modul können Prüfungsergebnisse:

* hinzugefügt
* bearbeitet
* gelöscht

werden.

Eine Prüfung kann zunächst auch ohne eingetragene Note gespeichert werden. In diesem Fall wird sie als **„Noch nicht geprüft“** angezeigt.

### Notendurchschnitt

Der aktuelle Notendurchschnitt wird automatisch aus den vorhandenen benoteten Prüfungsergebnissen berechnet.

Prüfungsergebnisse ohne Note werden dabei nicht berücksichtigt.

Zusätzlich kann ein persönlicher Ziel-Notendurchschnitt festgelegt werden. Das Dashboard zeigt anschließend an, ob dieses Ziel erreicht wurde.

### Studienfortschritt

Der Studienfortschritt wird anhand der abgeschlossenen Module berechnet.

Ein Modul gilt als abgeschlossen, wenn alle vorhandenen Prüfungsergebnisse bestanden wurden.

---

## Projektstruktur

Die Anwendung verwendet eine einfache Trennung in **Model**, **Service**, **Controller** und **GUI**:

* **Models** enthalten die Daten und deren grundlegende Eigenschaften.
* **Services** enthalten die Fachlogik, z. B. Berechnung von Notendurchschnitt und Studienfortschritt.
* **Controller** verbinden GUI und Services.
* **GUI** enthält die Benutzeroberfläche.
* **JsonDataStore** übernimmt das Speichern und Laden der Daten.
* **Application** initialisiert die einzelnen Komponenten.
* **main.py** ist der Einstiegspunkt des Programms.

---

## Technische Hinweise

Das Programm benötigt keine externe Datenbank.

Die persistenten Daten werden in einer JSON-Datei gespeichert:

```text
dashboard.json
```

Abgeleitete Werte wie Studienfortschritt, Notendurchschnitt und der Status eines Moduls werden nicht gespeichert, sondern bei Bedarf aus den vorhandenen Daten berechnet.

## Autor

Sebastian Denzer
