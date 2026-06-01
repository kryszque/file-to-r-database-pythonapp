from celery import shared_task
from .parsers import parse_mat_dspace
from .validators import validate_dataframe
from .services import save_import_to_db

@shared_task
def process_dspace_file_task(file_path):
    """
    To jest zadanie dla Celery. Działa w tle (niewidocznie dla użytkownika).
    """
    print(f"[CELERY] Rozpoczynam import z pliku: {file_path}")
    
    df = parse_mat_dspace(file_path)
    if df.empty:
        return f"BŁĄD: Pusty plik lub błąd parsera: {file_path}"
    
    poprawne, bledne = validate_dataframe(df)
    
    save_import_to_db(file_path, poprawne, bledne)
    
    msg = f"SUKCES: Zapisano {len(poprawne)} punktów trajektorii. Odrzucono: {len(bledne)}"
    print(f"[CELERY] {msg}")
    
    return msg