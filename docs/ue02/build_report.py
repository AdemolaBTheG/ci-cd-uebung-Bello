"""Build the UE02 report from verified results and captured browser evidence."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Preformatted

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'docs/ue02/evidence'
OUTPUT = ROOT / 'output/pdf/UE02-Bericht-Bello.pdf'
RESULTS = json.loads((EVIDENCE / 'results.json').read_text())
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='SmallText', fontName='Helvetica', fontSize=9, leading=13, spaceAfter=6))
styles.add(ParagraphStyle(name='CodeBlock', fontName='Courier', fontSize=8, leading=11, backColor=colors.HexColor('#eef2f6'), borderPadding=8, spaceAfter=12))
styles['Normal'].fontSize = 10
styles['Normal'].leading = 14
styles['Heading1'].textColor = colors.HexColor('#163b57')
styles['Heading2'].textColor = colors.HexColor('#163b57')
styles['Title'].alignment = TA_LEFT
story = []
def p(text, style='Normal'):
    story.append(Paragraph(text, styles[style]))
def heading(text): p(text, 'Heading1')
def image(name, maxheight=128*mm):
    obj=Image(str(EVIDENCE/name))
    scale=min(174*mm/obj.imageWidth,maxheight/obj.imageHeight)
    obj.drawWidth=obj.imageWidth*scale;obj.drawHeight=obj.imageHeight*scale
    story.append(obj);story.append(Spacer(1,3*mm))
def code(text): story.append(Preformatted(text, styles['CodeBlock']))
def link(label,url): p(f'<a href="{escape(url)}" color="#17679c">{escape(label)}</a>','SmallText')
def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#d3dde5'));canvas.line(18*mm,16*mm,192*mm,16*mm)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#566674'))
    canvas.drawString(18*mm,11*mm,'Ademola Kevin Bello | CI/CD - UE02 | 22.11.2026')
    canvas.drawRightString(192*mm,11*mm,str(doc.page))

p('CI/CD - Übung 2', 'Title')
p('Matrix-Builds, Testberichte, Coverage und SonarQube Cloud', 'Heading2')
p('Ademola Kevin Bello · MC.ba VZ (WS26)', 'SmallText')
link('Repository', 'https://github.com/AdemolaBTheG/ci-cd-uebung-Bello')
p('Der Maven-Build führt alle 18 JUnit-Tests aus. Der ursprüngliche Palindromtest bleibt erhalten und besteht nach der Fehlerkorrektur. Lokal: Java 17; GitHub Actions: Temurin 17/21 auf Ubuntu und Windows.')
story.append(Spacer(1,3*mm))
data=[['Matrix-Variante','Ergebnis','Artefakte'],['Ubuntu / Java 17','Erfolgreich','Surefire + JaCoCo'],['Ubuntu / Java 21','Erfolgreich','Surefire + JaCoCo'],['Windows / Java 21','Erfolgreich','Surefire + JaCoCo']]
t=Table(data,colWidths=[70*mm,38*mm,66*mm],hAlign='LEFT')
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#163b57')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#edf3f7'),colors.white])]))
story.append(t);story.append(Spacer(1,3*mm))
p('<b>Ausschluss:</b> Windows/Java 17 ist ausgeschlossen. Beide Betriebssysteme und beide JDK-Versionen bleiben vertreten; Java 17 wird auf Ubuntu, Windows mit Java 21 geprüft. Das reduziert einen redundanten Job.','SmallText')
image('ci-matrix.jpg',95*mm)
p('Abbildung 1: Tatsächlicher GitHub-Actions-Lauf mit drei erfolgreichen Matrix-Jobs.','SmallText')
link('CI-Lauf und herunterladbare Test-/Coverage-Berichte',RESULTS['ci_url'])

story.append(PageBreak());heading('Pipeline und Coverage')
p('<b>CI:</b> Pushes und Pull Requests auf main; Pfadfilter für src/**, pom.xml und die Workflows. Manuelle Ausführung ist möglich. Concurrency verhindert doppelte CI-Läufe, fail-fast: false erhält die anderen Matrix-Ergebnisse bei einem Fehler.')
p('<b>Testberichte:</b> Surefire-XML und Textdateien werden mit if: always() hochgeladen. JaCoCo erzeugt HTML und XML; die Coverage-Artefakte werden nach erfolgreichen Tests gespeichert. Aufbewahrung: 30 Tage.')
p('<b>Sonar:</b> Ein eigener Workflow analysiert jeden Push auf main ohne Pfadfilter. Java 21, vollständige Git-Historie und ein Maven-Build liefern Bytecode und Coverage. Der Scanner wartet auf das serverseitige Quality Gate. Die Sonar-Analyse wird nicht stillschweigend übersprungen, wenn die Konfiguration fehlt.')
code('mvn --batch-mode --no-transfer-progress \\\n  -DskipTests=false clean verify\n\nCoverage: target/site/jacoco/jacoco.xml\nReports:  target/surefire-reports/')
p(f'<b>Gemessene Zeilen-Coverage:</b> {RESULTS["line_coverage"]}. Die Zahl stammt aus dem tatsächlich erzeugten JaCoCo-XML, nicht aus einer Schätzung.')
p('Die verbleibenden Lücken liegen hauptsächlich im Konsolen-Einstiegspunkt App und in NumberUtils. Tests werden nicht deaktiviert; Coverage-Dateien und Analyseergebnis bleiben überprüfbar.')
p('<b>Automatische Analyse:</b> Sonar Automatic Analysis wurde abgeschaltet, damit sie nicht mit der Maven-Analyse aus GitHub Actions konkurriert.')
image('ci-artifacts.jpg',115*mm)
p('Abbildung 2: Je drei Surefire- und JaCoCo-Artefakte, eindeutig nach Betriebssystem und Java-Version benannt.','SmallText')

story.append(PageBreak());heading('Fehlerkorrekturen: vorher / nachher')
p('1. Palindromprüfung - String-Inhalt statt Objektidentität','Heading2')
p('Der ursprüngliche Vergleich mit == prüfte Referenzen. Der bestehende Test mit Anna schlug fehl; Sonars initiale Analyse meldete java:S4973. equalsIgnoreCase vergleicht den Inhalt direkt und vermeidet die Abhängigkeit von der Standard-Locale beim Kleinschreiben. Null bleibt false.')
p('Vorher','SmallText');code('String reversed = new StringBuilder(input).reverse().toString();\nreturn input.toLowerCase() == reversed.toLowerCase();')
p('Nachher','SmallText');code('String reversed = new StringBuilder(input).reverse().toString();\nreturn input.equalsIgnoreCase(reversed);')
p('Nachweis: Der ursprüngliche Regressionstest isPalindrome_caseInsensitive_expectedTrue besteht jetzt. Weitere Fälle prüfen null, einen Nicht-Palindrom-String, leere Strings und einzelne Zeichen.','SmallText')
p('2. Integer-Parsing - gezielter Exception-Handler','Heading2')
p('Der alte Handler fing jede Exception ab und blieb leer. Dadurch hätten auch unerwartete Programmierfehler den Fallback 0 erzeugt. Jetzt werden ausschließlich ungültige Zahlen als NumberFormatException behandelt; der Handler gibt den Fallback explizit zurück. Dies adressiert das Muster der Sonar-Regel java:S2221.')
p('Vorher','SmallText');code('try {\n    return Integer.parseInt(s);\n} catch (Exception e) {\n    // leer\n}\nreturn 0;')
p('Nachher','SmallText');code('try {\n    return Integer.parseInt(s);\n} catch (NumberFormatException e) {\n    return 0;\n}')
p('Nachweis: Tests für gültige/ungültige Zahlen, negative Werte, null, leere Eingaben, Überlauf sowie Integer.MIN_VALUE und Integer.MAX_VALUE bestehen.','SmallText')
p(escape(RESULTS.get('finding_note','Die ursprüngliche automatische Analyse bestätigte S4973. Weitere Zuordnungen werden anhand der Maven-Analyse geprüft.')),'SmallText')

story.append(PageBreak());heading('SonarQube Cloud und Abschluss')
p(escape(RESULTS['sonar_summary']))
if (EVIDENCE/'sonar-after.jpg').exists():
    image('sonar-after.jpg',140*mm)
    p('Abbildung 3: Tatsächlicher Sonar-Dashboard-Status nach der Maven-Analyse.','SmallText')
link('SonarQube-Cloud-Projekt','https://sonarcloud.io/summary/overall?id=AdemolaBTheG_ci-cd-uebung-Bello&branch=main')
if RESULTS.get('sonar_run_url'): link('Sonar-Workflow in GitHub Actions',RESULTS['sonar_run_url'])
p('Probleme und Lösungen','Heading2')
p('Der absichtlich fehlschlagende Test blockierte den Ausgangsbuild. Die Implementierung wurde korrigiert, der Test erhalten. Sonars voreingestelltes Onboarding bot einen kostenpflichtigen Testplan und zusätzliche Projekte an; gewählt wurden der kostenlose Plan und ausschließlich das Übungsrepository. Die initiale automatische Analyse enthielt keine Test-Coverage; die Maven-Analyse importiert stattdessen das JaCoCo-XML.','SmallText')
p('Für die isolierte Vorher-Analyse des unveränderten Übung-1-Stands wurde der bekannte Testfehler einmalig mit maven.test.failure.ignore=true toleriert, damit Sonar die ursprüngliche Implementierung erfassen konnte. Die produktiven CI-Workflows ignorieren keine Testfehler.', 'SmallText')
p('Zugangsdaten liegen ausschließlich im Repository-Secret SONAR_TOKEN. Organization Key und Project Key werden als Actions-Variablen gepflegt. Keine Zugangsdaten sind Teil des Repositorys oder dieses Berichts.','SmallText')
p('Quellen und Abgabe','Heading2')
link('Aktuelle Aufgabenstellung','https://github.com/mrckurz/cicd-BA-uebung01/blob/main/README-UE02.md')
link('Implementierung und Prüfung (PR #2)','https://github.com/AdemolaBTheG/ci-cd-uebung-Bello/pull/2')
p('Abzugeben sind der Repository-Link und dieser PDF-Bericht in eLearning. Die veröffentlichte Aufgabenstellung nennt den 18.11.2026, 23:55; dieser Bericht dokumentiert den tatsächlichen Bearbeitungsstand vom 22.11.2026.','SmallText')

OUTPUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUTPUT),pagesize=(210*mm,297*mm),rightMargin=18*mm,leftMargin=18*mm,topMargin=17*mm,bottomMargin=22*mm,title='CI/CD Übung 2 - Ademola Kevin Bello',author='Ademola Kevin Bello').build(story,onFirstPage=footer,onLaterPages=footer)
print(OUTPUT)
