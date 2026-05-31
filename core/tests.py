import os
from django.test import TestCase
from .models import SimulationSession, TrajectoryPoint, ValidationError
from .parsers import parse_mat_dspace
from .validators import validate_dataframe
from .services import save_import_to_db

class DspaceIntegrationTest(TestCase):
    def setUp(self):
        # Ścieżka do pliku przesłanego przez prowadzącego.
        # Zakładamy, że plik leży w głównym folderze projektu (obok manage.py)
        self.file_path = "2000_0_0_Wiatr20_Wyrz40.mat"

    def test_full_dspace_import_pipeline(self):
        """
        Testuje pełną ścieżkę: Parser (HDF5) -> Walidator (Pydantic) -> Zapis (DB)
        na prawdziwym pliku sprzętowym.
        """
        # 1. Sprawdzenie, czy plik na pewno znajduje się w dobrym miejscu
        if not os.path.exists(self.file_path):
            self.skipTest(f"Nie znaleziono pliku: {self.file_path}. Umieść go obok manage.py!")

        # 2. PARSOWANIE
        df = parse_mat_dspace(self.file_path)
        
        # Jeśli parser zwróci pusty DataFrame, oznacza to, że nazwy struktur 
        # w pliku (X, Y) nie pokrywają się z naszymi założeniami.
        self.assertFalse(df.empty, "BŁĄD: Parser zwrócił pustą tabelę! Prawdopodobnie zła struktura pliku (KeyError).")
        
        # Sprawdzamy czy parser utworzył poprawne kolumny
        self.assertIn('time', df.columns)
        self.assertIn('x', df.columns)
        self.assertIn('y', df.columns)
        self.assertIn('z', df.columns)

        # 3. WALIDACJA
        valid_rows, invalid_rows = validate_dataframe(df)
        
        # Oczekujemy, że z pliku odczytano poprawne dane
        self.assertGreater(len(valid_rows), 0, "BŁĄD: Pydantic odrzucił wszystkie dane!")

        # 4. ZAPIS DO BAZY
        save_import_to_db(self.file_path, valid_rows, invalid_rows)

        # 5. WERYFIKACJA W BAZIE
        sesja_count = SimulationSession.objects.count()
        punkty_count = TrajectoryPoint.objects.count()

        self.assertEqual(sesja_count, 1, "Nie utworzono sesji symulacji w bazie.")
        self.assertEqual(punkty_count, len(valid_rows), "Liczba punktów w bazie nie zgadza się z liczbą poprawnych wierszy.")

        # Opcjonalnie wyświetlamy na końcu testu krótki raport
        print(f"\n[SUKCES] Odczytano, zwalidowano i zapisano do bazy: {punkty_count} punktów trajektorii z pliku {self.file_path}.")