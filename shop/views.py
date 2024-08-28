# storedata/views.py

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Report
from .task import generate_report

def trigger_report(request):
    print("hit here")
    if request.method == 'POST':
        report_id = generate_report.delay()
        return JsonResponse({'report_id': report_id})
    else :
            return JsonResponse({'error': 'Invalid method'}, status=405)

def get_report(request, report_id):
    report = get_object_or_404(Report, report_id=report_id)

    if report.status == 'Running':
        return JsonResponse({'status': 'Running'})

    response = HttpResponse(report.csv_file, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={report.csv_file.name}'
    return response
