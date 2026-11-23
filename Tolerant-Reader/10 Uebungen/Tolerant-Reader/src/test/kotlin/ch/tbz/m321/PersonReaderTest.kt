package ch.tbz.m321

import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals

class PersonReaderTest {

    private val reader = PersonReader()

    private val expectedOutput = listOf(
        "[p-101] Anna Muster (anna.muster@example.ch) - Adresse: Bahnhofstrasse 12, 8001 Zürich",
        "[p-102] Luca Bernasconi (luca.bernasconi@example.ch) - Adresse: Via Nassa 5, 6900 Lugano"
    )

    @Test
    fun `Teil 1`() {
        val file = File("data/persons-v1.json")

        val result = reader.readAndFormatPersons(file)

        assertEquals(expectedOutput, result)
    }

    // TODO: Füge in Teil 2, Teil 3 und Teil 4 hier weitere Unit-Tests für die neuen JSON-Dateien hinzu!
}
