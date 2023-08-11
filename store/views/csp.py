# views.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class CSPReportView(View):
    def post(self, request, *args, **kwargs):
        try:
            report_data = json.loads(request.body.decode('utf-8'))
            # Log the report data
            print(report_data)
        except json.JSONDecodeError:
            # Invalid JSON, you might want to log this too
            pass
        return JsonResponse({'status': 'ok'})
