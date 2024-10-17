import openai
from django.conf import settings

# Set up OpenAI API key from Django settings
openai.api_key = settings.OPENAI_API_KEY

def preprocess_data(sales_data):
    """
    Preprocess sales data and format it for LLM input.
    """
    processed_data = []
    for record in sales_data:
        processed_data.append(
            f"Employee ID: {record.employee_id}, Name: {record.employee_name}, "
            f"Leads Taken: {record.lead_taken}, Tours Booked: {record.tours_booked}, "
            f"Applications: {record.applications}, Apps per Lead: {record.apps_per_lead}, "
            f"Tours per Lead: {record.tours_per_lead}, Apps per Tour: {record.apps_per_tour}"
        )
    return "\n".join(processed_data)

def get_individual_insight(employee_data):
    """
    Generate insights for an individual sales representative using specific metrics.
    """
    # Preparing the prompt with all sales and communication metrics
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
    
    # Call to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Replace with "gpt-4" if that's the correct model for your account
        messages=[
            {"role": "system", "content": "You are an expert sales analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000  # Adjust based on required response length
    )
    return response['choices'][0]['message']['content'].strip()

def get_team_insight(sales_data):
    """
    Query the LLM for overall team performance insights, using summarized data.
    """
    # Preprocess the data to include in the prompt
    processed_data = preprocess_data(sales_data)
    prompt = (
        f"Analyze the following team sales data:\n\n{processed_data}\n\n"
        "Provide a summary of team performance, observable trends, and any areas for improvement."
    )

    # Call to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert sales analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000  # Adjust based on required response length
    )
    return response['choices'][0]['message']['content'].strip()

def get_performance_trends_insight(time_period):
    """
    Query the LLM for sales performance trends over a specified time period.
    """
    prompt = (
        f"Analyze sales trends over the {time_period} period, considering factors like leads, bookings, and conversions. "
        "Provide insights on trends and suggestions for performance improvements."
    )
    
    # Call to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert sales analyst."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000  # Adjust based on required response length
    )
    return response['choices'][0]['message']['content'].strip()
