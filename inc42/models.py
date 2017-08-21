from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


class Company(models.Model):
    """
    model to save company information
    """
    profile_id = models.CharField(max_length=254, unique=True)  # Randomly generated profile id
    name = models.CharField(max_length=254, blank=True, null=True)  # Company name
    description = models.TextField(default="")  # Description about the company 
    logo = models.TextField(default="")  # Company's logo url
    founded_on = models.DateField(blank=True, null=True)  # Company's foundation date
    website = models.TextField(default="")  # company's  official website
    social_info = JSONField(default={})  # all social information, kept as json as new social platforms can come
    markets = ArrayField(models.CharField(max_length=254, blank=True, null=True), null=True, blank=True)

    # Below 3 fields are to keep additional information about the record
    is_deleted = models.BooleanField(default=False)  # to soft delete a company
    created_at = models.DateTimeField(auto_now_add=True)  # when this record was created
    modified_at = models.DateTimeField(auto_now=True)  # when this record was last modified


class Funding(models.Model):
    """
    model to save all company funding information
    """
    company = models.ForeignKey(Company, null=True, blank=True)  # company's foreign key
    amount = models.FloatField(blank=True, null=True)  # amount of funding
    date = models.DateField(blank=True, null=True)  # funding date
    stage = models.CharField(max_length=254, null=True, blank=True)  # stage of funding
    investor = models.CharField(max_length=254, null=True, blank=True)  # name of investor
