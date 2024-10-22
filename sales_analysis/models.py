from django.db import models

class SalesRecord(models.Model):
    employee_id = models.IntegerField()
    employee_name = models.CharField(max_length=255)
    lead_taken = models.IntegerField()
    tours_booked = models.IntegerField()
    applications = models.IntegerField()
    apps_per_lead = models.FloatField()
    tours_per_lead = models.FloatField()
    apps_per_tour = models.FloatField()
    created_at = models.DateTimeField(null=True, blank=True)  # stores the 'dated' from CSV
    
    mon_text = models.IntegerField()
    tue_text = models.IntegerField()
    wed_text = models.IntegerField()
    thur_text = models.IntegerField()
    fri_text = models.IntegerField()
    sat_text = models.IntegerField()
    sun_text = models.IntegerField()
    
    mon_call = models.IntegerField()
    tue_call = models.IntegerField()
    wed_call = models.IntegerField()
    thur_call = models.IntegerField()
    fri_call = models.IntegerField()
    sat_call = models.IntegerField()
    sun_call = models.IntegerField()

    class Meta:
        unique_together = ('employee_name', 'created_at')  # ensures name + date uniqueness
    
    def __str__(self):
        return f"{self.employee_name} - {self.created_at}"
