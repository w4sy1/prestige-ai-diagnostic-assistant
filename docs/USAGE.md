# Użycie

`python app.py --input raport.json --output reports`
Przykład danych: `{"disk_free_percent":4,"packet_loss":8,"defender_enabled":true,"critical_errors":3}`.
Rozpoznaje też zagnieżdżone FreePercent i AntivirusEnabled z narzędzi Windows.

Warstwy: normalization.py, rules.py, providers.py, app.py. Domyślnie i w tej wersji
wyłącznie LOCAL MODE. DiagnosticProvider definiuje interfejs dla przyszłego opcjonalnego
AI; nie ma aktywnego zewnętrznego providera ani potrzeby klucza API.
Przy przyszłej integracji klucz tylko ze zmiennych środowiskowych/.env, nigdy z kodu;
provider musi ujawniać wysyłanie danych i wymagać świadomego wyboru użytkownika.
MVP ma cztery reguły i ograniczoną normalizację. Snapshoty bez tych metryk dają brak
pokrycia, nie pozytywny werdykt. Nie wykonuje poleceń z raportów ani zaleceń administracyjnych.

## Rozszerzenia 0.2.0

Analiza rozpoznaje metryki Windows/ADB/sieci, ostrzeżenia stanu dysku, temperatury,
jitter oraz brakujące moduły. Przenosi i deduplikuje alerty z Security Check/Malware Triage,
oznaczając je jako wskazania źródłowe, a nie niezależne potwierdzenie.
Progi są orientacyjne: porównaj temperaturę z limitem producenta. UNKNOWN nie oznacza awarii.
Całość nadal działa w LOCAL MODE; raport nie opuszcza urządzenia. Zewnętrzny provider
pozostaje opcjonalnym przyszłym rozszerzeniem i nie jest wymagany do tego trybu.
