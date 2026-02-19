"""
Test script to verify settings functionality
Run with: python manage.py shell < test_settings.py
"""

from django.contrib.auth.models import User
from core.models import UserProfile

# Get or create test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

if created:
    user.set_password('testpass123')
    user.save()
    print(f"✓ Created test user: {user.username}")
else:
    print(f"✓ Using existing user: {user.username}")

# Get or create profile
profile, created = UserProfile.objects.get_or_create(user=user)

if created:
    print("✓ Created new UserProfile")
else:
    print("✓ Using existing UserProfile")

# Test all settings
print("\n=== Current Settings ===")
print(f"Email Notifications:")
print(f"  - Investments: {profile.email_investments}")
print(f"  - Startups: {profile.email_startups}")
print(f"  - Market: {profile.email_market}")
print(f"  - Weekly: {profile.email_weekly}")

print(f"\nPush Notifications:")
print(f"  - Watchlist: {profile.push_watchlist}")
print(f"  - Messages: {profile.push_messages}")

print(f"\nDisplay Preferences:")
print(f"  - Language: {profile.language}")
print(f"  - Timezone: {profile.timezone}")
print(f"  - Currency: {profile.currency}")
print(f"  - Date Format: {profile.date_format}")
print(f"  - Show Charts: {profile.show_charts}")
print(f"  - Compact View: {profile.compact_view}")

print(f"\nPrivacy Settings:")
print(f"  - Profile Visibility: {profile.profile_visibility}")

print("\n✓ All settings loaded successfully!")
print(f"\nYou can now login with:")
print(f"  Username: {user.username}")
print(f"  Password: testpass123")
