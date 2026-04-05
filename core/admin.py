from django.contrib import admin
from .models import SimulationSession,SystemSetting, SimulationResult, ValidationError

# rejestracja sesji
@admin.register(SimulationSession)
class SimulationSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_path', 'created_at')

# rejestracja ustawien ukladu
@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('setting_name', 'setting_value', 'session')

# rejestracja wynikow
@admin.register(SimulationResult)
class SimulationResultAdmin(admin.ModelAdmin):
    list_display = ('original_file', 'parameter', 'value', 'sim_time', 'session')
    list_filter = ('parameter', 'session')

# rejestracja bledow
@admin.register(ValidationError)
class ValidationErrorAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'error_details', 'session')