from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.management import call_command
import os


def ingest_documents(request):
    if request.method == 'POST':
        # Process the uploaded files
        files = request.FILES.getlist('documents')
        for file in files:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'source_documents', file.name)

            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # Perform any further processing or actions
        # ...

        return HttpResponseRedirect(reverse('home'))

    return render(request, 'ingest_documents.html')