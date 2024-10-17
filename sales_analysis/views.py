from django.http import JsonResponse
from .models import SalesRecord
from .llm_integration import get_individual_insight, get_team_insight,get_performance_trends_insight
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Sales Performance Analysis API")


def individual_performance_view(request, employee_id):
    try:
        sales_record = SalesRecord.objects.filter(employee_id=employee_id)
        if not sales_record.exists():
            return JsonResponse({"error": "Sales record not found"}, status=404)

        # Assuming you want the latest data for the employee
        employee_data = sales_record.latest('dated')
        insights = get_individual_insight(employee_data)
        return JsonResponse({"insights": insights})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def team_performance_view(request):
    try:
        sales_data = SalesRecord.objects.all()
        insights = get_team_insight(sales_data)
        return JsonResponse({"team_insights": insights})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
# /api/rep_performance
@api_view(['GET'])
def rep_performance_view(request, rep_id):
    sales_record = SalesRecord.objects.filter(employee_id=rep_id)
    if not sales_record.exists():
        return Response({"error": "Sales record not found"}, status=404)
    # Pass the latest record for LLM analysis
    rep_data = sales_record.latest('dated')
    insight = get_individual_insight(rep_data)
    return Response({"insight": insight})
# /api/team_performance
@api_view(['GET'])
def team_performance_view(request):
    sales_data = SalesRecord.objects.all()
    insight = get_team_insight(sales_data)
    return Response({"team_insight": insight})

# /api/performance_trends
@api_view(['GET'])
def performance_trends_view(request):
    time_period = request.query_params.get('time_period', 'monthly')
    # Customize trend analysis based on time_period
    insight = get_performance_trends_insight(time_period)
    return Response({"trend_insight": insight})
