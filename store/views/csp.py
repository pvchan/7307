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

            # Log the report data to a file
            with open('csp-reports.txt', 'a') as file:
                file.write(json.dumps(report_data) + '\n')

            # Optionally, you can also print the report data
            print(report_data)

        except json.JSONDecodeError:
            # Invalid JSON, log this too
            with open('csp-reports.txt', 'a') as file:
                file.write("JSON decoding error. Invalid JSON received.\n")

        return JsonResponse({'status': 'ok'})
