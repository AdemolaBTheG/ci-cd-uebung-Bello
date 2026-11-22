# SonarQube Cloud einrichten

1. Mit dem GitHub-Konto `AdemolaBTheG` auf <https://sonarcloud.io> anmelden (EU-Region).
2. Die GitHub-App nur für `ci-cd-uebung-Bello` installieren und dieses öffentliche Repository in ein kostenloses SonarQube-Cloud-Projekt importieren.
3. Die tatsächlichen Schlüssel aus den Projektinformationen als GitHub-Actions-Variablen anlegen:
   - `SONAR_ORGANIZATION`: Organization Key.
   - `SONAR_PROJECT_KEY`: Project Key.
4. Unter My Account → Access Tokens einen Analyse-Token erzeugen. Diesen ausschließlich als Repository-Secret `SONAR_TOKEN` unter GitHub → Settings → Secrets and variables → Actions speichern. Keine Tokens in Dateien oder Commits eintragen.
5. Im Sonar-Projekt unter Administration → Analysis Method die Automatic Analysis deaktivieren: Die Analyse läuft über Maven in GitHub Actions.
6. Unter GitHub → Actions → SonarQube Cloud → Run workflow den Workflow auf `main` ausführen. Später startet er bei jedem Push auf `main` automatisch.

Der Workflow bricht bei fehlender Konfiguration mit einer konkreten Fehlermeldung ab. Er überspringt die Analyse nicht stillschweigend. Ein grüner Matrix-Build allein bestätigt deshalb noch keine erfolgreiche Sonar-Analyse.

## Aufteilung der Workflows

- `ci.yml`: Pushes und Pull Requests auf `main`, gefiltert auf Quellcode, POM und Workflows; manuell ebenfalls startbar. Drei Matrix-Varianten, jeweils eigene Artefakte. `fail-fast: false` liefert auch bei einem Plattformfehler die Ergebnisse der anderen Varianten.
- `sonar.yml`: Jeder Push auf `main` und manueller Start, ohne Pfadfilter. Ein separater Build mit Java 21 erzeugt Bytecode und JaCoCo-XML für die Maven-Analyse; `sonar.qualitygate.wait=true` prüft das serverseitige Ergebnis.

## Behandelte Probleme

### String-Referenzvergleich (java:S4973)

Vorher: `input.toLowerCase() == reversed.toLowerCase()` verglich Objektidentitäten; der vorhandene Test mit `Anna` schlug fehl. Jetzt vergleicht `input.equalsIgnoreCase(reversed)` den Inhalt ohne abhängig von der Standard-Locale kleinzuschreiben. Null bleibt `false`.

### Zu allgemeiner Exception-Handler (java:S2221)

Vorher fing `safeParseInt` jede `Exception` ab und ließ den Handler leer. Jetzt wird nur `NumberFormatException` abgefangen und der bisherige Fallback `0` unmittelbar zurückgegeben. Ungültige Zahlen, Null und Überlauf bleiben abgedeckt; andere Programmierfehler werden nicht pauschal verschluckt.

Diese Regelzuordnungen beschreiben die Codeänderungen. Die tatsächlich gemeldeten Findings und der Quality-Gate-Status müssen anhand eines erfolgreichen SonarQube-Cloud-Laufs belegt werden.
