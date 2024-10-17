from django.db import models

class SalesRecord(models.Model):
    employee_id = models.IntegerField()
    employee_name = models.CharField(max_length=100)
    created = models.DateTimeField()
    dated = models.DateField()
    lead_taken = models.IntegerField()
    tours_booked = models.IntegerField()
    applications = models.IntegerField()
    tours_per_lead = models.FloatField()
    apps_per_tour = models.FloatField()
    apps_per_lead = models.FloatField()
    
    # Daily text messages count
    mon_text = models.IntegerField()
    tue_text = models.IntegerField()
    wed_text = models.IntegerField()
    thur_text = models.IntegerField()
    fri_text = models.IntegerField()
    sat_text = models.IntegerField()
    sun_text = models.IntegerField()
    
    # Daily call count
    mon_call = models.IntegerField()
    tue_call = models.IntegerField()
    wed_call = models.IntegerField()
    thur_call = models.IntegerField()
    fri_call = models.IntegerField()
    sat_call = models.IntegerField()
    sun_call = models.IntegerField()

    def __str__(self):
        return f"{self.employee_name} ({self.employee_id})"
