from django.contrib import admin
from .models import SimulationSession, TrajectoryPoint, ValidationError

# rejestracja sesji
@admin.register(SimulationSession)
class SimulationSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_path', 'created_at')
    search_fields = ('source_path',) 

# rejestracja punktów trajektorii
@admin.register(TrajectoryPoint)
class TrajectoryPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'sim_time', 'pos_x', 'pos_y', 'pos_z', 'session')
    
    list_filter = ('session',)
    
    ordering = ('id', 'session')

# rejestracja bledow
@admin.register(ValidationError)
class ValidationErrorAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'error_details', 'session')
    search_fields = ('file_name', 'error_details')
    list_filter = ('session',)