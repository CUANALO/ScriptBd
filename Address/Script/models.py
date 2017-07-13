from django.db import models

# Create your models here.
class IndexAddress(models.Model):
    city = models.CharField(db_column='City', max_length=100, blank=True, null=True)  # Field name made lowercase.
    code_oag = models.CharField(db_column='Code_oag', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=200, blank=True, null=True)  # Field name made lowercase.
    zip_code = models.CharField(db_column='Zip_code', max_length=35, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=4, blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(db_column='Latitude', max_length=20, blank=True, null=True)  # Field name made lowercase.
    longitude = models.CharField(db_column='Longitude', max_length=20, blank=True, null=True)  # Field name made lowercase.
    operation_time = models.CharField(db_column='Operation_Time', max_length=50, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=20, blank=True, null=True)  # Field name made lowercase.
