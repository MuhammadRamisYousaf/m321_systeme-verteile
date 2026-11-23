# Teil 3: Tolerant Reader & Schrittweise Migration

## Die Lösung für rückwärtskompatible Änderungen (Expand & Contract)

Anstatt das bestehende Feld `"address"` direkt durch ein Objekt zu überschreiben (Breaking Change!), wendet man das **Expand-and-Contract Pattern** (auch *Parallel Change* genannt) an:

1. **Expand (Erweitern):** Der Producer behält das alte Feld `"address"` (als `String`) vorerst bei und fügt **parallel ein neues Feld** `"addressDetails"` mit der strukturierten Adresse hinzu.
2. **Migrate (Migrieren):** Alle Consumer stellen in ihrem eigenen Tempo von `"address"` auf `"addressDetails"` um.
3. **Contract (Aufräumen):** Erst wenn kein Consumer mehr das alte Feld `"address"` nutzt, entfernt der Producer das alte Feld.

Das Partner-Team hat seinen Fehler eingesehen und liefert nun die Übergangsversion in [`data/persons-v2-compatible.json`](data/persons-v2-compatible.json):

```json
[
  {
    "id": "p-101",
    "firstName": "Anna",
    "lastName": "Muster",
    "email": "anna.muster@example.ch",
    "address": "Bahnhofstrasse 12, 8001 Zürich",
    "addressDetails": {
      "street": "Bahnhofstrasse 12",
      "zipCode": "8001",
      "city": "Zürich"
    }
  }
]
```

---

## Deine Aufgaben (Schritt 3)

### Schritt 3a: Das neue Format tolerieren, aber noch die alten Daten nutzen

1. Schreibe in [`PersonReaderTest.kt`](src/test/kotlin/ch/tbz/m321/PersonReaderTest.kt) einen neuen Unit-Test für `File("data/persons-v2-compatible.json")`, der prüft, ob `expectedOutput` zurückgegeben wird.
2. Führe den Test aus. **Was passiert?** Jackson 2 wirft standardmässig eine `UnrecognizedPropertyException`, weil deine `data class Person` das neue Feld `addressDetails` nicht kennt! Dein Reader ist also mit den Standardeinstellungen von Jackson 2 noch **kein** *Tolerant Reader*.
3. **Aufgabe:** Passe `PersonReader.kt` minimal an, sodass unbekannte Felder im JSON ignoriert werden, **ohne** dass du `addressDetails` bereits in deiner `data class` modellierst. Dein Programm soll weiterhin das alte Feld `address` nutzen.
   - *Hinweis für Jackson 2:* Nutze entweder `@JsonIgnoreProperties(ignoreUnknown = true)` an der `data class` oder konfiguriere den `mapper` mit `.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)`.
4. **Test:** Beide Unit-Tests (`persons-v1.json` und `persons-v2-compatible.json`) müssen nun **grün** sein!

---

### Schritt 3b: Auf die neuen strukturierten Daten umsteigen (mit Fallback)

Jetzt migrieren wir unseren `PersonReader` so, dass er die neuen Daten aus `addressDetails` verwendet, aber weiterhin rückwärtskompatibel zu `v1` bleibt:

1. Erstelle eine `data class AddressDetails(val street: String, val zipCode: String, val city: String)`.
2. Erweitere deine `data class Person` um das optionale Feld `val addressDetails: AddressDetails? = null` (und mache auch `val address: String? = null` optional).
3. Passe deine Formatierungslogik in `readAndFormatPersons` so an:
   - Wenn `addressDetails != null` ist, verwende die strukturierten Felder: `"${addressDetails.street}, ${addressDetails.zipCode} ${addressDetails.city}"`.
   - Wenn `addressDetails == null` ist, greife als Fallback auf den alten `address`-String zurück.
4. **Test:** Führe deine Unit-Tests für [`data/persons-v1.json`](data/persons-v1.json) **und** [`data/persons-v2-compatible.json`](data/persons-v2-compatible.json) erneut aus. Beide müssen weiterhin **grün** sein!

👉 **Wenn beide Tests grün sind, gehe weiter zu [Teil 4: Aufräumen & Bonus](Teil4-Abschluss-und-Bonus.md).**
