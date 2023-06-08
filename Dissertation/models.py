from django.db import models

class IpList(models.Model):
    ipList = models.CharField("First name", max_length=255, blank = True, null = True)
    hostname = models.CharField("First name", max_length=255, blank = True, null = True)
    ios = models.CharField("First name", max_length=255, blank = True, null = True)
    device_type = models.CharField("First name", max_length=255, blank = True, null = True)


    def __str__(self):
        return self.hostname
