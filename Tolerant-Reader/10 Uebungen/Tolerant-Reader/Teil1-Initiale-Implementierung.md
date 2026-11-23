# Teil 1: Initiale Implementierung (Version 1)

## Ausgangslage

Dein Team entwickelt einen Service, der Personendaten aus einem zentralen Stammdaten-Service (Partner-Team) einliest und verarbeitet.

Das Partner-Team hat euch folgende Schnittstellenbeschreibung für **Version 1** zur Verfügung gestellt:

### Schnittstellen-Spezifikation (v1)

Die Schnittstelle liefert eine JSON-Liste von Personen-Objekten mit folgenden Feldern:

| Feldname | Typ | Pflichtfeld | Beschreibung |
| :--- | :--- | :--- | :--- |
| `id` | `String` | Ja | Eindeutige ID der Person (z.B. `"p-101"`) |
| `firstName` | `String` | Ja | Vorname |
| `lastName` | `String` | Ja | Nachname |
| `email` | `String` | Ja | E-Mail-Adresse |
| `address` | `String` | Ja | Komplette Postadresse als einzelner Text-String |

Ein Beispiel-Auszug liegt in der Datei [`data/persons-v1.json`](data/persons-v1.json) vor:

```json
[
  {
    "id": "p-101",
    "firstName": "Anna",
    "lastName": "Muster",
    "email": "anna.muster@example.ch",
    "address": "Bahnhofstrasse 12, 8001 Zürich"
  },
  {
    "id": "p-102",
    "firstName": "Luca",
    "lastName": "Bernasconi",
    "email": "luca.bernasconi@example.ch",
    "address": "Via Nassa 5, 6900 Lugano"
  }
]
```

---

## Deine Aufgabe (Schritt 1)

1. Öffne [`src/main/kotlin/ch/tbz/m321/PersonReader.kt`](src/main/kotlin/ch/tbz/m321/PersonReader.kt).
2. Erstelle eine `data class Person`, welche die oben beschriebene JSON-Struktur abbildet.
3. Implementiere die Methode `readAndFormatPersons(jsonFile: File): List<String>` mithilfe von **Jackson** (`mapper.readValue<List<Person>>(jsonFile)` aus dem Package `com.fasterxml.jackson.module.kotlin.readValue`).
4. Formatiere jede gelesene Person in **exakt folgender Struktur**, gib sie per `println(...)` auf der Konsole aus und gib die Liste der formatierten Strings als Rückgabewert zurück:

```text
[p-101] Anna Muster (anna.muster@example.ch) - Adresse: Bahnhofstrasse 12, 8001 Zürich
[p-102] Luca Bernasconi (luca.bernasconi@example.ch) - Adresse: Via Nassa 5, 6900 Lugano
```

---

### Erfolgskontrolle

Führe den bestehenden Unit-Test `Teil 1 - liest persons-v1 erfolgreich ein` in [`PersonReaderTest.kt`](src/test/kotlin/ch/tbz/m321/PersonReaderTest.kt) aus. Der Test muss **grün** sein!

👉 **Wenn der Unit-Test grün ist, gehe weiter zu [Teil 2: Der Breaking Change](Teil2-Breaking-Change.md).**
