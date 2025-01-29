# Climbing Route Creator - Przewodnik Użytkownika

## Spis treści
1. [Pierwsze kroki](#pierwsze-kroki)
2. [Interfejs aplikacji](#interfejs-aplikacji)
3. [Tworzenie drogi](#tworzenie-drogi)
4. [Edycja i poprawki](#edycja-i-poprawki)
5. [Zapisywanie drogi](#zapisywanie-drogi)
6. [Najczęstsze problemy](#najczęstsze-problemy)

## Pierwsze kroki

### Wymagania systemowe
- System operacyjny: Windows 10/11, Linux lub macOS
- Minimalne wymagania:
  - 4GB RAM
  - Procesor dual-core 2.0 GHz
  - 500MB wolnego miejsca na dysku

### Uruchomienie aplikacji
1. Uruchom plik wykonywalny aplikacji
2. Zobaczysz ekran powitalny z opcją wczytania zdjęcia
3. Możesz przeciągnąć zdjęcie na okno lub kliknąć przycisk "Upload Wall Image"

### Przygotowanie zdjęcia
- Używaj zdjęć w formacie JPG lub PNG
- Upewnij się, że ściana jest dobrze oświetlona
- Unikaj zdjęć z dużymi cieniami lub odblaskami
- Zalecana rozdzielczość: minimum 1920x1080 pikseli

## Interfejs aplikacji

### Pasek narzędzi
- **New Route** - rozpoczyna nową drogę
- **Save Route** - zapisuje aktualną drogę
- **Hands/Feet** - przełącza między trybem zaznaczania chwytów dla rąk/nóg
- **Edit Curves** - włącza tryb edycji połączeń między chwytami
- **Instructions** - wyświetla instrukcję obsługi
- **Grade Selector** - wybór trudności drogi

### Kolory i oznaczenia
- Pomarańczowy - chwyty dla rąk
- Czerwony - chwyty dla nóg
- Szary - niewybrane chwyty
- Niebieskie podświetlenie - aktualnie edytowany element

## Tworzenie drogi

### Krok 1: Wczytanie zdjęcia
1. Wybierz zdjęcie ściany wspinaczkowej
2. Poczekaj na automatyczną detekcję chwytów
3. Wszystkie wykryte chwyty zostaną podświetlone na szaro

### Krok 2: Zaznaczanie chwytów
1. Wybierz tryb "Hands" lub "Feet" z paska narzędzi
2. Klikaj chwyty w kolejności ich użycia:
   - Dla rąk: start → kolejne chwyty → top
   - Dla nóg: analogicznie jak dla rąk
3. Chwyty będą automatycznie numerowane w kolejności zaznaczania

### Krok 3: Edycja połączeń
1. Włącz tryb "Edit Curves"
2. Kliknij środek linii aby zmienić ją na krzywą
3. Przeciągnij punkty kontrolne aby dostosować kształt
4. Prawy przycisk myszy na linii przełącza między prostą a krzywą

## Edycja i poprawki

### Usuwanie zaznaczenia
- Kliknij ponownie zaznaczony chwyt aby go odznaczyć
- Wszystkie kolejne chwyty zostaną automatycznie przenumerowane

### Zmiana kolejności
1. Odznacz chwyt, który chcesz przesunąć w kolejności
2. Zaznacz go ponownie w odpowiednim momencie

### Edycja krzywych
- Używaj punktów kontrolnych do dostosowania kształtu krzywych
- Można przełączać między liniami prostymi a krzywymi
- Krzywe pomagają lepiej zobrazować ruch między chwytami

## Zapisywanie drogi

### Krok 1: Rozpoczęcie zapisu
1. Kliknij "Save Route" na pasku narzędzi
2. Wypełnij formularz z informacjami:
   - Nazwa drogi
   - Stopień trudności
   - Autor
   - Opis (opcjonalny)

### Krok 2: Eksport
1. Wybierz lokalizację zapisu
2. Droga zostanie zapisana w dwóch formatach:
   - Plik JSON z danymi drogi
   - Obraz JPG z wizualizacją

### Krok 3: Weryfikacja
- Sprawdź czy wszystkie informacje są poprawne
- Otwórz wygenerowany obraz aby upewnić się, że wszystko jest widoczne
- W razie potrzeby możesz wrócić do edycji i zapisać ponownie

## Najczęstsze problemy

### Problem z detekcją chwytów
- Upewnij się, że zdjęcie ma dobrą jakość
- Sprawdź oświetlenie na zdjęciu
- Spróbuj zrobić nowe zdjęcie pod innym kątem

### Problem z zaznaczaniem chwytów
- Upewnij się, że klikasz dokładnie w chwyt
- Sprawdź czy wybrany jest odpowiedni tryb (Hands/Feet)
- Spróbuj przybliżyć widok jeśli chwyty są małe

### Problem z zapisem
- Sprawdź czy wszystkie wymagane pola są wypełnione
- Upewnij się, że masz uprawnienia do zapisu w wybranej lokalizacji
- Sprawdź czy jest wystarczająco miejsca na dysku
