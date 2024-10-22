import openai
from django.conf import settings
import json
from django.db.models import Sum
from sales_analysis.models import SalesRecord
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from rest_framework.decorators import api_view
import logging

logger = logging.getLogger(__name__)

# Ensure OpenAI API key is set from Django settings
openai.api_key = settings.OPENAI_API_KEY

def get_individual_insight(employee_name, selected_date=None):
    """
    Retrieve and return performance data for an individual employee.
    If a date is provided, data for that specific date will be retrieved.
    """

    # Ensure `employee_name` and `selected_date` are passed in correctly
    if not employee_name:
        raise ValueError("employee_name is required")
    
    # Query database for performance data based on employee_name and selected_date
    if selected_date:
        performance_data = SalesRecord.objects.filter(employee_name=employee_name, created_at__date=selected_date)
    else:
        performance_data = SalesRecord.objects.filter(employee_name=employee_name)

    # Ensure there's performance data for this employee and date
    if not performance_data.exists():
        return json.dumps({"error": "No performance data found for the selected employee and date."})

    # Aggregate individual performance data
    individual_performance = performance_data.aggregate(
        total_leads_taken=Sum('lead_taken'),
        total_tours_booked=Sum('tours_booked'),
        total_applications=Sum('applications'),
        total_mon_text=Sum('mon_text'),
        total_tue_text=Sum('tue_text'),
        total_wed_text=Sum('wed_text'),
        total_thur_text=Sum('thur_text'),
        total_fri_text=Sum('fri_text'),
        total_sat_text=Sum('sat_text'),
        total_sun_text=Sum('sun_text'),
        total_mon_call=Sum('mon_call'),
        total_tue_call=Sum('tue_call'),
        total_wed_call=Sum('wed_call'),
        total_thur_call=Sum('thur_call'),
        total_fri_call=Sum('fri_call'),
        total_sat_call=Sum('sat_call'),
        total_sun_call=Sum('sun_call'),
    )

    # Formulate prompt for OpenAI based on performance data
    prompt = (
        f"Strictly analyze the sales data for employee {employee_name} on the selected date {selected_date}:\n\n"
        f"- Total Leads Taken: {individual_performance['total_leads_taken']}\n"
        f"- Tours Booked: {individual_performance['total_tours_booked']}\n"
        f"- Applications: {individual_performance['total_applications']}\n"
        f"- Weekly Text Messages: Mon: {individual_performance['total_mon_text']}, Tue: {individual_performance['total_tue_text']}, "
        f"Wed: {individual_performance['total_wed_text']}, Thu: {individual_performance['total_thur_text']}, "
        f"Fri: {individual_performance['total_fri_text']}, Sat: {individual_performance['total_sat_text']}, "
        f"Sun: {individual_performance['total_sun_text']}\n"
        f"- Weekly Calls Made: Mon: {individual_performance['total_mon_call']}, Tue: {individual_performance['total_tue_call']}, "
        f"Wed: {individual_performance['total_wed_call']}, Thu: {individual_performance['total_thur_call']}, "
        f"Fri: {individual_performance['total_fri_call']}, Sat: {individual_performance['total_sat_call']}, "
        f"Sun: {individual_performance['total_sun_call']}\n\n"
        "Strictly provide performance insights and areas of improvement based on this data."
    )

    # Call OpenAI API for feedback
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a strict sales analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    # Return the performance data and LLM feedback in JSON format
    result = {
        "employee_name": employee_name,
        "total_leads_taken": individual_performance['total_leads_taken'],
        "total_tours_booked": individual_performance['total_tours_booked'],
        "total_applications": individual_performance['total_applications'],
        "total_text_messages_sent": {
            "Mon": individual_performance['total_mon_text'],
            "Tue": individual_performance['total_tue_text'],
            "Wed": individual_performance['total_wed_text'],
            "Thu": individual_performance['total_thur_text'],
            "Fri": individual_performance['total_fri_text'],
            "Sat": individual_performance['total_sat_text'],
            "Sun": individual_performance['total_sun_text']
        },
        "total_calls_made": {
            "Mon": individual_performance['total_mon_call'],
            "Tue": individual_performance['total_tue_call'],
            "Wed": individual_performance['total_wed_call'],
            "Thu": individual_performance['total_thur_call'],
            "Fri": individual_performance['total_fri_call'],
            "Sat": individual_performance['total_sat_call'],
            "Sun": individual_performance['total_sun_call']
        },
        "LLM_feedback": response['choices'][0]['message']['content'].strip()
    }

    return json.dumps(result)  # Return as a JSON response

#team performance
def get_team_insight(team_name):
    # Query the database for all performance data for the selected team
    team_performance_data = SalesRecord.objects.filter(employee_name=team_name)

    # Aggregate team performance by summing up all values
    team_performance = team_performance_data.aggregate(
        total_leads_taken=Sum('lead_taken'),
        total_tours_booked=Sum('tours_booked'),
        total_applications=Sum('applications'),
        total_mon_text=Sum('mon_text'),
        total_tue_text=Sum('tue_text'),
        total_wed_text=Sum('wed_text'),
        total_thur_text=Sum('thur_text'),
        total_fri_text=Sum('fri_text'),
        total_sat_text=Sum('sat_text'),
        total_sun_text=Sum('sun_text'),
        total_mon_call=Sum('mon_call'),
        total_tue_call=Sum('tue_call'),
        total_wed_call=Sum('wed_call'),
        total_thur_call=Sum('thur_call'),
        total_fri_call=Sum('fri_call'),
        total_sat_call=Sum('sat_call'),
        total_sun_call=Sum('sun_call'),
    )

    # Calculate conversion ratios
    if team_performance['total_leads_taken'] > 0 and team_performance['total_tours_booked'] > 0:
        conversion_ratios = {
            'tours_per_lead': team_performance['total_tours_booked'] / team_performance['total_leads_taken'],
            'apps_per_tour': team_performance['total_applications'] / team_performance['total_tours_booked'],
            'apps_per_lead': team_performance['total_applications'] / team_performance['total_leads_taken']
        }
    else:
        conversion_ratios = {
            'tours_per_lead': 0,
            'apps_per_tour': 0,
            'apps_per_lead': 0
        }

    # Return all performance data
    return {
        "team_name": team_name,
        "total_leads_taken": team_performance['total_leads_taken'],
        "total_tours_booked": team_performance['total_tours_booked'],
        "total_applications": team_performance['total_applications'],
        "conversion_ratios": conversion_ratios,
        "total_text_messages_sent": {
            "Mon": team_performance['total_mon_text'],
            "Tue": team_performance['total_tue_text'],
            "Wed": team_performance['total_wed_text'],
            "Thu": team_performance['total_thur_text'],
            "Fri": team_performance['total_fri_text'],
            "Sat": team_performance['total_sat_text'],
            "Sun": team_performance['total_sun_text']
        },
        "total_calls_made": {
            "Mon": team_performance['total_mon_call'],
            "Tue": team_performance['total_tue_call'],
            "Wed": team_performance['total_wed_call'],
            "Thu": team_performance['total_thur_call'],
            "Fri": team_performance['total_fri_call'],
            "Sat": team_performance['total_sat_call'],
            "Sun": team_performance['total_sun_call']
        }
    }
    


#monthly performance
def get_performance_trends_insight(selected_month=None, from_date=None, to_date=None):
    """
    Retrieve and return performance trends for a selected month or date range.
    """
    # If a month is selected, filter by that month
    if selected_month:
        performance_data = SalesRecord.objects.filter(
            created_at__month=selected_month.month, created_at__year=selected_month.year)
    elif from_date and to_date:
        # If a date range is provided, filter by that range
        performance_data = SalesRecord.objects.filter(
            created_at__date__gte=from_date, created_at__date__lte=to_date)
    else:
        # Default to the current month if no input is provided
        current_month = timezone.now().month
        performance_data = SalesRecord.objects.filter(created_at__month=current_month)

    # Aggregate the performance data
    monthly_performance = performance_data.aggregate(
        total_leads_taken=Sum('lead_taken'),
        total_tours_booked=Sum('tours_booked'),
        total_applications=Sum('applications'),
        total_mon_text=Sum('mon_text'),
        total_tue_text=Sum('tue_text'),
        total_wed_text=Sum('wed_text'),
        total_thur_text=Sum('thur_text'),
        total_fri_text=Sum('fri_text'),
        total_sat_text=Sum('sat_text'),
        total_sun_text=Sum('sun_text'),
        total_mon_call=Sum('mon_call'),
        total_tue_call=Sum('tue_call'),
        total_wed_call=Sum('wed_call'),
        total_thur_call=Sum('thur_call'),
        total_fri_call=Sum('fri_call'),
        total_sat_call=Sum('sat_call'),
        total_sun_call=Sum('sun_call'),
    )

    # Prepare the response data
    result = {
        "performance_trends_summary": {
            "total_leads_taken": monthly_performance['total_leads_taken'],
            "total_tours_booked": monthly_performance['total_tours_booked'],
            "total_applications": monthly_performance['total_applications'],
            "total_text_messages_sent": {
                "Mon": monthly_performance['total_mon_text'],
                "Tue": monthly_performance['total_tue_text'],
                "Wed": monthly_performance['total_wed_text'],
                "Thu": monthly_performance['total_thur_text'],
                "Fri": monthly_performance['total_fri_text'],
                "Sat": monthly_performance['total_sat_text'],
                "Sun": monthly_performance['total_sun_text']
            },
            "total_calls_made": {
                "Mon": monthly_performance['total_mon_call'],
                "Tue": monthly_performance['total_tue_call'],
                "Wed": monthly_performance['total_wed_call'],
                "Thu": monthly_performance['total_thur_call'],
                "Fri": monthly_performance['total_fri_call'],
                "Sat": monthly_performance['total_sat_call'],
                "Sun": monthly_performance['total_sun_call']
            }
        }
    }

    return json.dumps(result)  # Return the result in JSON format
