from django.db import models

class temp_table(models.Model):
    EmpID = models.IntegerField(primary_key=True)
    Biorefno = models.CharField(max_length=12, null=True, blank=True)
    Plantcode = models.CharField(max_length=10, null=True, blank=True)
    Attndt = models.DateTimeField()
    Shiftcode = models.CharField(max_length=5)
    Earlystart = models.DateTimeField(null=True, blank=True)
    Shiftstart = models.DateTimeField(null=True, blank=True)
    Chkin = models.DateTimeField(null=True, blank=True)
    Attn = models.CharField(max_length=5, default='AB')
    La = models.IntegerField(default=0)
    Lastout = models.DateTimeField(null=True, blank=True)
    Logcount = models.IntegerField(default=0)
    Status = models.CharField(max_length=3, default='AB')
    Shiftend = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'temp_table'      


