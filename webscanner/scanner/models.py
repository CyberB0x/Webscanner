# scanner/models.py
from django.db import models

class Target(models.Model):
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    report = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.url

class Vulnerability(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    vuln_type = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
