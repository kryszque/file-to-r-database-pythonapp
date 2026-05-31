from .models import SimulationSession, TrajectoryPoint, ValidationError

def save_import_to_db(file_path, valid_rows, invalid_rows):
    """
    Zapisuje poprawne punkty trajektorii i błędy do bazy danych za pomocą mechanizmu bulk_create.
    """
    # 1. Tworzymy główną sesję dla tego importu
    sim_ses = SimulationSession.objects.create(source_path=file_path)
    
    # 2. Pakowanie czystych danych w obiekty Django (w pamięci RAM)
    points_to_insert = [
        TrajectoryPoint(
            session=sim_ses,
            sim_time=row['time'],
            pos_x=row['x'],
            pos_y=row['y'],
            pos_z=row['z']
        )
        for row in valid_rows
    ]
    
    # 3. Pakowanie logów z błędami w obiekty Django (w pamięci RAM)
    errors_to_insert = [
        ValidationError(
            session=sim_ses,
            file_name=file_path,
            error_details=err_dict['szczegoly_bledu'],
            raw_data=err_dict['oryginalne_dane']
        )
        for err_dict in invalid_rows
    ]
    
    # 4. Wykonanie paczkowego zapisu do bazy danych (Bulk Insert)
    # Zwiększamy batch_size do 5000, bo model jest teraz bardzo "lekki"
    if points_to_insert:
        TrajectoryPoint.objects.bulk_create(points_to_insert, batch_size=5000)
        
    if errors_to_insert:
        ValidationError.objects.bulk_create(errors_to_insert, batch_size=1000)