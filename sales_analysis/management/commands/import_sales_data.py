from django.core.management.base import BaseCommand
from sales_analysis.models import SalesRecord
import pandas as pd

class Command(BaseCommand):
    help = 'Import sales data from CSV'

    def handle(self, *args, **kwargs):
        # Load the CSV file
        csv_file = "sales_performance_data.csv"
        df = pd.read_csv(csv_file)
        
        # Loop through the CSV and create records
        sales_records = [
            SalesRecord(
                employee_id=row['employee_id'],
                employee_name=row['employee_name'],
                lead_taken=row['lead_taken'],
                tours_booked=row['tours_booked'],
                applications=row['applications'],
                apps_per_lead=row['apps_per_lead'],
                tours_per_lead=row['tours_per_lead'],
                apps_per_tour=row['apps_per_tour'],
                created_at=row['dated'],  # Map 'dated' field to 'created_at' field in the model
                mon_text=row['mon_text'],
                tue_text=row['tue_text'],
                wed_text=row['wed_text'],
                thur_text=row['thur_text'],
                fri_text=row['fri_text'],
                sat_text=row['sat_text'],
                sun_text=row['sun_text'],
                mon_call=row['mon_call'],
                tue_call=row['tue_call'],
                wed_call=row['wed_call'],
                thur_call=row['thur_call'],
                fri_call=row['fri_call'],
                sat_call=row['sat_call'],
                sun_call=row['sun_call'],
            )
            for index, row in df.iterrows()
        ]

        # Bulk create records (for efficiency)
        SalesRecord.objects.bulk_create(sales_records)

        self.stdout.write(self.style.SUCCESS('Sales data imported successfully!'))
