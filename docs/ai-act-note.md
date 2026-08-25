# AI deployment note / Hinweis zum KI-Einsatz

## English

`ellmos-voice-io` is a technical component, not a complete deployed AI system.
It connects caller-selected local speech-to-text, text-to-speech, and wake-word
engines. It does not determine the legal classification of the application
that embeds it.

Intended uses are explicit transcription of caller-authorized audio, explicit
speech synthesis, and caller-controlled local wake-word detection. The module
is not designed or validated for biometric identification, emotion inference,
covert monitoring, employment or education decisions, medical diagnosis,
law-enforcement decisions, or other safety-critical/high-impact decisions.

The integrating application owns notices, consent, accessibility, retention,
human oversight, and any required identification of synthetic audio. A local
engine does not remove those responsibilities. No test in this repository
proves regulatory conformity of a deployed application.

## Deutsch

`ellmos-voice-io` ist eine technische Komponente und kein vollständig
eingesetztes KI-System. Es verbindet vom Aufrufer ausgewählte lokale Engines
für Speech-to-Text, Text-to-Speech und Wake-Word-Erkennung. Die rechtliche
Einordnung der einbettenden Anwendung wird dadurch nicht festgelegt.

Vorgesehen sind die ausdrückliche Transkription autorisierter Audiodaten, die
ausdrückliche Sprachsynthese und eine vom Aufrufer kontrollierte lokale
Wake-Word-Erkennung. Das Modul ist weder für biometrische Identifizierung,
Emotionserkennung, verdeckte Überwachung, Entscheidungen in Beschäftigung oder
Bildung, medizinische Diagnosen, Strafverfolgungsentscheidungen noch andere
sicherheitskritische oder folgenreiche Entscheidungen entwickelt oder geprüft.

Die einbettende Anwendung verantwortet Hinweise, Einwilligung, Barrierefreiheit,
Aufbewahrung, menschliche Aufsicht und eine gegebenenfalls erforderliche
Kennzeichnung synthetischer Audiodaten. Eine lokale Engine hebt diese Pflichten
nicht auf. Kein Test dieses Repositories belegt die regulatorische Konformität
einer eingesetzten Anwendung.
