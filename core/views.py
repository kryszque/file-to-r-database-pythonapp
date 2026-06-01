from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .tasks import process_dspace_file_task
from .models import SimulationSession, TrajectoryPoint, ValidationError
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import SimulationSession

def index(request):
    if request.method == 'POST' and request.FILES.get('dspace_file'):
        uploaded_file = request.FILES['dspace_file']
        
        fs = FileSystemStorage()
        
        if fs.exists(uploaded_file.name):
            fs.delete(uploaded_file.name)
            
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        process_dspace_file_task.delay(file_path)
        
        messages.success(request, f"Plik '{filename}' został przyjęty. Trwa asynchroniczny import w tle.")
        
        return redirect('/') 

    context = {
        'total_sessions': SimulationSession.objects.count(),
        'total_points': TrajectoryPoint.objects.count(),
        'total_errors': ValidationError.objects.count(),
    }
    
    return render(request, 'core/index.html', context)

def import_report_list(request):
    sessions = SimulationSession.objects.annotate(
        points_count=Count('trajectorypoint', distinct=True),
        errors_count=Count('validationerror', distinct=True)
    ).order_by('-created_at')

    return render(request, 'core/report_list.html', {'sessions': sessions})

def import_report_detail(request, session_id):
    session = get_object_or_404(SimulationSession, id=session_id)
    
    stats = session.get_aggregated_stats()

    return render(request, 'core/report_detail.html', {
        'session': session,
        'stats': stats
    })