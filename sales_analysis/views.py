from django.http import JsonResponse
from .models import SalesRecord
from .llm_integration import get_individual_insight, get_team_insight,get_performance_trends_insight
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

def performance_dashboard(request):
    employees = SalesRecord.objects.values('employee_id', 'employee_name').distinct()
    return render(request, 'performance.html', {'employees': employees})


@api_view(['GET'])
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


@api_view(['GET'])
def team_performance_view(request, team_name=None):
    try:
        print(f"Team Name: {team_name}")  # Debugging print
        sales_data = SalesRecord.objects.all()

        if team_name:
            print(f"Filtering sales data for team: {team_name}")  # Debugging print
            sales_data = sales_data.filter(employee_name=team_name)

        if not sales_data.exists():
            print("No sales data found for the team.")  # Debugging print
            return JsonResponse({"error": "No data available for this team."}, status=404)

        insights = get_team_insight(sales_data)
        return JsonResponse({"team_insights": insights}, safe=False)

    except Exception as e:
        print(f"Error: {e}")  # Debugging print
        return JsonResponse({"error": str(e)}, status=500)
# /api/rep_performance
@api_view(['GET'])
def rep_performance_view(request, rep_id):
    # Replace 'dated' with 'created_at' or another valid date field
    sales_record = SalesRecord.objects.filter(employee_id=rep_id).latest('created_at')
    
    if not sales_record:
        return Response({"error": "Sales record not found"}, status=404)
    
    # Pass the latest record for LLM analysis
    insight = get_individual_insight(sales_record)
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
    time_period = request.GET.get('time_period', 'monthly')  # Default to 'monthly' if not provided
    
    # Assuming you need to fetch the sales_data from the database
    sales_data = SalesRecord.objects.all()  # Replace with any filtering logic you may need
    
    # Call the function with both sales_data and time_period
    insight = get_performance_trends_insight(sales_data, time_period)
    
    return JsonResponse(insight, safe=False)

