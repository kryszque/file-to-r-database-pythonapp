from django.db import models

# grupa danych z jednego importu
class SimulationSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    source_path = models.CharField(max_length=500, db_index=True)

# parametry ustawione przed symulacja
class SystemSetting(models.Model):
    session = models.ForeignKey(SimulationSession, on_delete=models.CASCADE)
    setting_name = models.CharField(max_length=100, db_index=True)
    setting_value = models.CharField(max_length=255, db_index=True)

# glowne dane liczbowe
class SimulationResult(models.Model):
    session = models.ForeignKey(SimulationSession, on_delete=models.CASCADE)
    # nazwa pliku z ktorego pochodzi ten konkretny wiersz
    original_file = models.CharField(max_length=255, db_index=True)
    parameter = models.CharField(max_length=100, db_index=True)
    value = models.FloatField(db_index=True)
    sim_time = models.FloatField(db_index=True)

# obsluga blednych danych
class ValidationError(models.Model):
    session = models.ForeignKey(SimulationSession, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, db_index=True)
    error_details = models.TextField(db_index=True)