"""
Database models for the Investment Management System.
"""
from django.db import models
from django.contrib.auth.models import User

class Startup(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='startups/', blank=True, null=True)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    founder = models.CharField(max_length=255)
    founded_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    contact_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='watchlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'startup')

    def __str__(self):
        return f"{self.user.username} watching {self.startup.name}"

class Investment(models.Model):
    STAGE_CHOICES = [
        ('Seed', 'Seed'),
        ('Series A', 'Series A'),
        ('Series B', 'Series B'),
        ('Series C', 'Series C'),
        ('IPO', 'IPO'),
    ]

    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    equity_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Equity percentage owned")

    def __str__(self):
        return f"{self.investor.username} - {self.startup.name} ({self.amount})"


class Document(models.Model):
    """Simple Document model for uploads and downloads."""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """User profile model to store user preferences and settings."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Email Notification Preferences
    email_investments = models.BooleanField(default=True, help_text="New investment opportunities")
    email_startups = models.BooleanField(default=True, help_text="Startup updates and milestones")
    email_market = models.BooleanField(default=False, help_text="Market trends and analysis")
    email_weekly = models.BooleanField(default=True, help_text="Weekly portfolio summary")
    
    # Push Notification Preferences
    push_watchlist = models.BooleanField(default=True, help_text="Watchlist updates")
    push_messages = models.BooleanField(default=True, help_text="Messages and alerts")
    
    # Display Preferences
    language = models.CharField(max_length=10, default='en', help_text="Preferred language")
    timezone = models.CharField(max_length=50, default='UTC', help_text="Preferred timezone")
    currency = models.CharField(max_length=10, default='USD', help_text="Preferred currency")
    date_format = models.CharField(max_length=10, default='mdy', help_text="Date format preference")
    show_charts = models.BooleanField(default=True, help_text="Show charts and graphs")
    compact_view = models.BooleanField(default=False, help_text="Use compact view")
    
    # Privacy Settings
    profile_visibility = models.CharField(max_length=20, default='public', help_text="Profile visibility")
    
    # Security Settings
    two_factor_enabled = models.BooleanField(default=False, help_text="Two-factor authentication enabled")
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True, help_text="2FA secret key")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class Newsletter(models.Model):
    """Newsletter subscription model."""
    email = models.EmailField(unique=True, help_text="Subscriber email address")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Subscription status")
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']

