# Übung: Tolerant Reader Pattern & API-Evolution

In verteilten Systemen (Microservices, Schnittstellen zwischen Teams) ändern sich Datenformate im Laufe der Zeit. Wenn ein Service (Producer) seine Schnittstelle anpasst, darf dies im Idealfall nicht dazu führen, dass alle aufrufenden Systeme (Consumer) sofort abstürzen.

Das **Tolerant Reader Pattern** (nach Martin Fowler / Postel's Law: *"Be conservative in what you do, be liberal in what you accept from others"*) hilft dabei, Consumer so robust zu bauen, dass Schnittstellen ohne Ausfallzeiten weiterentwickelt werden können.

---

## Lernziele

1. Du erfährst anhand von Unit-Tests am eigenen Code, wie ein **Breaking Change** in einer JSON-Schnittstelle einen strikten Consumer zum Absturz bringt.
2. Du überlegst dir, wie Änderungen an Schnittstellen nach dem **Expand-and-Contract Pattern** (Parallel Change) rückwärtskompatibel gestaltet werden können.
3. Du implementierst einen **Tolerant Reader** mit **Kotlin**, **Gradle** und **Jackson 2**, der sowohl mit neuen, unbekannten Feldern als auch mit schrittweisen Migrationen von alten zu neuen Datenstrukturen umgehen kann.
4. Im Bonus-Teil untersuchst du, was sich diesbezüglich mit **Jackson 3** und anderen Technologien geändert hat.

---

## Projektstruktur & Setup

Öffne diesen Ordner als **Gradle-Projekt** in deiner IDE (z.B. IntelliJ IDEA):

- [`build.gradle.kts`](build.gradle.kts) – Gradle-Konfiguration mit Kotlin und `com.fasterxml.jackson.module:jackson-module-kotlin` (Jackson 2)
- [`src/main/kotlin/ch/tbz/m321/PersonReader.kt`](src/main/kotlin/ch/tbz/m321/PersonReader.kt) – Hier implementierst du deinen JSON-Reader
- [`src/test/kotlin/ch/tbz/m321/PersonReaderTest.kt`](src/test/kotlin/ch/tbz/m321/PersonReaderTest.kt) – Hier überprüfst du deinen Reader Schritt für Schritt mit Unit-Tests
- [`data/`](data/) – Enthält die JSON-Dateien für die verschiedenen Evolutionsstufen der Schnittstelle

---

## Tests starten (Windows / VS Code)

Voraussetzung: JDK 21 (mit `java -version` pruefen). Gradle wird automatisch ueber den Wrapper geladen; beim ersten Start wird Internet benoetigt.

In VS Code die Datei `../../Tolerant-Reader.code-workspace` oeffnen. Anschliessend **Terminal > Run Task... > Tolerant Reader: Tests** auswaehlen.

Alternativ im Terminal in diesem Ordner (`10 Uebungen/Tolerant-Reader`) ausfuehren:

```powershell
.\gradlew.bat test
```

Nur die geoeffnete Testklasse erneut ausfuehren:

```powershell
.\gradlew.bat test --tests "ch.tbz.m321.PersonReaderTest" --rerun-tasks
```

Den Testbericht findest du danach unter `build/reports/tests/test/index.html`.
`PersonReader.kt` ist eine Bibliotheksklasse ohne `main`-Methode; sie wird ueber `PersonReaderTest.kt` ausgefuehrt. Teil 1 ist implementiert, die weiteren Uebungsschritte bleiben offen.

---

## Ablauf der Übung

> **Wichtig:** Bearbeite die Schritte **nacheinander**. Öffne das nächste Dokument erst, wenn du den aktuellen Schritt abgeschlossen hast!

1. **[Teil 1: Initiale Implementierung (Version 1)](Teil1-Initiale-Implementierung.md)**
   Consumer für die erste Version der Personendaten-Schnittstelle schreiben und den ersten Unit-Test auf Grün bringen.
2. **[Teil 2: Der Breaking Change & Architektur-Überlegung](Teil2-Breaking-Change.md)**
   Was passiert im Unit-Test, wenn das Nachbarsystem die Adresse plötzlich strukturiert liefert?
3. **[Teil 3: Tolerant Reader & Schrittweise Migration](Teil3-Tolerant-Reader-Migration.md)**
   Den Consumer fehlertolerant machen und schrittweise auf das neue Format migrieren.
4. **[Teil 4: Aufräumen (Contract) & Bonus: Jackson 3 / Andere Sprachen](Teil4-Abschluss-und-Bonus.md)**
   Abschluss der Migration (`v3`), Upgrade auf Jackson 3 und Vergleich mit anderen Technologien.
