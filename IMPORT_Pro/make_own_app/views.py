from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from tablib import Dataset
from .resources import *

from .models import Person

def Simple_Upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']
        imported_data = dataset.load(new_persons.read().decode('utf-8'), format='csv')
        result = person_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)
    return render(request, 'import.html')





def File_Export(request):
    person_resource = PersonResource()
    dataset = person_resource.export()


    #  For the JSON Exporting File
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="persons.json"'

    #  For the XLS Exporting File
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'

    #  For the CSV Exporting File
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'


    return response



# For the Filtering OF The Data we USe Bascially

def Data_Set_Filter(request):
    person_resource = PersonResource()
    queryset = Person.objects.filter(location='Jyväskyla')
    dataset = person_resource.export(queryset)
    print(dataset)
    return render(request, 'import.html')
    # HttpResponse(dataset.yaml)