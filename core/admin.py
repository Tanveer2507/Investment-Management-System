from django.contrib import admin
from .models import Startup, Watchlist, Investment, Document, UserProfile, Newsletter


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
	list_display = ('name', 'founder', 'industry', 'created_at')


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
	list_display = ('investor', 'startup', 'amount', 'date', 'stage')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
	list_display = ('user', 'startup', 'created_at')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('title', 'uploaded_by', 'uploaded_at')
	search_fields = ('title', 'description')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'email_investments', 'email_startups', 'push_watchlist', 'created_at')
	list_filter = ('email_investments', 'email_startups', 'email_market', 'email_weekly')
	search_fields = ('user__username', 'user__email')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
	list_display = ('email', 'subscribed_at', 'is_active')
	list_filter = ('is_active', 'subscribed_at')
	search_fields = ('email',)
	readonly_fields = ('subscribed_at',)
