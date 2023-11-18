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


class BloodBank(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(default='')
    phone = models.CharField(max_length=15, default='+234 7858559023')
    services_provided = models.TextField(default='')
    operational_hours = models.CharField(max_length=255, default='9 AM - 5 PM')
    # Add more fields as needed

    def __str__(self):
        return self.name


class Donor(models.Model):
    DONATION_TYPE_CHOICES = [
        ('free', 'Free Donation'),
        ('token', 'Token Donation'),
    ]

    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15, default='+234 7858559023')
    address = models.TextField()
    donation_type = models.CharField(
        max_length=10, choices=DONATION_TYPE_CHOICES, default='free')
    available = models.BooleanField()

    def __str__(self):
        return self.name


class DonationRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('individual', 'From Individual (Donor)'),
        ('blood_bank', 'From Blood Bank'),
    ]

    requester = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='donation_requests'
    )
    number_of_pints_needed = models.IntegerField()
    status = models.CharField(max_length=20)
    donor = models.ForeignKey(
        Donor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donation_requests'
    )
    request_type = models.CharField(
        max_length=15,
        choices=REQUEST_TYPE_CHOICES,
        default='individual'
    )
    # Other fields as needed

    def __str__(self):
        return f"Donation Request for {self.number_of_pints_needed} pints by {self.requester}"
