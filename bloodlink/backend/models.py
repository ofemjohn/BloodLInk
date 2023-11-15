from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('blood_bank', 'Blood Bank'),
        ('blood_recipient', 'Blood Recipient'),
        ('donor', 'Donor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    # Add other fields specific to each user type

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


class BloodType(models.Model):
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type


class BloodBank(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(default='')
    contact_information = models.JSONField(default=dict)
    blood_stock = models.ManyToManyField(BloodType, related_name='hospitals')

    def __str__(self):
        return self.name


class Donor(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    contact_information = models.JSONField()
    address = models.TextField()
    medical_history = models.TextField()
    blood_type = models.ForeignKey(
        BloodType, on_delete=models.CASCADE, related_name='donors')
    available = models.BooleanField()

    def __str__(self):
        return self.name


class Recipient(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    contact_information = models.JSONField()
    address = models.TextField()
    medical_history = models.TextField()
    blood_type = models.ForeignKey(
        BloodType, on_delete=models.CASCADE, related_name='recipients')
    need_blood = models.BooleanField()
    preferred_source = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class DonationRequest(models.Model):
    requester = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='donation_requests')
    blood_type = models.ForeignKey(
        BloodType, on_delete=models.CASCADE, related_name='donation_requests')
    number_of_pints_needed = models.IntegerField()
    status = models.CharField(max_length=20)
    # Add other fields as needed

    def __str__(self):
        return f"Donation Request for {self.number_of_pints_needed} pints of {self.blood_type} by {self.requester}"
