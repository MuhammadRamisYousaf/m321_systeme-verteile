package ch.tbz.m321

import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import java.io.File

data class Person(
    val id: String,
    val firstName: String,
    val lastName: String,
    val email: String,
    val address: String
)

class PersonReader {

    private val mapper = jacksonObjectMapper()

    /** Liest Personen ein, gibt die formatierten Zeilen aus und liefert sie fuer Tests zurueck. */
    fun readAndFormatPersons(jsonFile: File): List<String> {
        val persons = mapper.readValue<List<Person>>(jsonFile)
        return persons.map { person ->
            "[${person.id}] ${person.firstName} ${person.lastName} (${person.email}) - Adresse: ${person.address}"
        }.also { lines -> lines.forEach(::println) }
    }
}
