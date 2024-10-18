import openai
from django.conf import settings
from django.utils import timezone
import calendar
from django.db.models import Sum
# Set up OpenAI API key from Django settings
openai.api_key = settings.OPENAI_API_KEY

def preprocess_data(sales_data):
    """
    Preprocess the team sales data to format it for LLM input.
    """
    processed_data = []
    for record in sales_data:
        if record.created_at:  # Skip records where 'created_at' is None
            processed_data.append(
                f"Employee ID: {record.employee_id}, Name: {record.employee_name}, "
                f"Leads Taken: {record.lead_taken}, Tours Booked: {record.tours_booked}, "
                f"Applications: {record.applications}, Apps per Lead: {record.apps_per_lead}, "
                f"Tours per Lead: {record.tours_per_lead}, Apps per Tour: {record.apps_per_tour}, "
                f"Month: {calendar.month_name[record.created_at.month]}"
            )
        else:
            print(f"Skipping record {record.id} due to missing created_at")

def get_individual_insight(employee_data):
    prompt = (
        f"Analyze the following sales data for sales representative {employee_data.employee_name}:\n\n"
        f"- Total Leads Taken: {employee_data.lead_taken}\n"
        f"- Tours Booked: {employee_data.tours_booked}\n"
        f"- Applications: {employee_data.applications}\n"
        f"- Tours per Lead: {employee_data.tours_per_lead}\n"
        f"- Apps per Tour: {employee_data.apps_per_tour}\n"
        f"- Apps per Lead: {employee_data.apps_per_lead}\n\n"
        f"Additionally, here are weekly communications data:\n"
        f"- Text Messages Sent: Mon: {employee_data.mon_text}, Tue: {employee_data.tue_text}, "
        f"Wed: {employee_data.wed_text}, Thu: {employee_data.thur_text}, Fri: {employee_data.fri_text}, "
        f"Sat: {employee_data.sat_text}, Sun: {employee_data.sun_text}\n"
        f"- Calls Made: Mon: {employee_data.mon_call}, Tue: {employee_data.tue_call}, "
        f"Wed: {employee_data.wed_call}, Thu: {employee_data.thur_call}, Fri: {employee_data.fri_call}, "
        f"Sat: {employee_data.sat_call}, Sun: {employee_data.sun_call}\n\n"
        "Based on this data, provide detailed feedback on performance and actionable insights for improvement."
    )
    
    # Call to OpenAI API for feedback
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert sales analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    
    return {
        "Analyze the following sales data for sales representative": employee_data.employee_name,
        "total_lead_taken": employee_data.lead_taken,
        "Tours_Booked": employee_data.tours_booked,
        "Applications": employee_data.applications,
        "Tours_per_Lead": employee_data.tours_per_lead,
        "Apps_per_Tour": employee_data.apps_per_tour,
        "Apps_per_Lead": employee_data.apps_per_lead,
        "Text_Messages_Sent": {
            "Mon": employee_data.mon_text,
            "Tue": employee_data.tue_text,
            "Wed": employee_data.wed_text,
            "Thu": employee_data.thur_text,
            "Fri": employee_data.fri_text,
            "Sat": employee_data.sat_text,
            "Sun": employee_data.sun_text
        },
        "Calls_Made": {
            "Mon": employee_data.mon_call,
            "Tue": employee_data.tue_call,
            "Wed": employee_data.wed_call,
            "Thu": employee_data.thur_call,
            "Fri": employee_data.fri_call,
            "Sat": employee_data.sat_call,
            "Sun": employee_data.sun_call
        },
        # "LLM Feedback": response['choices'][0]['message']['content'].strip()
    }





def get_team_insight(sales_data):
    """
    Generate insights for team performance using key metrics.
    """

    # Aggregating team performance data by summing the values
    total_leads_taken = sum([record.lead_taken for record in sales_data])
    total_tours_booked = sum([record.tours_booked for record in sales_data])
    total_applications = sum([record.applications for record in sales_data])

    # Calculate conversion ratios
    tours_per_lead = total_tours_booked / total_leads_taken if total_leads_taken > 0 else 0
    apps_per_tour = total_applications / total_tours_booked if total_tours_booked > 0 else 0
    apps_per_lead = total_applications / total_leads_taken if total_leads_taken > 0 else 0

    # Communication data aggregation (per day of the week)
    total_text_messages_sent = {
        "Mon": sum([record.mon_text for record in sales_data]),
        "Tue": sum([record.tue_text for record in sales_data]),
        "Wed": sum([record.wed_text for record in sales_data]),
        "Thu": sum([record.thur_text for record in sales_data]),
        "Fri": sum([record.fri_text for record in sales_data]),
        "Sat": sum([record.sat_text for record in sales_data]),
        "Sun": sum([record.sun_text for record in sales_data]),
    }

    total_calls_made = {
        "Mon": sum([record.mon_call for record in sales_data]),
        "Tue": sum([record.tue_call for record in sales_data]),
        "Wed": sum([record.wed_call for record in sales_data]),
        "Thu": sum([record.thur_call for record in sales_data]),
        "Fri": sum([record.fri_call for record in sales_data]),
        "Sat": sum([record.sat_call for record in sales_data]),
        "Sun": sum([record.sun_call for record in sales_data]),
    }

    # Return the insights in a JSON-friendly format
    return {
        "total_leads_taken": total_leads_taken,
        "total_tours_booked": total_tours_booked,
        "total_applications": total_applications,
        "conversion_ratios": {
            "tours_per_lead": tours_per_lead,
            "apps_per_tour": apps_per_tour,
            "apps_per_lead": apps_per_lead,
        },
        "total_text_messages_sent": total_text_messages_sent,
        "total_calls_made": total_calls_made,
        "team_performance_summary": "Team performance analysis completed."  # Modify or use GPT-based insights here
    }

def get_performance_trends_insight(sales_data, time_period):
    """
    Generate insights for sales performance trends over a specified time period using LLM.
    """
    # Group sales data by month
    monthly_data = {}
    for record in sales_data:
        # Use the current date if 'created_at' is None
        created_at = record.created_at or timezone.now()
        month = created_at.strftime('%Y-%m')  # Example: '2024-10'
        
        if month not in monthly_data:
            monthly_data[month] = {
                'leads': 0,
                'tours': 0,
                'applications': 0,
            }
        monthly_data[month]['leads'] += record.lead_taken
        monthly_data[month]['tours'] += record.tours_booked
        monthly_data[month]['applications'] += record.applications
    
    # Create a summary prompt for each month
    monthly_summary = ""
    for month, data in monthly_data.items():
        monthly_summary += (
            f"Month: {month}, Leads Taken: {data['leads']}, "
            f"Tours Booked: {data['tours']}, Applications: {data['applications']}\n"
        )
    
    prompt = (
        f"Analyze sales trends over the {time_period} period based on the following monthly data:\n\n"
        f"{monthly_summary}\n"
        "Provide insights on trends, any noticeable improvements or declines, and suggestions for improvement."
    )

    # Call to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert sales analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    # Return JSON response for performance trends
    return {
        "performance_trends_summary": response['choices'][0]['message']['content'].strip(),
        "monthly_data": monthly_data  # Include raw monthly data as well in the response
    }