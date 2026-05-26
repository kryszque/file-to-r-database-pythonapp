from .models import SimulationSession, SystemSetting, SimulationResult, ValidationError

def save_import_to_db(file_path, valid_rows, invalid_rows, settings_dict=None):
    sim_ses = SimulationSession.objects.create(source_path=file_path)
    results_to_insert = []
    errors_to_insert = []

    if settings_dict:
        settings_to_insert = []
        for s_name, s_val in settings_dict.items():
            setting_obj = SystemSetting(
                session=sim_ses,
                setting_name=s_name,
                setting_value=str(s_val)
            )
            settings_to_insert.append(setting_obj)
        
        if settings_to_insert:
            SystemSetting.objects.bulk_create(settings_to_insert)

    for row in valid_rows:
        sim_time = row['time']
        
        for param_name, param_value in row['value'].items():
            
            sim_result = SimulationResult(
                session=sim_ses,              
                parameter=param_name,    
                value=param_value,           
                sim_time=sim_time,
                original_file=file_path                
            )
            results_to_insert.append(sim_result)
    
    for err_dict in invalid_rows:
        
        error_obj = ValidationError(
            session=sim_ses,
            error_details=err_dict['szczegoly_bledu'],
            file_name=file_path,
            raw_data=err_dict['oryginalne_dane']       
        )
        errors_to_insert.append(error_obj)
    
    if results_to_insert:
        SimulationResult.objects.bulk_create(results_to_insert, batch_size=1000)
        
    if errors_to_insert:
        ValidationError.objects.bulk_create(errors_to_insert, batch_size=1000)