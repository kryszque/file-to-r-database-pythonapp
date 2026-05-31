from django.contrib import admin
from .models import SimulationSession, TrajectoryPoint, ValidationError

# rejestracja sesji
@admin.register(SimulationSession)
class SimulationSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_path', 'created_at')
    search_fields = ('source_path',) # Pozwala szukać po nazwie pliku

# rejestracja punktów trajektorii (poprawiona!)
@admin.register(TrajectoryPoint)
class TrajectoryPointAdmin(admin.ModelAdmin):
    # Pokazujemy faktyczne kolumny z nowego modelu TrajectoryPoint
    list_display = ('sim_time', 'pos_x', 'pos_y', 'pos_z', 'session')
    
    # Dodajemy panel boczny do filtrowania po sesjach (kluczowe przy wielu plikach!)
    list_filter = ('session',)
    
    # Domyślne sortowanie - najpierw sesja, potem czas rosnąco
    ordering = ('session', 'sim_time')

# rejestracja bledow
@admin.register(ValidationError)
class ValidationErrorAdmin(admin.ModelAdmin):
    # Dodałem 'id' oraz wyświetlanie błędów
    list_display = ('id', 'file_name', 'error_details', 'session')
    search_fields = ('file_name', 'error_details') # Szukajka błędów
    list_filter = ('session',)