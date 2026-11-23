# Teil 2: Der Breaking Change & Architektur-Überlegung

## Szenario

Einige Wochen später beschliesst das Partner-Team des Stammdaten-Services, dass eine Adresse als einzelner String (`"Bahnhofstrasse 12, 8001 Zürich"`) unpraktisch ist, weil man nicht sauber nach Postleitzahl oder Ort filtern kann.

Sie passen ihren Service an und spielen ein Update ein. Ab sofort liefert die Schnittstelle die Daten wie in [`data/persons-v2-breaking.json`](data/persons-v2-breaking.json):

```json
[
  {
    "id": "p-101",
    "firstName": "Anna",
    "lastName": "Muster",
    "email": "anna.muster@example.ch",
    "address": {
      "street": "Bahnhofstrasse 12",
      "zipCode": "8001",
      "city": "Zürich"
    }
  }
]
```

---

## Deine Aufgabe (Schritt 2)

### 2.1 Unit-Test mit dem neuen JSON ausführen

Ergänze in [`PersonReaderTest.kt`](src/test/kotlin/ch/tbz/m321/PersonReaderTest.kt) einen zweiten Unit-Test, der `File("data/persons-v2-breaking.json")` an `reader.readAndFormatPersons(...)` übergibt, **ohne deinen Code in `PersonReader.kt` anzupassen**, und führe den Test aus.

**Beobachtung:**
- Was passiert beim Ausführen des Tests?
- Welche Exception wirft Jackson konkret und warum?
- *(Tipp: Du kannst den Test danach mit `assertFailsWith<MismatchedInputException> { ... }` aus `com.fasterxml.jackson.databind.exc.MismatchedInputException` dokumentieren, damit deine Test-Suite später wieder grün bleibt.)*

---

### 2.2 Überlegung: Rückwärtskompatibles Design

Dein Consumer ist beim Einlesen abgestürzt! In einer echten Produktionsumgebung mit vielen Consumern können nicht alle Services exakt in derselben Millisekunde aktualisiert werden.

**Denkaufgabe (bevor du Teil 3 öffnest!):**
1. **Auf Producer-Seite (JSON-Format):** Wie hätte das Partner-Team das JSON gestalten müssen, damit die neue strukturierte Adresse eingeführt werden kann, **ohne** dass bestehende Consumer (wie dein aktueller `PersonReader` aus Teil 1) abstürzen oder falsche Daten anzeigen? Skizziere ein passendes JSON.
2. **Auf Consumer-Seite (Dein Jackson-Code):** Selbst wenn das Partner-Team das JSON rückwärtskompatibel erweitert – würde dein aktueller `PersonReader` aus Teil 1 (mit Standard-Jackson-2-Konfiguration) damit sofort klarkommen, oder wirft Jackson standardmässig immer noch einen Fehler? Warum?

Notiere dir deine Überlegungen kurz.

👉 **Wenn du dir Gedanken gemacht hast, gehe weiter zu [Teil 3: Tolerant Reader & Schrittweise Migration](Teil3-Tolerant-Reader-Migration.md).**
