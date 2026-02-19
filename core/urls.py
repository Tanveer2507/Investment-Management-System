from django.urls import path, include
from django.shortcuts import redirect
from core.views import (
    HomeView, DashboardView, StartupCreateView, StartupUpdateView,
    InvestmentCreateView, PortfolioView, MarketsView, StartupListView,
    StartupDetailView, WatchlistView, register_view, login_view, logout_view, toggle_watchlist,
    ReportsOverviewView, InvestmentsReportView, StartupsReportView,
    ProfileUpdateView, ProfileView, SettingsView, NotificationsView,
    AboutView, CareersView, BlogView, ContactView, PrivacyView,
    newsletter_subscribe,
)
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-startup/', StartupCreateView.as_view(), name='add_startup'),
    path('add-investment/', InvestmentCreateView.as_view(), name='add_investment'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('markets/', MarketsView.as_view(), name='markets'),
    path('startups/', StartupListView.as_view(), name='startup_list'),
    path('startups/<int:pk>/', StartupDetailView.as_view(), name='startup_detail'),
    path('startups/<int:pk>/edit/', StartupUpdateView.as_view(), name='edit_startup'),
    path('startups/<int:pk>/watchlist/', toggle_watchlist, name='toggle_watchlist'),
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    # Documents
    path('documents/', views.DocumentsListView.as_view(), name='documents_list'),
    path('documents/upload/', views.DocumentUploadView.as_view(), name='documents_upload'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('documents/<int:pk>/download/', views.document_download, name='document_download'),
    path('documents/my/', views.MyDocumentsView.as_view(), name='documents_my'),
    path('documents/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
    path('account/profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('account/profile/', ProfileView.as_view(), name='profile'),
    path('account/settings/', SettingsView.as_view(), name='settings'),
    path('account/notifications/', NotificationsView.as_view(), name='notifications'),
    # Reports
    # imported views for reports are available in core.views
    # Reports
    path('reports/', ReportsOverviewView.as_view(), name='reports_overview'),
    path('reports/investments/', InvestmentsReportView.as_view(), name='investments_report'),
    path('reports/startups/', StartupsReportView.as_view(), name='startups_report'),
    # Company Pages
    path('about/', AboutView.as_view(), name='about'),
    path('careers/', CareersView.as_view(), name='careers'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    # Newsletter
    path('newsletter/subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
]
