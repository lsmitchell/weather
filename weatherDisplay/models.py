from django.db import models

class Weather(models.Model):
    temp_f = models.TextField(blank=True, default="")
    condition = models.TextField(blank=True, default="")
    err = models.TextField(blank=True, default="")

    def __str__(self):
        return str(self.temp_f) + " " + self.condition

    def __init__(self, temp_f='', condition='', err=''):
        super(Weather, self).__init__()
        self.temp_f = temp_f
        self.condition = condition
        self.err = err