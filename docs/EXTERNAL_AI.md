# Zewnętrzna analiza AI

Domyślny provider `local` działa bez sieci. Provider `openai` wysyła wybrane,
znormalizowane metryki raportu do API Responses. Dowolny tekst alertów wejściowych
nie jest dodawany do żądania. Odpowiedź modelu jest sugestią i nie uruchamia poleceń.

W GUI wybierz provider `openai`, wskaż raport i użyj przycisku ustawienia klucza
sesji. Klucz jest przechowywany tylko w pamięci procesu. W CLI używany jest
`OPENAI_API_KEY` ze środowiska. Nie zapisuj klucza w repozytorium ani w raportach.

Przed wysłaniem można obejrzeć dokładne żądanie:

```powershell
python app.py --input raport.json --provider openai --preview-send
python app.py --input raport.json --provider openai --model gpt-5-mini
```

Model można zmienić przez `--model` lub `PRESTIGE_AI_MODEL`. Dostęp do modelu
i limity zależą od konta API. Żądanie ustawia `store=false`; nie jest to obietnica
braku retencji po stronie dostawcy. GUI pyta przed wysłaniem metryk.

Test rzeczywistego połączenia z syntetycznymi metrykami zwrócił HTTP 429.
Nie potwierdzono odpowiedzi modelu na użytym koncie; testy lokalne i testy
z podstawioną odpowiedzią HTTP przechodzą. Nie ma automatycznych ponowień.

Dokumentacja dostawcy: https://developers.openai.com/api/docs/guides/text

