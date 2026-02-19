"""
Core views for the Investment Management System.
# pylint: disable=too-many-ancestors
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
import csv
import io
from .models import Startup, Investment, Watchlist
from .forms import StartupForm, InvestmentForm, UserProfileForm, DocumentForm
from .models import Document
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

class HomeView(TemplateView):
    """
    View for the home page.
    """
    template_name = 'home.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    View for the user dashboard.
    """
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        investments = Investment.objects.filter(investor=user)
        context['total_investment'] = investments.aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_startups'] = investments.values('startup').distinct().count()
        context['recent_investments'] = investments.order_by('-date')[:5]
        context['investments'] = investments
        return context

class StartupCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new startup.
    """
    model = Startup
    form_class = StartupForm
    template_name = 'add_startup.html'
    # Redirect to the created startup detail and show a success message
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Startup created successfully!")
        return response

    def get_success_url(self):
        return reverse('startup_detail', args=[self.object.pk])

class StartupUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating an existing startup.
    """
    model = Startup
    form_class = StartupForm
    template_name = 'add_startup.html'
    success_message = "Startup updated successfully!"
    
    def get_success_url(self):
        return reverse('startup_detail', args=[self.object.pk])

class InvestmentCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new investment.
    """
    model = Investment
    form_class = InvestmentForm
    template_name = 'add_investment.html'
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        """Pre-fill startup field if provided in URL"""
        initial = super().get_initial()
        startup_id = self.request.GET.get('startup')
        if startup_id:
            try:
                startup = Startup.objects.get(id=startup_id)
                initial['startup'] = startup
            except Startup.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        startup_id = self.request.GET.get('startup')
        if startup_id:
            try:
                context['selected_startup'] = Startup.objects.get(id=startup_id)
            except Startup.DoesNotExist:
                pass
        return context

    def form_valid(self, form):
        form.instance.investor = self.request.user
        messages.success(self.request, f'Investment of ${form.instance.amount} in {form.instance.startup.name} created successfully!')
        return super().form_valid(form)

class PortfolioView(LoginRequiredMixin, ListView):
    """
    View for displaying the user's portfolio.
    """
    model = Startup
    template_name = 'portfolio.html'
    context_object_name = 'startups'

    def get_queryset(self):
        # In a real app, we'd filter by investments. 
        # For now, let's just return all startups to populate the view.
        return Startup.objects.all()

class MarketsView(TemplateView):
    """
    View for the markets page.
    """
    template_name = 'markets.html'

class StartupListView(ListView):
    """
    View for listing all startups.
    """
    model = Startup
    template_name = 'startup_list.html'
    context_object_name = 'startups'
    ordering = ['-created_at']

def register_view(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    """
    View for user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    """
    View for user logout.
    """
    logout(request)
    return redirect('home')

class StartupDetailView(DetailView):
    """
    View for displaying startup details.
    """
    model = Startup
    template_name = "startup_detail_v2.html"
    context_object_name = "startup"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_in_watchlist'] = Watchlist.objects.filter(
                user=self.request.user,
                startup=self.object
            ).exists()
        else:
            context['is_in_watchlist'] = False
        return context


@login_required
def toggle_watchlist(request, pk):
    """
    View to toggle a startup in the user's watchlist.
    """
    startup = get_object_or_404(Startup, pk=pk)
    watchlist_item, created = Watchlist.objects.get_or_create(
        user=request.user,
        startup=startup
    )

    if not created:
        watchlist_item.delete()
        messages.success(request, f"{startup.name} removed from your watchlist.")
    else:
        messages.success(request, f"{startup.name} added to your watchlist.")

    return HttpResponseRedirect(reverse("startup_detail", args=[pk]))

class WatchlistView(LoginRequiredMixin, ListView):
    """
    View for displaying the user's watchlist.
    """
    model = Watchlist
    template_name = 'watchlist.html'
    context_object_name = 'watchlist_items'

    def get_queryset(self):
        return Watchlist.objects.filter(
            user=self.request.user
        ).select_related('startup')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update their basic profile information."""
    model = User
    form_class = UserProfileForm
    template_name = 'auth/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Profile updated successfully.')
        return response

    def get_success_url(self):
        return reverse('profile')


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display user's profile with quick stats."""
    template_name = 'auth/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_obj'] = user
        context['investments_count'] = Investment.objects.filter(investor=user).count()
        context['watchlist_count'] = Watchlist.objects.filter(user=user).count()
        return context


class ReportsOverviewView(TemplateView):
    """Overview dashboard for reports (public preview)."""
    template_name = 'reports/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_investment'] = Investment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_startups'] = Startup.objects.count()
        context['recent_investments'] = Investment.objects.order_by('-date')[:10]
        return context


class InvestmentsReportView(LoginRequiredMixin, TemplateView):
    """Investments report table."""
    template_name = 'reports/investments.html'
    def get(self, request, *args, **kwargs):
        qs = Investment.objects.select_related('startup', 'investor').all()

        # Filters
        q = request.GET.get('q', '').strip()
        stage = request.GET.get('stage', '').strip()
        start_date = request.GET.get('start_date', '').strip()
        end_date = request.GET.get('end_date', '').strip()
        order = request.GET.get('order', '-date')

        if q:
            qs = qs.filter(Q(startup__name__icontains=q) | Q(investor__username__icontains=q))
        if stage:
            qs = qs.filter(stage__iexact=stage)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        # Ordering
        try:
            qs = qs.order_by(order)
        except Exception:
            qs = qs.order_by('-date')

        # Export CSV
        if request.GET.get('export') == 'csv':
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(['Date', 'Investor', 'Startup', 'Stage', 'Amount', 'Equity %'])
            for inv in qs:
                writer.writerow([inv.date, inv.investor.username, inv.startup.name, inv.stage, str(inv.amount), str(inv.equity_percentage)])
            resp = HttpResponse(buf.getvalue(), content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="investments_report.csv"'
            return resp

        # Compute summary stats for display
        investments_count = qs.count()
        distinct_startups = qs.values('startup').distinct().count()
        top_startups = qs.values('startup__name').annotate(total=Sum('amount')).order_by('-total')[:5]

        # Context for template
        context = self.get_context_data(**kwargs)
        context['investments'] = qs
        context['total_investment'] = qs.aggregate(Sum('amount'))['amount__sum'] or 0
        context['investments_count'] = investments_count
        context['distinct_startups'] = distinct_startups
        context['top_startups'] = top_startups
        context['q'] = q
        context['stage'] = stage
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['order'] = order
        return self.render_to_response(context)


class StartupsReportView(LoginRequiredMixin, TemplateView):
    """Startups report table."""
    template_name = 'reports/startups.html'
    def get(self, request, *args, **kwargs):
        qs = Startup.objects.all()

        q = request.GET.get('q', '').strip()
        industry = request.GET.get('industry', '').strip()
        order = request.GET.get('order', '-created_at')

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(founder__icontains=q) | Q(industry__icontains=q))
        if industry:
            qs = qs.filter(industry__icontains=industry)

        try:
            qs = qs.order_by(order)
        except Exception:
            qs = qs.order_by('-created_at')

        if request.GET.get('export') == 'csv':
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(['Name', 'Founder', 'Industry', 'Founded Date', 'Contact Email', 'Website'])
            for s in qs:
                writer.writerow([s.name, s.founder, s.industry, str(s.founded_date), s.contact_email or '', s.website or ''])
            resp = HttpResponse(buf.getvalue(), content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="startups_report.csv"'
            return resp

        # compute summary stats
        total_startups = qs.count()
        distinct_industries = qs.values('industry').distinct().count()
        top_industries = qs.values('industry').annotate(count=Count('id')).order_by('-count')[:6]

        context = self.get_context_data(**kwargs)
        context['startups'] = qs
        context['q'] = q
        context['industry'] = industry
        context['order'] = order
        context['total_startups'] = total_startups
        context['distinct_industries'] = distinct_industries
        context['top_industries'] = top_industries
        return self.render_to_response(context)


class DocumentsListView(TemplateView):
    """Public list of documents with search."""
    template_name = 'documents/list.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        qs = Document.objects.all()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        context = self.get_context_data(**kwargs)
        context['documents'] = qs
        context['q'] = q
        return self.render_to_response(context)


class DocumentUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/upload.html'

    def get(self, request, *args, **kwargs):
        form = DocumentForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('documents_list')
        return self.render_to_response({'form': form})


class DocumentDetailView(TemplateView):
    template_name = 'documents/detail.html'

    def get(self, request, pk, *args, **kwargs):
        doc = get_object_or_404(Document, pk=pk)
        return self.render_to_response({'document': doc})


class MyDocumentsView(LoginRequiredMixin, TemplateView):
    """List documents uploaded by the current user with management actions."""
    template_name = 'documents/my_documents.html'

    def get(self, request, *args, **kwargs):
        qs = Document.objects.filter(uploaded_by=request.user)
        context = self.get_context_data(**kwargs)
        context['documents'] = qs
        return self.render_to_response(context)


class DocumentDeleteView(LoginRequiredMixin, TemplateView):
    """Handle document deletion via POST."""

    def post(self, request, pk, *args, **kwargs):
        doc = get_object_or_404(Document, pk=pk, uploaded_by=request.user)
        doc.file.delete(save=False)
        doc.delete()
        messages.success(request, 'Document deleted successfully.')
        return redirect('documents_my')


@login_required
def document_download(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    # For dev server, redirect to file URL (served by MEDIA). In production, serve via X-Sendfile or cloud.
    return redirect(doc.file.url)


class SettingsView(LoginRequiredMixin, TemplateView):
    """
    View for user settings page with multiple sections.
    """
    template_name = 'auth/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get or create user profile
        from .models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        return context

    def post(self, request, *args, **kwargs):
        from .models import UserProfile
        section = request.POST.get('section')
        
        if section == 'account':
            # Update account information
            user = request.user
            user.username = request.POST.get('username', user.username)
            user.email = request.POST.get('email', user.email)
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()
            messages.success(request, 'Account information updated successfully.')
        
        elif section == 'password':
            # Change password
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
            else:
                for error in form.errors.values():
                    messages.error(request, error)
        
        elif section == 'notifications':
            # Save notification preferences
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            # Email notifications
            profile.email_investments = 'email_investments' in request.POST
            profile.email_startups = 'email_startups' in request.POST
            profile.email_market = 'email_market' in request.POST
            profile.email_weekly = 'email_weekly' in request.POST
            
            # Push notifications
            profile.push_watchlist = 'push_watchlist' in request.POST
            profile.push_messages = 'push_messages' in request.POST
            
            profile.save()
            messages.success(request, 'Notification preferences saved successfully.')
        
        elif section == 'preferences':
            # Save display preferences
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.language = request.POST.get('language', 'en')
            profile.timezone = request.POST.get('timezone', 'UTC')
            profile.currency = request.POST.get('currency', 'USD')
            profile.date_format = request.POST.get('date_format', 'mdy')
            profile.show_charts = 'show_charts' in request.POST
            profile.compact_view = 'compact_view' in request.POST
            profile.save()
            messages.success(request, 'Display preferences saved successfully.')
        
        elif section == 'privacy':
            # Save privacy settings
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.profile_visibility = request.POST.get('profile_visibility', 'public')
            profile.save()
            messages.success(request, 'Privacy settings saved successfully.')
        
        return redirect('settings')


class NotificationsView(LoginRequiredMixin, TemplateView):
    """
    View for user notifications page.
    """
    template_name = 'auth/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # In a real application, you would fetch notifications from the database
        # For now, we'll use the template's static data
        return context


class AboutView(TemplateView):
    """
    View for the About Us page.
    """
    template_name = 'about.html'


class CareersView(TemplateView):
    """
    View for the Careers page.
    """
    template_name = 'careers.html'


class BlogView(TemplateView):
    """
    View for the Blog page.
    """
    template_name = 'blog.html'


class ContactView(TemplateView):
    """
    View for the Contact Us page.
    """
    template_name = 'contact.html'


class PrivacyView(TemplateView):
    """
    View for the Privacy Policy page.
    """
    template_name = 'privacy.html'


from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Newsletter
from django.core.mail import send_mail
from django.conf import settings

@require_POST
def newsletter_subscribe(request):
    """
    Handle newsletter subscription.
    """
    email = request.POST.get('email', '').strip()
    
    if not email:
        return JsonResponse({'success': False, 'message': 'Please enter an email address.'}, status=400)
    
    # Basic email validation
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)
    
    # Check if already subscribed
    if Newsletter.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'This email is already subscribed to our newsletter.'}, status=400)
    
    # Create subscription
    try:
        Newsletter.objects.create(email=email)
        
        # Send confirmation email
        try:
            send_mail(
                subject='Welcome to InvestTrack Newsletter!',
                message=f'''
Hello!

Thank you for subscribing to the InvestTrack newsletter!

You'll now receive:
- Latest investment opportunities
- Startup success stories
- Market insights and trends
- Weekly portfolio updates

Stay tuned for exciting updates!

Best regards,
The InvestTrack Team

---
If you wish to unsubscribe, please contact us at support@investtrack.com
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception as e:
            # Log error but don't fail the subscription
            print(f"Email sending failed: {e}")
        
        return JsonResponse({
            'success': True, 
            'message': 'Successfully subscribed! Check your email for confirmation.'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'An error occurred. Please try again later.'
        }, status=500)
