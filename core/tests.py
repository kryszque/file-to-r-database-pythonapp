from django.test import TestCase
from .models import SimulationSession, SystemSetting, SimulationResult, ValidationError
from .services import save_import_to_db

class DatabaseImportTests(TestCase):
    def setUp(self):
        # Ta funkcja uruchamia się przed każdym testem.
        # Przygotowujemy tu "sztuczne" dane, które udają to, co wypluwa nasz parser i walidator.
        
        self.file_path = "test_folder/symulacja.xlsx"
        
        self.settings_dict = {
            "tryb_pracy": "Eko",
            "temp_zadana": 65.0
        }
        
        self.valid_rows = [
            {
                "time": 0.5, 
                "value": {"Temperatura": 22.4, "Cisnienie": 1.2}
            },
            {
                "time": 1.0, 
                "value": {"Temperatura": 25.1, "Cisnienie": 1.8}
            }
        ]
        
        self.invalid_rows = [
            {
                "czas": 1.5,
                "szczegoly_bledu": "anomaly in column Temperatura : -99.0",
                "oryginalne_dane": "{'Temperatura': -99.0, 'Cisnienie': 2.1}"
            }
        ]

    def test_save_import_to_db_success(self):
        """
        Testuje, czy funkcja save_import_to_db poprawnie zapisuje wszystkie obiekty do bazy.
        """
        # 1. Wykonanie akcji: uruchamiamy Twoją funkcję
        save_import_to_db(
            file_path=self.file_path,
            valid_rows=self.valid_rows,
            invalid_rows=self.invalid_rows,
            settings_dict=self.settings_dict
        )

        # 2. Sprawdzenia (Asercje): pytamy bazę, co w niej jest
        
        # Sprawdzamy sesję
        self.assertEqual(SimulationSession.objects.count(), 1)
        sesja = SimulationSession.objects.first()
        self.assertEqual(sesja.source_path, self.file_path)

        # Sprawdzamy ustawienia (mieliśmy 2 klucze w słowniku)
        self.assertEqual(SystemSetting.objects.count(), 2)
        self.assertTrue(SystemSetting.objects.filter(setting_name="tryb_pracy").exists())

        # Sprawdzamy poprawne wyniki
        # Mamy 2 wiersze po 2 parametry (Temp i Cisnienie) = 4 rekordy
        self.assertEqual(SimulationResult.objects.count(), 4)
        
        # Sprawdźmy konkretną wartość z pierwszego wiersza
        temp_wynik = SimulationResult.objects.get(parameter="Temperatura", sim_time=0.5)
        self.assertEqual(temp_wynik.value, 22.4)

        # Sprawdzamy błędy
        self.assertEqual(ValidationError.objects.count(), 1)
        blad = ValidationError.objects.first()
        self.assertIn("-99.0", blad.error_details)