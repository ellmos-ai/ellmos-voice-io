# Contributing / Mitwirken

## English

1. Open an issue before a behavioral or public-API redesign.
2. Keep every engine optional and lazily imported.
3. Preserve the no-storage, no-telemetry, no-implicit-network boundary.
4. Tests must not open microphones, play audio, download models, or require
   platform voices. Use deterministic test doubles.
5. Add a regression test for every privacy, lifecycle, or engine-routing bug.
6. Run `python -m pytest -q`, `python -m ruff check .`,
   `python -m compileall -q src`, `python -m build`, and
   `python tools/normalize_sdist.py "dist/*.tar.gz" --epoch 1787270400`,
   then `python -m twine check dist/*`.
7. Keep English and German README structure and code blocks aligned.
8. Do not claim real engine, hardware, model, release, or registry evidence
   from mocked tests.

## Deutsch

1. Lege vor einem Verhaltens- oder Public-API-Umbau ein Issue an.
2. Halte jede Engine optional und lade sie erst bei ausdrücklicher Nutzung.
3. Erhalte die Grenzen: keine Speicherung, keine Telemetrie und kein implizites Netzwerk.
4. Tests dürfen kein Mikrofon öffnen, Audio abspielen, Modelle herunterladen
   oder Systemstimmen voraussetzen. Nutze deterministische Test-Doubles.
5. Ergänze für jeden Datenschutz-, Lebenszyklus- oder Engine-Routing-Fehler einen Regressionstest.
6. Führe `python -m pytest -q`, `python -m ruff check .`,
   `python -m compileall -q src`, `python -m build`,
   `python tools/normalize_sdist.py "dist/*.tar.gz" --epoch 1787270400` und
   danach `python -m twine check dist/*` aus.
7. Halte Struktur und Codeblöcke der englischen und deutschen README synchron.
8. Leite aus Mock-Tests keinen echten Engine-, Hardware-, Modell-, Release-
   oder Registry-Nachweis ab.
