plugins {
    kotlin("jvm") version "2.3.20"
}

group = "ch.tbz.m321"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    // Jackson 2 (wirft standardmässig einen Fehler bei unbekannten JSON-Feldern)
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.21.2")

    // Für die Bonus-Aufgabe in Teil 4 (Upgrade auf Jackson 3):
    // implementation("tools.jackson.module:jackson-module-kotlin:3.2.4")

    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        showStandardStreams = true
        events("passed", "skipped", "failed")
    }
}

kotlin {
    jvmToolchain(21)
}
