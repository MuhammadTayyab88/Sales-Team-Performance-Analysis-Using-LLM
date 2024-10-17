import csv
from django.core.management.base import BaseCommand
from sales_analysis.models import SalesRecord

class Command(BaseCommand):
    help = 'Imports sales data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            sales_records = [
                SalesRecord(
                    employee_id=row['employee_id'],
                    employee_name=row['employee_name'],
                    created=row['created'],
                    dated=row['dated'],
                    lead_taken=row['lead_taken'],
                    tours_booked=row['tours_booked'],
                    applications=row['applications'],
                    tours_per_lead=row['tours_per_lead'],
                    apps_per_tour=row['apps_per_tour'],
                    apps_per_lead=row['apps_per_lead'],
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
                    sun_call=row['sun_call']
                )
                for row in reader
            ]
            SalesRecord.objects.bulk_create(sales_records)
            self.stdout.write(self.style.SUCCESS('Successfully imported data from CSV'))
            
