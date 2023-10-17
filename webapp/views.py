from django.shortcuts import render
from .logic import initialize_qa, process_query
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.management import call_command
import os
from ingest.loader import run_ingestion


def home(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        qa = initialize_qa()  # Initialize the 'qa' variable
        result = process_query(qa, query)  # Pass 'qa' as an argument to process_query
        return render(request, 'home.html', {'result': result})

    return render(request, 'home.html')

def initialize(request):
    qa = initialize_qa()
    return render(request, 'home.html')

def ingest_documents(request):
    if request.method == 'POST':
        # Process the uploaded files
        files = request.FILES.getlist('documents')
        for file in files:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'source_documents', file.name)

            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

       # Perform the document ingestion process
        run_ingestion()

        return HttpResponseRedirect(reverse('home'))

    return render(request, 'ingest_documents.html')
