import os
from django.shortcuts import render, redirect  # <--- DODAJ redirect TUTAJ
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .tasks import process_dspace_file_task
from .models import SimulationSession, TrajectoryPoint, ValidationError

def index(request):
    if request.method == 'POST' and request.FILES.get('dspace_file'):
        uploaded_file = request.FILES['dspace_file']
        
        fs = FileSystemStorage()
        
        # 1. Sprawdzamy, czy plik o takiej nazwie już fizycznie istnieje na dysku
        if fs.exists(uploaded_file.name):
            fs.delete(uploaded_file.name) # 2. Jeśli tak, usuwamy starą wersję
            
        # 3. Zapisujemy nowy plik (teraz nazwa zawsze będzie czysta!)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        process_dspace_file_task.delay(file_path)
        
        messages.success(request, f"Plik '{filename}' został przyjęty. Trwa asynchroniczny import w tle.")
        
        # --- KLUCZOWA ZMIANA ---
        # Zamiast renderować stronę z "bagażem" formularza, zmuszamy przeglądarkę 
        # do załadowania strony od nowa jako czyste wejście.
        return redirect('/') 

    # Wyciągamy statystyki
    context = {
        'total_sessions': SimulationSession.objects.count(),
        'total_points': TrajectoryPoint.objects.count(),
        'total_errors': ValidationError.objects.count(),
    }
    
    return render(request, 'core/index.html', context)