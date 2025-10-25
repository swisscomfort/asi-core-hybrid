# Sektion IV – Datenschutz & Anonymisierung (FR-013)

**Traceability**: Erfüllt FR-013 - "Content MUST address privacy protection through anonymization strategies and zero-knowledge principles"

## Lernziele

Nach Abschluss dieser Sektion sollten Sie in der Lage sein:

- Die datenschutzspezifische Anwendung der drei Kernprinzipien "Lokal. Anonym. Für immer." zu erklären
- Die fünf Datenschutz-Policies (Collection, Processing, Transfer, Storage, Deletion) zu beschreiben
- Mechanismen zur Datenminimierung, Anonymisierung und K-Anonymität zu verstehen
- Datenklassen zu unterscheiden und entsprechende Schutzmaßnahmen zu benennen
- QA-Gates für Datenschutz-Compliance zu identifizieren
- Praktische Datenschutz-Szenarien zu analysieren und Schutzmaßnahmen abzuleiten

---

## 1. Datenschutz-Grundsätze

Die drei Kernprinzipien des ASI Core Systems haben im Datenschutz-Kontext spezifische Bedeutungen und Implementierungen:

### 🏠 Lokal (Privacy by Design)
**Grundsatz**: Persönliche Daten verbleiben grundsätzlich auf dem Nutzergerät

**Datenschutz-Umsetzung**:
- **On-Device Processing**: Alle sensiblen Verarbeitungen (NLP, Embedding-Generierung) erfolgen lokal
- **Lokale Verschlüsselung**: Daten werden bereits im Gerätespeicher verschlüsselt
- **Minimale Netzwerk-Exposition**: Nur wenn unbedingt notwendig verlassen Daten das Gerät
- **Nutzer-Kontrolle**: Vollständige Transparenz und Kontrolle über alle Datenflüsse

### 👤 Anonym (Zero-Knowledge First)
**Grundsatz**: Interaktionen mit dem Netzwerk erfolgen ohne Preisgabe von Identitäten oder Inhalten

**Datenschutz-Umsetzung**:
- **Pseudonyme Identitäten**: DIDs statt Klarnamen
- **Zero-Knowledge Proofs**: Eigenschaften beweisen ohne Daten preiszugeben
- **Differenzierende Hashes**: Inhalts-Commitments statt Rohdaten
- **K-Anonymität**: Nur aggregierte Metriken, nie Einzelwerte

### ♾️ Für immer (Retention by Choice)
**Grundsatz**: Dauerhaftigkeit nur für explizit freigegebene, anonymisierte Artefakte

**Datenschutz-Umsetzung**:
- **Lokale Löschkontrolle**: Nutzer kann lokale Daten jederzeit löschen
- **Netzwerk-Artefakte sind personenfrei**: Nur Proofs/Hashes werden permanent gespeichert
- **Expiry-Mechanismen**: Zeitlich begrenzte Autorisierungen (UCAN)
- **Right to be Forgotten**: Durch Design unmöglich, da keine PII im Netzwerk

---

## 2. Datenschutz-Policies

### Collection (Sammlung)
**Policy**: Keine PII sammeln; Defaults „opt-out of telemetry"

**Implementierung**:
- **PII-Verbot**: System ist so designed, dass PII-Sammlung technisch nicht möglich ist
- **Opt-Out Default**: Telemetrie und Analytik sind standardmäßig deaktiviert
- **Explizite Einwilligung**: Nutzer muss aktiv zustimmen, bevor Metadaten geteilt werden
- **Granulare Kontrolle**: Separate Einstellungen für verschiedene Datentypen

### Processing (Verarbeitung)
**Policy**: On-device; nur aggregierte/abgeleitete Werte

**Implementierung**:
- **Edge Computing**: Alle KI-Operationen erfolgen auf dem Nutzergerät
- **Aggregation Only**: Nur statistische Zusammenfassungen, nie Rohdaten
- **Differential Privacy**: Mathematische Verfahren zur Anonymisierung
- **Derived Values**: Hashes, Embeddings, Scores statt Originalinhalte

### Transfer (Übertragung)
**Policy**: Nur Proof/Meta; Ende-zu-Ende gesichert

**Implementierung**:
- **Proof-Only Transfer**: Kryptographische Beweise statt Daten
- **E2E Encryption**: Alle Netzwerk-Kommunikation verschlüsselt
- **TLS + Application Layer**: Mehrschichtige Verschlüsselung
- **Metadata Minimization**: Nur notwendige Metadaten übertragen

### Storage (Speicherung)
**Policy**: Verschlüsselt lokal; im Netzwerk nur nicht-PII-Artefakte

**Implementierung**:
- **Local Encryption**: AES-256 für lokale SQLite-Datenbank
- **Key Vault**: Sichere Schlüsselverwaltung auf dem Gerät
- **Network Storage**: Nur anonymisierte Hashes und Proofs
- **No-PII Guarantee**: Technisch unmöglich, PII im Netzwerk zu speichern

### Deletion (Löschung)
**Policy**: Lokale Löschung kontrolliert; Netz-Artefakte sind nicht personenbezogen

**Implementierung**:
- **User-Controlled Deletion**: Nutzer kann lokale Daten jederzeit vollständig löschen
- **Secure Deletion**: Kryptographische Löschung durch Key-Destruction
- **Network Immunity**: Netzwerk-Artefakte enthalten keine personenbezogenen Daten
- **Expiry by Design**: Autorisierungen laufen automatisch ab

---

## 3. Datenschutz-Mechanismen

### Datenminimierung
**Ziel**: Nur absolut notwendige Daten erheben und verarbeiten

**Mechanismen**:
- **Schema-Validation**: Automatische Prüfung auf PII-Felder (verboten)
- **Linter/CI-Checkliste**: Kontinuierliche Überwachung in der Entwicklung
- **Field Whitelisting**: Nur explizit erlaubte Datenfelder
- **Purpose Limitation**: Jedes Datenfeld hat einen definierten, begrenzten Zweck

### Anonymisierung/Pseudonymisierung
**Ziel**: Nutzer-Identitäten unerkennbar machen

**Mechanismen**:
- **DID statt Nutzername**: Dezentrale Identifikatoren ohne persönlichen Bezug
- **Rotierende Schlüssel/Tags**: Regelmäßiger Wechsel der kryptographischen Identitäten
- **Salt-basierte Hashing**: Verhinderung von Rainbow-Table-Angriffen
- **Temporal Isolation**: Zeitliche Trennung von Aktivitäten

### K-Anonymität (praktisch)
**Ziel**: Einzelpersonen in Gruppen ununterscheidbar machen

**Mechanismen**:
- **Gruppen/Quantiles**: Veröffentlichung nur in Buckets mit mindestens k Personen
- **Statistical Disclosure Control**: Mathematische Verfahren zur Anonymisierung
- **Noise Injection**: Kontrollierte Störsignale in Statistiken
- **Minimum Group Size**: k ≥ 5 für alle veröffentlichten Metriken

### Differenzierung von Meta
**Ziel**: Metadaten von Inhalten trennen

**Mechanismen**:
- **Hashes/Commitments statt Inhalte**: Eindeutige Referenzen ohne Inhaltspreisgabe
- **Salts/Nonces gegen Linkability**: Verhinderung der Verknüpfung verschiedener Aktivitäten
- **Content-Addressable Storage**: IPFS-Style Referenzierung
- **Temporal Decorrelation**: Zeitliche Entkopplung von Aktionen

### ZK-Prinzipien (High-Level)
**Ziel**: "Beweise die Eigenschaft X, ohne X offenzulegen"

**Beispiele**:
- **Besitz-Nachweis**: "Ich besitze Datei X" ohne X zu zeigen
- **Verfügbarkeits-Proof**: "Mein Node ist online" ohne Aktivitätsdaten preiszugeben
- **Quality-Score**: "Mein Beitrag hat Score > Threshold" ohne Inhalt zu zeigen
- **Compliance-Proof**: "Meine Daten erfüllen Policy Y" ohne Details zu nennen

### Side-Channel-Mitigation
**Ziel**: Verhinderung von Informationsleckage durch Timing und Verhalten

**Mechanismen**:
- **Batch/Timing-Jitter**: Zufällige Verzögerungen für Netz-Events
- **Rate Limiting**: Begrenzung der Aktivitätsfrequenz
- **Uniform Response Times**: Konstante Antwortzeiten unabhängig vom Inhalt
- **Traffic Analysis Protection**: Verschleierung von Kommunikationsmustern

### Logging
**Ziel**: Debugging ermöglichen ohne Nutzdaten zu protokollieren

**Mechanismen**:
- **Standard „lokal-only"**: Logs verbleiben auf dem Gerät
- **Keine Nutzdaten**: Nur technische IDs und System-Events
- **Pseudonyme IDs**: DIDs und UUIDs statt persönlicher Bezeichner
- **Log Rotation**: Automatische Löschung alter Log-Dateien

---

## 4. Datenklassen & Beispiele

| Klasse | Beispiel | Darf das Repo verlassen? | Schutzmaßnahmen |
|--------|----------|-------------------------|-----------------|
| **PII** | Name, E-Mail, GPS, IP-Adresse | **Nein** | N/A (nicht erheben) |
| **Pseudonyme IDs** | DID, UCAN Token IDs, Session-Keys | Nur Proof/Meta | Rotation, minimal disclosure |
| **Telemetrie-Meta** | Uptime-Prozent, Fehlerraten, Performance-Metriken | Aggregiert | Bucketing, Differentialität |
| **Proof-Artefakte** | Verfügbarkeits-Proofs, Hash-Commitments | Ja | Signatur, Nonce, Hash, Expiry |
| **Lokale Inhalte** | Nutzer-Reflexionen, persönliche Notizen | Lokal | Verschlüsselung, Schlüssel-Vault |
| **System-Metadaten** | Versions-Info, Config-Hashes | Ja | Keine PII-Bezug, öffentlich |

### Detaillierte Klassifizierung

**PII (Personally Identifiable Information)**:
- **Definition**: Jede Information, die direkt oder indirekt zur Identifikation einer Person führen kann
- **Behandlung**: Technisch unmöglich zu erheben oder zu speichern
- **Beispiele**: Klarnamen, E-Mail-Adressen, Telefonnummern, biometrische Daten

**Pseudonyme Identifikatoren**:
- **Definition**: Technische IDs ohne direkten Personenbezug
- **Behandlung**: Rotation und minimale Preisgabe
- **Beispiele**: DID:key:xyz..., UCAN-Tokens, kryptographische Public Keys

**Aggregierte Telemetrie**:
- **Definition**: Statistische Zusammenfassungen ohne Einzelperson-Bezug
- **Behandlung**: k-Anonymität und Differential Privacy
- **Beispiele**: "95% der Nodes haben Uptime > 99%", "Median Response Time: 250ms"

---

## 5. Prüf-/Freigabe-Gates (QA)

### Schema-Gate
**Zweck**: Verhinderung von PII-Feldern in Datenstrukturen

**Implementierung**:
- **Automatische Checkliste**: CI/CD prüft alle Schemas auf verbotene Felder
- **Grep-basierte Tests**: `grep -i "name\|email\|phone\|address" schemas/` → Fehler
- **Whitelist-Ansatz**: Nur explizit erlaubte Feldtypen
- **Review-Requirement**: Jede Schema-Änderung benötigt Datenschutz-Review

### Flow-Gate
**Zweck**: Sicherstellen, dass nur Proofs, nicht Daten übertragen werden

**Implementierung**:
- **Proof-not-Data-Prinzip**: Jeder Transferpfad muss belegen "nur Proof"
- **Network Interface Audit**: Alle API-Endpunkte auf PII-Freiheit prüfen
- **Encryption-by-Default**: Jede Übertragung ist verschlüsselt
- **Payload-Analyse**: Automatische Überprüfung der Datenstrukturen

### Log-Gate
**Zweck**: Keine Nutzdaten in Log-Ausgaben

**Implementierung**:
- **Log-Sanitization**: Automatische Entfernung sensibler Daten aus Logs
- **Beispiel-Log-Prüfung**: Manuelle Review typischer Log-Ausgaben
- **Pseudonym-Only**: Logs enthalten nur DIDs und technische IDs
- **Local-Only Default**: Logs werden standardmäßig nur lokal gespeichert

### Threat-Gate
**Zweck**: Für jede Komponente Missbrauchsfälle dokumentiert

**Implementierung**:
- **Threat Modeling**: STRIDE-Analyse für jede Systemkomponente
- **Missbrauchsfall-Dokumentation**: "Was passiert, wenn Angreifer X versucht?"
- **Gegenmaßnahmen-Katalog**: Dokumentierte Schutzmaßnahmen für jeden Threat
- **Red-Team-Tests**: Regelmäßige Angriffssimulationen

### Retention-Gate
**Zweck**: Kontrollierte Löschpfade vorhanden

**Implementierung**:
- **Lokale Löschpfade**: User kann alle lokalen Daten löschen
- **Netz-Artefakte personenfrei**: Beweise, dass Netzwerk-Daten keine PII enthalten
- **Expiry-Mechanismen**: Automatische Ablaufzeiten für Autorisierungen
- **Retention-Tests**: Regelmäßige Überprüfung der Löschfunktionalität

---

## 6. Beispiel-Szenarien

### S1 – Reward-Proof
**Szenario**: Node weist Verfügbarkeit nach und erhält Token-Belohnung

**Datenschutz-Ablauf**:
1. **Lokal**: Node generiert Verfügbarkeits-Proof (Zero-Knowledge)
2. **Transfer**: Nur kryptographischer Proof + DID werden übertragen
3. **Netzwerk**: Smart Contract verifiziert Proof, keine Inhalte gespeichert
4. **Result**: Token-Belohnung an pseudonyme Wallet

**Datenschutz-Eigenschaften**:
- ✅ Kein Inhalt verlässt das Gerät
- ✅ Nur pseudonyme Identität (DID) verwendet
- ✅ Proof ist nicht zu Nutzer-Aktivitäten verlinkbar
- ✅ Belohnung erfolgt an anonyme Wallet

### S2 – Fehlerbericht
**Szenario**: Lokaler Fehler (Timeout) wird für Systemverbesserung gemeldet

**Datenschutz-Ablauf**:
1. **Lokal**: Fehler wird intern geloggt (nur technische Details)
2. **Aggregation**: Nach k-Anonymität werden nur aggregierte Kennzahlen erstellt
3. **Optional**: Nutzer kann entscheiden, ob aggregierte Daten geteilt werden
4. **Transfer**: Nur statistischer Bucket (z.B. "Timeout-Rate: 2-5%") übertragen

**Datenschutz-Eigenschaften**:
- ✅ Keine individuellen Fehlerdaten verlassen das Gerät
- ✅ Nur k-anonyme Buckets (k≥5) werden geteilt
- ✅ Opt-in für jede Datenübertragung
- ✅ Differential Privacy schützt vor Re-Identifikation

### S3 – Identität & Autorisierung
**Szenario**: Nutzer autorisiert Anwendung via UCAN

**Datenschutz-Ablauf**:
1. **DID-Generierung**: Lokale Erstellung einer pseudonymen Identität
2. **UCAN-Token**: Zeitlich begrenzte Autorisierung für spezifische Aktionen
3. **Delegation**: Minimale Berechtigungen für definierten Zeitraum
4. **Expiry**: Automatischer Ablauf ohne Nutzer-Intervention erforderlich

**Datenschutz-Eigenschaften**:
- ✅ Keine Klarnamen oder PII erforderlich
- ✅ Zeitlich begrenzte Autorisierungen
- ✅ Principle of Least Privilege
- ✅ Automatische Expiry verhindert langfristige Verlinkbarkeit

---

## 7. Abgrenzung & Nicht-Ziele

### ❌ Was das System NICHT leistet

**Kein Anspruch auf Rechtsberatung/Compliance-Text**:
- Juristische Rahmen (GDPR, CCPA, etc.) werden separat behandelt
- Keine rechtsverbindlichen Compliance-Aussagen
- Technische Datenschutz-Maßnahmen, nicht juristische Interpretation

**Keine Implementierungsdetails zu konkreten ZK-Libs/Protokollen**:
- Fokus auf konzeptuelle ZK-Prinzipien
- Spezifische Bibliotheken (libsnark, circom, etc.) sind Implementierungsdetails
- Algorithmische Details werden in technischer Dokumentation behandelt

**Kein Tracking/Profiling**:
- Grundsätzlich widerspricht Tracking dem Prinzip "Anonym"
- Keine Verhaltensanalyse oder Profilerstellung
- Keine Cross-Device oder Cross-Session Correlation

### ✅ Was das System leistet

**Privacy by Design**:
- Technische Architektur verhindert Datenschutz-Verletzungen
- Proaktiver, nicht reaktiver Datenschutz
- Datenschutz als Kerneigenschaft, nicht als Add-On

**Technische Anonymisierung**:
- Mathematisch fundierte Anonymisierungs-Verfahren
- Zero-Knowledge-Prinzipien für minimale Datenpreisgabe
- Kryptographische Garantien für Pseudonymität

**Nutzer-Souveränität**:
- Vollständige Kontrolle über persönliche Daten
- Transparenz über alle Datenflüsse
- Technische Durchsetzung von Datenschutz-Prinzipien

---

## 8. Integration mit Kernprinzipien

### Synergie mit "Lokal. Anonym. Für immer."

**Datenschutz verstärkt Kernprinzipien**:
- **Lokal**: Privacy by Design macht lokale Verarbeitung zur Notwendigkeit
- **Anonym**: Zero-Knowledge und K-Anonymität implementieren Anonymität technisch
- **Für immer**: Pseudonyme Artefakte können dauerhaft sein, da sie nicht verlinkbar sind

**Kernprinzipien verstärken Datenschutz**:
- **Lokal**: Reduziert Angriffsfläche für Datenschutz-Verletzungen
- **Anonym**: Macht Re-Identifikation technisch unmöglich
- **Für immer**: Garantiert langfristige Verfügbarkeit ohne Datenschutz-Risiken

### Wirtschaftliche Anreize

**Token-Ökonomie unterstützt Datenschutz**:
- Belohnungen für datenschutz-konforme Beiträge
- Strafmechanismen (Slashing) für Datenschutz-Verletzungen
- Governance ermöglicht Anpassung von Datenschutz-Parametern

---

## 9. Traceability

**Erfüllt FR-013 vollständig**:
- ✅ Anonymisierung-Strategien detailliert (Pseudonymisierung, K-Anonymität)
- ✅ Zero-Knowledge-Prinzipien erklärt (Proof-basierte Verifikation)
- ✅ Privacy-Protection-Mechanismen implementiert (5 Policies, 6 Mechanismen)
- ✅ Praktische Beispiele und QA-Gates definiert

**Verweise**:
- `specs/001-core-system-detaillierter/spec.md` (§ Datenschutz-Requirements)
- `docs/studienführer/sektion-01-uebersicht.md` (Kernprinzipien-Kontext)
- `docs/studienführer/sektion-02-architektur.md` (Technische Umsetzung)

**Quiz-Integration**:
- Künftige Erweiterung: M5-M8, S3-S4 in `assessment-quiz.md`
- Datenschutz-spezifische Fragen zu Policies und Mechanismen
- Praktische Anwendung der ZK-Prinzipien

---

## Weiterführende Ressourcen

### Technische Standards
- **W3C DID Core**: Decentralized Identifiers specification
- **UCAN**: User Controlled Authorization Networks
- **Differential Privacy**: Mathematical framework for privacy protection

### Akademische Grundlagen
- **k-Anonymity**: Sweeney, L. (2002). k-anonymity: A model for protecting privacy
- **Zero-Knowledge Proofs**: Goldreich, O. (2001). Foundations of Cryptography
- **Privacy by Design**: Cavoukian, A. (2009). Privacy by Design principles

### Implementierungs-Guidelines
- **NIST Privacy Framework**: Structured approach to privacy risk management
- **OWASP Privacy Guide**: Web application privacy protection
- **ISO/IEC 27001**: Information security management systems
