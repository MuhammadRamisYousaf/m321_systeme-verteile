# Teil 4: Aufräumen (Contract) & Bonus-Aufgaben

## Schritt 4: Das alte Feld fällt weg (`v3`)

Nachdem alle Consumer erfolgreich auf `addressDetails` umgestellt haben, führt das Partner-Team den letzten Schritt des Expand-and-Contract-Prozesses durch (**Contract**): Das veraltete Feld `"address"` wird aus der Schnittstelle entfernt.

Die neue Datei [`data/persons-v3-clean.json`](data/persons-v3-clean.json) sieht nun so aus:

```json
[
  {
    "id": "p-101",
    "firstName": "Anna",
    "lastName": "Muster",
    "email": "anna.muster@example.ch",
    "addressDetails": {
      "street": "Bahnhofstrasse 12",
      "zipCode": "8001",
      "city": "Zürich"
    }
  },
  {
    "id": "p-102",
    "firstName": "Luca",
    "lastName": "Bernasconi",
    "email": "luca.bernasconi@example.ch",
    "addressDetails": {
      "street": "Via Nassa 5",
      "zipCode": "6900",
      "city": "Lugano"
    }
  }
]
```

### Deine Aufgabe (Schritt 4)

1. Füge in [`PersonReaderTest.kt`](src/test/kotlin/ch/tbz/m321/PersonReaderTest.kt) einen weiteren Unit-Test für `File("data/persons-v3-clean.json")` hinzu und führe alle Tests aus.
   - *Hinweis:* Falls dieser Test wegen eines fehlenden `address`-Feldes fehlschlägt (`MissingKotlinParameterException`), stelle sicher, dass `val address: String? = null` in deiner `data class Person` als nullable mit Default-Wert definiert ist!
2. Überprüfe, dass deine Test-Suite für **alle drei** gültigen Evolutionsstufen gleichzeitig **grün** ist:
   - `persons-v1.json`
   - `persons-v2-compatible.json`
   - `persons-v3-clean.json`
3. *(Optional)* Sobald in der Praxis sicher ist, dass `v1` nirgends mehr produziert wird, könnte man das alte Feld `address` auch aus der `Person`-Klasse entfernen.

---

## Zusammenfassung: Regeln für einen Tolerant Reader

- **Unbekannte Felder ignorieren:** Konfiguriere deinen JSON-Parser immer so, dass neue/unbekannte Felder im JSON keinen Fehler auslösen (`FAIL_ON_UNKNOWN_PROPERTIES = false` bzw. `@JsonIgnoreProperties(ignoreUnknown = true)`).
- **Optionale Felder & Null-Safety:** Gehe nicht davon aus, dass jedes Feld für immer vorhanden bleibt. Arbeite in Kotlin mit nullable Typen und Default-Werten (`val oldField: String? = null`).
- **Expand and Contract:** Ändere niemals den Datentyp eines bestehenden JSON-Feldes direkt. Führe stattdessen ein neues Feld parallel ein, migriere die Consumer und entferne das alte Feld erst am Schluss.

---

## Zusatz-Aufgabe 1: Upgrade auf Jackson 3

Über viele Jahre war es einer der häufigsten Fehler in Java/Kotlin-Projekten, dass Entwickler vergessen haben, `FAIL_ON_UNKNOWN_PROPERTIES` in **Jackson 2** auszuschalten – beim kleinsten neuen Feld im JSON stürzten Produktivsysteme ab.

Das Jackson-Team hat daraus gelernt und mit **Jackson 3** das Verhalten geändert: **In Jackson 3 ist `FAIL_ON_UNKNOWN_PROPERTIES` standardmässig deaktiviert (`false`)!** Jackson 3 verhält sich also *out-of-the-box* wie ein Tolerant Reader gegenüber unbekannten Feldern.

### Probier es selbst aus:

1. Öffne [`build.gradle.kts`](build.gradle.kts): Kommentiere die Jackson-2-Dependency aus und aktiviere stattdessen **Jackson 3**:
   ```kotlin
   implementation("tools.jackson.module:jackson-module-kotlin:3.2.4")
   ```
2. Aktualisiere die Imports in `PersonReader.kt` (und ggf. `PersonReaderTest.kt`) von `com.fasterxml.jackson.*` auf das neue Package **`tools.jackson.*`** (z.B. `import tools.jackson.module.kotlin.jacksonObjectMapper` und `import tools.jackson.module.kotlin.readValue`).
3. **Entferne** nun deine Konfiguration `@JsonIgnoreProperties(ignoreUnknown = true)` bzw. `.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)` aus `PersonReader.kt`.
4. Führe alle deine Unit-Tests erneut aus – selbst wenn deine `Person`-Klasse ein Feld im JSON nicht kennt, laufen die Tests mit `jacksonObjectMapper()` in Jackson 3 ohne zusätzliche Konfiguration **grün** durch!

---

## Zusatz-Aufgabe 2: Andere Sprache / Technologie

Wie verhalten sich andere Programmiersprachen und JSON-Bibliotheken bei denselben 4 JSON-Dateien? Sind sie von Haus aus "tolerant" (wie Jackson 3) oder "strikt" (wie Jackson 2)?

Wähle eine andere Sprache oder Bibliothek deiner Wahl, z.B.:
- **Kotlin Serialization** (`kotlinx.serialization.json.Json` – wie verhält sich `ignoreUnknownKeys` standardmässig?)
- **TypeScript / JavaScript** (`JSON.parse`, evtl. mit `zod`)
- **Python** (`json.loads`, `dataclasses` oder `Pydantic`)
- **C# / .NET** (`System.Text.Json` oder `Newtonsoft.Json`)
- **Go** (`encoding/json` mit `struct`-Tags)
- **Rust** (`serde_json`)

### Auftrag

1. Implementiere das Einlesen und die Prüfung für [`data/persons-v1.json`](data/persons-v1.json) in der gewählten Sprache (gerne ebenfalls als Unit-Test).
2. Teste nacheinander [`persons-v2-breaking.json`](data/persons-v2-breaking.json), [`persons-v2-compatible.json`](data/persons-v2-compatible.json) und [`persons-v3-clean.json`](data/persons-v3-clean.json).
3. **Vergleiche mit Jackson 2 & Jackson 3:**
   - Musstest du unbekannte Felder (`persons-v2-compatible.json`) explizit ignorieren, oder macht die Sprache/Library das automatisch?
   - Wie verhält sich die Sprache bei [`persons-v2-breaking.json`](data/persons-v2-breaking.json) (gibt es einen Fehler beim Parsen, erst bei der Formatierung, oder wird z.B. `[object Object]` ausgegeben)?
