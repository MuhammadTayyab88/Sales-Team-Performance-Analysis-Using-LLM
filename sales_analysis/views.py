from django.http import JsonResponse
from .models import SalesRecord
from .llm_integration import get_individual_insight, get_team_insight, get_performance_trends_insight
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.utils.dateparse import parse_date
import json
import logging
from django.utils.dateformat import DateFormat


logger = logging.getLogger(__name__)

# Performance Dashboard View - lists all employees
def performance_dashboard(request):
    employees = SalesRecord.objects.values('employee_id', 'employee_name').distinct()
    return render(request, 'performance.html', {'employees': employees})


# Individual Performance View - lists available dates for an employee and retrieves insights for the selected date
@api_view(['GET'])
def individual_performance_view(request, employee_name):
    try:
        # Fetch all records for the selected employee
        sales_records = SalesRecord.objects.filter(employee_name=employee_name)

        if not sales_records.exists():
            return JsonResponse({"error": "No sales data found for this employee."}, status=404)

        # Fetch all distinct dates for the employee
        available_dates = sales_records.values_list('created_at__date', flat=True).distinct()

        # Convert dates to string format (if necessary)
        available_dates = [date.strftime('%Y-%m-%d') for date in available_dates if date]

        selected_date = request.GET.get('selected_date')

        if selected_date:
            selected_date = parse_date(selected_date)
            if not selected_date:
                return JsonResponse({"error": "Invalid date."}, status=400)

            # Ensure the selected date is in the available dates
            if str(selected_date) not in available_dates:
                return JsonResponse({"error": "Unavailable date."}, status=400)

            # Fetch performance insights for the selected date
            insights = get_individual_insight(employee_name, selected_date)
            return JsonResponse({"insights": json.loads(insights)})

        # If no date is selected, return the list of available dates for the employee
        return JsonResponse({"available_dates": available_dates})

    except Exception as e:
        logger.error(f"Error in fetching individual performance: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


# Team Performance View - fetches insights for all records of a team (considering employee_name as the team name)
@api_view(['GET'])
def team_performance_view(request):
    try:
        # Get the team name from the request query parameters
        team_name = request.GET.get('team_name')

        if not team_name:
            return JsonResponse({"error": "Missing 'team_name' parameter."}, status=400)

        # Fetch all sales data for the selected team (employee_name is treated as the team name)
        sales_data = SalesRecord.objects.filter(employee_name=team_name)

        if not sales_data.exists():
            return JsonResponse({"error": "No data available for this team."}, status=404)

        # Get the aggregated team insights
        insights = get_team_insight(team_name)  # Assuming this returns a dictionary
        return JsonResponse({"team_insights": insights})

    except Exception as e:
        logger.error(f"Error in fetching team performance: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

# Monthly Performance Trends View - fetches performance trends for a selected month or a date range
@api_view(['GET'])
def performance_trends_view(request):
    selected_month = request.GET.get('selected_month')  # Expected in 'YYYY-MM' format
    from_date = request.GET.get('from_date')  # Expected in 'YYYY-MM-DD' format
    to_date = request.GET.get('to_date')  # Expected in 'YYYY-MM-DD' format

    # Validate the selected_month or date range
    if selected_month:
        try:
            # Parse the selected month from 'YYYY-MM' format
            selected_month = parse_date(f"{selected_month}-01")
        except ValueError:
            return JsonResponse({"error": "Invalid 'selected_month' format. Expected 'YYYY-MM'."}, status=400)

    elif from_date and to_date:
        try:
            from_date = parse_date(from_date)
            to_date = parse_date(to_date)

            # Validate that 'from_date' is before or equal to 'to_date'
            if from_date > to_date:
                return JsonResponse({"error": "'from_date' cannot be later than 'to_date'."}, status=400)

        except ValueError:
            return JsonResponse({"error": "Invalid date range. Expected 'YYYY-MM-DD' format."}, status=400)
    else:
        return JsonResponse({"error": "Either 'selected_month' or 'from_date' and 'to_date' must be provided."}, status=400)

    try:
        # Fetch performance insights based on month or date range
        insights = get_performance_trends_insight(selected_month, from_date, to_date)
        return JsonResponse(json.loads(insights))

    except Exception as e:
        logger.error(f"Error in fetching performance trends: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

