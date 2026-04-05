from django.shortcuts import render
from .forms import DirectoryImportForm

def index(request):
    form = DirectoryImportForm()
    return render(request, 'core/index.html', {'form': form})