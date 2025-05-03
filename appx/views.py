# views.py
import json
from datetime import datetime, date, time, timedelta
from django.db.models.functions import TruncDate
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q, Avg, Prefetch, F, ExpressionWrapper, DurationField
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.db import transaction
import datetime
import json
import os
from datetime import datetime
import google.generativeai as genai
from django.conf import settings # To get the API key
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Scholarship # Import your Scholarship model
from .models import Profile, Scholarship, Application, Document, FAQItem, Notification
from .forms import (
    RegistrationForm, ProfileForm, CustomUserChangeForm, ScholarshipForm,
    ApplicationForm, UserForm
)




# --- Helper funksiyalar ---
def is_admin_or_superadmin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role in ['admin', 'superadmin']

def is_superadmin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'superadmin'

# --- Autentifikatsiya View'lari ---
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        messages.info(self.request, f"Xush kelibsiz, {self.request.user.username}!")
        return reverse_lazy('dashboard')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
             messages.info(request, "Hisobingizdan muvaffaqiyatli chiqdingiz.")
        return super().dispatch(request, *args, **kwargs)

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                auth_login(request, user)
                messages.success(request, f"Muvaffaqiyatli roʻyxatdan oʻtdingiz, {user.username}! Hisobingizga kirdingiz.")
                return redirect('dashboard')
            except Exception as e:
                 messages.error(request, f"Ro'yxatdan o'tishda xatolik yuz berdi: {e}")
        else:
             messages.error(request, "Iltimos, quyidagi xatoliklarni toʻgʻrilang.")
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Sahifa View'lari ---
@login_required
def dashboard(request):
    today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)
    start_of_month = today.replace(day=1)
    last_month_end = start_of_month - timezone.timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    start_of_week = today - timezone.timedelta(days=today.weekday())

    # Arizalar statistikasi
    today_apps_count = Application.objects.filter().count()
    yesterday_apps_count = Application.objects.filter(submission_date__date=yesterday).count()
    approved_this_month = Application.objects.filter(status='approved', last_updated__date__gte=start_of_month).count()
    approved_last_month = Application.objects.filter(status='approved', last_updated__date__range=(last_month_start, last_month_end)).count()
    reviewing_apps_count = Application.objects.filter(status='reviewing').count()
    # O'tgan haftadagi umumiy son bilan solishtirish kerak bo'lishi mumkin
    clarification_apps_count = Application.objects.filter(status='clarification').count()

    def calculate_change(current, previous):
        if previous > 0: return round(((current - previous) / previous) * 100)
        elif current > 0: return 100
        return 0

    today_vs_yesterday_change = calculate_change(today_apps_count, yesterday_apps_count)
    approved_change = calculate_change(approved_this_month, approved_last_month)

    # So'nggi arizalar
    recent_applications = Application.objects.select_related('applicant__profile', 'scholarship').order_by('-submission_date')[:5]

    # Grafik uchun
    status_counts_qs = Application.objects.values('status').annotate(count=Count('id')).order_by('status')
    status_choices_dict = dict(Application.STATUS_CHOICES)
    chart_labels = [status_choices_dict.get(s['status'], s['status'].capitalize()) for s in status_counts_qs]
    chart_data = [s['count'] for s in status_counts_qs]

    total_applications = Application.objects.count()
    total_approved = Application.objects.filter(status='approved').count()
    total_pending = Application.objects.filter(status__in=['submitted', 'reviewing', 'clarification']).count()
    total_rejected = Application.objects.filter(status='rejected').count()

    context = {
        'stats': {
            'today_submitted': {'value': today_apps_count, 'change': today_vs_yesterday_change},
            'month_approved': {'value': approved_this_month, 'change': approved_change},
            'active_reviewing': {'value': reviewing_apps_count, 'change': None}, # O'tgan hafta logikasi kerak
            'needs_attention': {'value': clarification_apps_count, 'change': None}, # Oxirgi 24 soat logikasi kerak

        },
        'recent_applications': recent_applications,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'total_applications': total_applications,
        'total_approved': total_approved,
        'total_pending': total_pending,
        'total_rejected': total_rejected,
    }
    return render(request, 'dashboard.html', context)

@login_required
@user_passes_test(is_admin_or_superadmin)
def all_applications(request):
    application_list = Application.objects.select_related(
        'applicant__profile', 'scholarship'
    ).prefetch_related(
        'documents'
    ).order_by('-submission_date')

    status_filter = request.GET.get('status_filter')
    scholarship_filter = request.GET.get('scholarship_filter')
    search_query = request.GET.get('search')

    query = Q()
    if status_filter: query &= Q(status=status_filter)
    if scholarship_filter: query &= Q(scholarship_id=scholarship_filter)
    if search_query:
        query &= ( Q(applicant__username__icontains=search_query) |
                   Q(applicant__email__icontains=search_query) |
                   Q(applicant_full_name__icontains=search_query) |
                   Q(scholarship__name__icontains=search_query) |
                   Q(status__icontains=search_query) )
    application_list = application_list.filter(query)

    paginator = Paginator(application_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'all_scholarships': Scholarship.objects.filter(status__in=['active', 'completed']),
        'status_choices': Application.STATUS_CHOICES
    }
    return render(request, 'all_applications.html', context)

@login_required
@user_passes_test(is_admin_or_superadmin)
def analytics(request):
    # --- Date Filtering ---
    # Get date strings from GET parameters, default to last 30 days
    default_end_date = timezone.now().date()
    # Use timedelta directly because of the import style
    default_start_date = default_end_date - timedelta(days=30)
    date_start_str = request.GET.get('date_start', default_start_date.strftime('%Y-%m-%d'))
    date_end_str = request.GET.get('date_end', default_end_date.strftime('%Y-%m-%d'))

    try:
        # Parse the date strings into actual date objects
        # Use datetime.strptime directly
        date_start = datetime.strptime(date_start_str, '%Y-%m-%d').date()
        date_end_obj = datetime.strptime(date_end_str, '%Y-%m-%d').date()
        # Use timedelta directly
        date_end_for_filter = date_end_obj + timedelta(days=1) # Use this for filtering < end_date+1
        date_end = date_end_obj # Use the original end date for display

    except ValueError:
        # Fallback to defaults if parsing fails
        date_end = default_end_date
        # Use timedelta directly
        date_start = date_end - timedelta(days=30)
        date_start_str = date_start.strftime('%Y-%m-%d')
        date_end_str = date_end.strftime('%Y-%m-%d')
        # Use timedelta directly
        date_end_for_filter = date_end + timedelta(days=1)
        messages.warning(request, "Sana formati noto'g'ri yoki mavjud emas. Standart 30 kunlik davr ishlatildi.")

    # --- Chart Data ---

    # 1. Application Status Chart
    status_counts_qs = Application.objects.filter(
        submission_date__gte=date_start,
        submission_date__lt=date_end_for_filter
    ).values('status').annotate(count=Count('id')).order_by('status')

    status_choices_dict = dict(Application.STATUS_CHOICES)
    status_chart_labels = [status_choices_dict.get(s['status'], str(s['status']).capitalize()) for s in status_counts_qs]
    status_chart_data = [s['count'] for s in status_counts_qs]

    # 2. Application Trend Chart (Daily)
    trend_data = Application.objects.filter(
        submission_date__gte=date_start,
        submission_date__lt=date_end_for_filter
    ).annotate(
        day=TruncDate('submission_date')
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')

    trend_chart_labels = [t['day'].strftime('%d-%b') for t in trend_data if t.get('day')]
    trend_chart_data = [t['count'] for t in trend_data]

    # 3. Success Rate Chart (Placeholder - needs logic)
    success_rate_chart_labels = []
    success_rate_chart_data = []

    # 4. User Roles Chart
    role_counts_qs = Profile.objects.values('role').annotate(count=Count('id')).order_by('role')
    role_choices_dict = dict(Profile.ROLE_CHOICES)
    role_chart_labels = [role_choices_dict.get(r['role'], str(r['role'])) for r in role_counts_qs]
    role_chart_data = [r['count'] for r in role_counts_qs]

    # 5. KPIs
    # New users within the selected period
    try:
        # Use datetime.combine and time.min directly
        start_dt = datetime.combine(date_start, time.min, tzinfo=timezone.get_current_timezone())
        end_dt = datetime.combine(date_end_for_filter, time.min, tzinfo=timezone.get_current_timezone())

        new_users_count = User.objects.filter(
            date_joined__gte=start_dt,
            date_joined__lt=end_dt
        ).count()

        # Average review time for applications decided within the period
        avg_review_time_agg = Application.objects.filter(
            status__in=['approved', 'rejected'],
            # Use datetime.combine and time.min directly
            last_updated__gte=start_dt,
            last_updated__lt=end_dt
        ).annotate(
            duration=ExpressionWrapper(F('last_updated') - F('submission_date'), output_field=DurationField())
        ).aggregate(avg_duration=Avg('duration'))

        # Extract days from the average duration (handle None case)
        avg_days = 0
        if avg_review_time_agg and avg_review_time_agg.get('avg_duration'):
            # avg_duration is a timedelta object
            avg_days = avg_review_time_agg['avg_duration'].days

    except Exception as e:
        # Handle potential errors during KPI calculation, e.g., timezone issues
        messages.error(request, f"KPI hisoblashda xatolik: {e}")
        new_users_count = 0
        avg_days = 0
        # Optionally log the error e for debugging

    # --- Context for Template ---
    context = {
        'date_start': date_start_str,
        'date_end': date_end_str,
        'status_chart': {'labels': status_chart_labels, 'data': status_chart_data},
        'trend_chart': {'labels': trend_chart_labels, 'data': trend_chart_data},
        'success_rate_chart': {'labels': success_rate_chart_labels, 'data': success_rate_chart_data},
        'role_chart': {'labels': role_chart_labels, 'data': role_chart_data},
        'kpi_new_users': new_users_count,
        'kpi_avg_review_days': avg_days,
    }
    return render(request, 'analytics.html', context)

@login_required
def find_scholarships(request):
    search_query = request.GET.get('search')
    field_filter = request.GET.get('field')
    type_filter = request.GET.get('type')

    query = Q(status='active')
    if search_query:
        query &= ( Q(name__icontains=search_query) |
                   Q(provider__icontains=search_query) |
                   Q(description__icontains=search_query) )
    if field_filter: query &= Q(field=field_filter)
    if type_filter: query &= Q(type=type_filter)

    scholarship_list = Scholarship.objects.filter(query).order_by('deadline')

    paginator = Paginator(scholarship_list, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'field_choices': Scholarship.FIELD_CHOICES,
        'type_choices': Scholarship.TYPE_CHOICES,
    }
    return render(request, 'find_scholarships.html', context)
############################################################

GEMINI_API_KEY = "AIzaSyA8VtLhUnjrUKPHhFUbBxfJXYKR5SlZkq8"

# Gemini AI ni sozlash
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Modelni yaratish (masalan, 'gemini-pro')
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"Gemini sozlamalarida xatolik: {e}")
    # Agar sozlashda xatolik bo'lsa, modelni None qilib qo'yish mumkin
    model = None

@login_required
def help_center(request):
    search_query = request.GET.get('search', '').strip() # .strip() bosh/oxiridagi bo'shliqlarni olib tashlaydi
    ai_response = None
    error_message = None

    if not model:
        error_message = "Sun'iy intellekt xizmati hozircha mavjud emas. Sozlamalarni tekshiring."

    elif search_query:
        try:
            # Maxsuslashtirilgan Prompt (Ko'rsatma)
            prompt = f"""
            Sen O'zbekistondagi davlat grantlari, nomdor davlat stipendiyalari (masalan, Islom Karimov nomidagi davlat stipendiyasi, Navoiy nomidagi davlat stipendiyasi va boshqalar) va Zulfiya nomidagi Davlat mukofoti haqida ma'lumot berishga ixtisoslashgan yordamchi AI assistantisan.

            Sening vazifang quyidagilardan iborat:
            1. Yuqorida sanab o'tilgan grantlar, stipendiyalar va mukofotlar haqida UMUMIY ma'lumot berish (ularning maqsadi, kimlar uchunligi, qanday afzalliklar berishi va hokazo).
            2. Ushbu dasturlarga ariza topshirish uchun talab qilinadigan ASOSIY HUJJATLAR ro'yxatini taqdim etish.

            MUHIM QOIDALAR:
            - Faqat va faqat yuqorida ko'rsatilgan mavzular (O'zbekiston grantlari, nomdor stipendiyalari, Zulfiya mukofoti va ularga kerakli hujjatlar) bo'yicha javob ber. Boshqa HECH QANDAY mavzuga javob berma.
            - Agar foydalanuvchi boshqa mavzuda savol bersa (masalan, "ob-havo qanday?", "matematika haqida gapir", "chet el grantlari bormi?" kabi), quyidagi javobni QAT'IY ravishda qaytar: "Kechirasiz, men faqat O'zbekistondagi davlat grantlari, nomdor davlat stipendiyalari va Zulfiya mukofoti hamda ularga kerakli hujjatlar haqida ma'lumot bera olaman."
            - Javoblaring aniq, qisqa va tushunarli bo'lsin. Hujjatlar ro'yxatini iloji bo'lsa raqamlangan yoki belgili ro'yxat ko'rinishida ber.
            - Agar so'ralgan ma'lumot bo'yicha aniq biliming bo'lmasa yoki ma'lumot topa olmasang, "Bu haqida hozircha aniq ma'lumotim yo'q" yoki shunga o'xshash javob ber. Taxminiy ma'lumot bermaslikka harakat qil.

            Foydalanuvchi savoli: "{search_query}"

            Javobingni faqat yuqoridagi qoidalarga amal qilgan holda shakllantir.
            """

            # Gemini AI ga so'rov yuborish
            response = model.generate_content(prompt)
            ai_response = response.text

        except Exception as e:
            # Xatolikni log qilish (production uchun logging sozlamalarini ishlating)
            print(f"Gemini API so'rovida xatolik: {e}")
            # Foydalanuvchiga xatolik haqida xabar berish
            error_message = "Sun'iy intellekt bilan bog'lanishda xatolik yuz berdi. Iltimos keyinroq qayta urinib ko'ring yoki administratsiya bilan bog'laning."
            # Xatolik yuz berganda ai_response ni None qilib qoldiramiz yoki xato xabarini beramiz
            # ai_response = error_message



    context = {
        # 'faq_items': faq_items, # Endi bu kerak emas
        'search_query': search_query,
        'ai_response': ai_response,
        'error_message': error_message, # Xatolik xabarini ham jo'natamiz
    }
    return render(request, 'help_center.html', context)
####################################################
@login_required
@user_passes_test(is_admin_or_superadmin)
def manage_scholarships(request):
    status_filter = request.GET.get('status_filter')
    search_query = request.GET.get('search')

    query = Q()
    if status_filter: query &= Q(status=status_filter)
    if search_query: query &= (Q(name__icontains=search_query) | Q(provider__icontains=search_query))

    scholarship_list = Scholarship.objects.filter(query).annotate(
        application_count=Count('applications')
    ).order_by('-created_at')

    paginator = Paginator(scholarship_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    form = ScholarshipForm() # Modal uchun

    context = {
        'page_obj': page_obj,
        'status_choices': Scholarship.STATUS_CHOICES,
        'form': form
    }
    return render(request, 'manage_scholarships.html', context)

# --- Scholarship AJAX Views ---
@login_required
@user_passes_test(is_admin_or_superadmin)
def scholarship_create(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    raise Http404

@login_required
@user_passes_test(is_admin_or_superadmin)
def scholarship_update(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    elif request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
         data = {
             'id': scholarship.pk, 'name': scholarship.name, 'provider': scholarship.provider,
             'description': scholarship.description, 'amount': scholarship.amount,
             'deadline': scholarship.deadline.strftime('%Y-%m-%d') if scholarship.deadline else '',
             'field': scholarship.field, 'type': scholarship.type, 'status': scholarship.status,
             'popular': scholarship.popular,
         }
         return JsonResponse(data)
    raise Http404

@login_required
@user_passes_test(is_admin_or_superadmin)
def scholarship_toggle_status(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        scholarship = get_object_or_404(Scholarship, pk=pk)
        current_status = scholarship.status
        next_status = 'completed' if current_status == 'active' else 'active'
        scholarship.status = next_status
        scholarship.save()
        return JsonResponse({
            'success': True,
            'new_status_display': scholarship.get_status_display(),
            'new_status_val': scholarship.status,
        })
    raise Http404

@login_required
def my_applications(request):
    status_filter = request.GET.get('status_filter')
    search_query = request.GET.get('search')

    query = Q(applicant=request.user)
    if status_filter: query &= Q(status=status_filter)
    if search_query: query &= (Q(scholarship__name__icontains=search_query) | Q(status__icontains=search_query))

    application_list = Application.objects.filter(query).select_related('scholarship').order_by('-submission_date')

    paginator = Paginator(application_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = { 'page_obj': page_obj, 'status_choices': Application.STATUS_CHOICES }
    return render(request, 'my_applications.html', context)

@login_required
def profile_settings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect('profile_settings')
        else:
            messages.error(request, 'Iltimos, xatoliklarni to\'g\'rilang.')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'profile_settings.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def security(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Parolingiz muvaffaqiyatli oʻzgartirildi!')
            return redirect('security')
        else:
             messages.error(request, 'Parolni oʻzgartirishda xatolik yuz berdi.')
    else:
        password_form = PasswordChangeForm(request.user)
    # TODO: 2FA va Sessiya logikasi
    return render(request, 'security.html', {'password_form': password_form})

@login_required
@transaction.atomic
def submit_application(request):
    scholarship_id = request.GET.get('scholarship_id') or request.POST.get('scholarship_id')
    application_id = request.GET.get('application_id') # Tahrirlash uchun (agar ruxsat bo'lsa)
    application_instance = None
    scholarship = None

    if application_id:
        # Faqat 'clarification' statusidagilarni tahrirlash mumkin (misol)
        application_instance = get_object_or_404(Application, pk=application_id, applicant=request.user, status='clarification')
        scholarship = application_instance.scholarship
    elif scholarship_id:
        scholarship = get_object_or_404(Scholarship, id=scholarship_id, status='active')
        # Yangi ariza topshirishga ruxsatni tekshirish
        if Application.objects.filter(applicant=request.user, scholarship=scholarship).exists():
             messages.warning(request, f"Siz allaqachon '{scholarship.name}' stipendiyasiga ariza topshirgansiz.")
             return redirect('my_applications')
    else:
        messages.error(request, "Stipendiya tanlanmagan yoki ariza topilmadi!")
        return redirect('find_scholarships')

    profile = getattr(request.user, 'profile', None)
    initial_data = {}
    if not application_instance: # Faqat yangi ariza uchun boshlang'ich ma'lumotlar
        initial_data = {
            'applicant_full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'applicant_email': request.user.email,
            'applicant_phone': profile.phone if profile else '',
            'applicant_birth_date': profile.birth_date if profile else None,
            'applicant_iin': profile.iin if profile else '',
            'applicant_address': profile.address if profile else '',
        }

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application_instance)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.applicant = request.user
                application.scholarship = scholarship
                if not application_instance: # Agar yangi ariza bo'lsa
                     application.status = 'submitted'

                application.save()


                doc_fields = {
                    'id_card': form.cleaned_data.get('doc_id_file'), 'transcript': form.cleaned_data.get('doc_transcript_file'),
                    'motivation': form.cleaned_data.get('doc_motivation_file'), 'recommendation': form.cleaned_data.get('doc_recommendation_file'),
                }
                for doc_type, file in doc_fields.items():
                    if file:

                        Document.objects.filter(application=application, document_type=doc_type).delete()
                        Document.objects.create(application=application, document_type=doc_type, file=file)

                action = "yangilandi" if application_instance else "yuborildi"
                messages.success(request, f"Arizangiz muvaffaqiyatli {action}!")
                return redirect('my_applications')
            except Exception as e:
                 messages.error(request, f"Arizani saqlashda kutilmagan xatolik yuz berdi: {e}")
        else:
             messages.error(request, "Iltimos, formadagi xatoliklarni to'g'rilang.")
    else: # GET request
        form = ApplicationForm(instance=application_instance, initial=initial_data if not application_instance else None)

    context = { 'scholarship': scholarship, 'form': form }
    return render(request, 'submit_application.html', context)

@login_required
@user_passes_test(is_superadmin)
def users(request):
    role_filter = request.GET.get('role_filter')
    status_filter_str = request.GET.get('status_filter') # 'Активен' yoki 'Неактивен'
    search_query = request.GET.get('search')

    query = Q(is_superuser=False) # Super Adminlarni chiqarmaymiz
    if role_filter: query &= Q(profile__role=role_filter)
    if status_filter_str:
         is_active_status = status_filter_str == 'Активен'
         query &= Q(is_active=is_active_status)
    if search_query:
        query &= ( Q(username__icontains=search_query) | Q(email__icontains=search_query) |
                   Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) |
                   Q(profile__role__icontains=search_query) )

    user_list = User.objects.filter(query).select_related('profile').order_by('username')

    # Arizalar sonini qo'shish (optimallashtirish mumkin)
    applicant_role_key = 'applicant' # Profile.ROLE_CHOICES dagi kalit
    user_data_list = []
    for user in user_list:
        app_count = '-'
        profile = getattr(user, 'profile', None)
        if profile and profile.role == applicant_role_key:
            app_count = Application.objects.filter(applicant=user).count()
        user_data_list.append({
            'user': user, 'app_count': app_count,
            'role_display': profile.get_role_display() if profile else 'Noma\'lum',
            'status_display': 'Faol' if user.is_active else 'Faol emas',
            'status_val': 'Активен' if user.is_active else 'Неактивен' # Filtr uchun
        })

    paginator = Paginator(user_data_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    form = UserForm() # Modal uchun

    context = {
        'users_page': page_obj,
        'role_choices': Profile.ROLE_CHOICES,
        'status_choices_filter': [('Активен', 'Faollar'), ('Неактивен', 'Faol emaslar')],
        'form': form
    }
    return render(request, 'users.html', context)

# --- User AJAX Views ---
@login_required
@user_passes_test(is_superadmin)
@transaction.atomic
def user_create_or_update(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user_id = request.POST.get('user_id')
        instance = None
        if user_id: instance = get_object_or_404(User, pk=user_id)

        form = UserForm(request.POST) # Formani POST ma'lumotlari bilan yaratamiz
        if form.is_valid():
            data = form.cleaned_data
            try:
                if instance: # Tahrirlash
                    user = instance
                    # Ismni ajratish (oddiy usul)
                    name_parts = data['name'].split(' ', 1)
                    user.first_name = name_parts[0]
                    user.last_name = name_parts[1] if len(name_parts) > 1 else ''
                    user.email = data['email']
                    user.is_active = data['is_active']
                    if data['password']: user.set_password(data['password'])
                    user.save()
                    profile, created = Profile.objects.get_or_create(user=user)
                    profile.role = data['role']
                    profile.save()
                else: # Qo'shish
                    name_parts = data['name'].split(' ', 1)
                    user = User.objects.create_user(
                        username=data['email'], email=data['email'], password=data['password'],
                        first_name=name_parts[0], last_name=name_parts[1] if len(name_parts) > 1 else '',
                        is_active=data['is_active'] )
                    Profile.objects.create(user=user, role=data['role'])
                return JsonResponse({'success': True})
            except Exception as e:
                 return JsonResponse({'success': False, 'errors': {'__all__': [f"Saqlashda xatolik: {e}"]}}, status=500)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    raise Http404

@login_required
@user_passes_test(is_superadmin)
def user_get_details(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = get_object_or_404(User.objects.select_related('profile'), pk=pk)
        profile = getattr(user, 'profile', None)
        data = {
            'id': user.pk, 'name': user.get_full_name() or user.username, 'email': user.email,
            'role': profile.role if profile else '', 'is_active': user.is_active,
        }
        return JsonResponse(data)
    raise Http404

@login_required
@user_passes_test(is_superadmin)
def user_toggle_status(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = get_object_or_404(User, pk=pk)
        if user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'superadmin'):
            return JsonResponse({'success': False, 'error': "Super Admin holatini o'zgartirib bo'lmaydi."}, status=403)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({ 'success': True, 'is_active': user.is_active,
                              'status_display': 'Faol' if user.is_active else 'Faol emas' })
    raise Http404

# --- API Views (Misollar) ---
@login_required
@user_passes_test(is_admin_or_superadmin) # Yoki ariza egasi
def application_details_api(request, pk):
     # Bu funksiya all_applications.html dagi "Ko'rish" tugmasi uchun ishlatiladi
     application = get_object_or_404(
         Application.objects.select_related('applicant__profile', 'scholarship')
         .prefetch_related('documents'), # Hujjatlarni yuklaymiz
         pk=pk
     )
     # Ruxsatni tekshirish (faqat admin yoki ariza egasi ko'rsin)
     if not (is_admin_or_superadmin(request.user) or application.applicant == request.user):
         return JsonResponse({'error': 'Ruxsat yo\'q'}, status=403)

     documents_data = [{
         'url': doc.file.url,
         'type_display': doc.get_document_type_display(),
         'filename': doc.file.name.split('/')[-1] # Fayl nomini olish
     } for doc in application.documents.all()]

     status_badge_html = f'<span class="status-badge status-{application.status}"><i class="fa-solid fa-..."></i> {application.get_status_display()}</span>' # Ikonkani to'g'rilash kerak

     data = {
         'id': application.id,
         'applicant_name': application.applicant_full_name or application.applicant.get_full_name(),
         'applicant_email': application.applicant_email or application.applicant.email,
         'scholarship_name': application.scholarship.name,
         'status_display': application.get_status_display(),
         'status_badge_html': status_badge_html, # Buni JSda generatsiya qilish ham mumkin
         'submission_date': application.submission_date.strftime('%Y-%m-%d %H:%M'),
         'last_updated': application.last_updated.strftime('%Y-%m-%d %H:%M'),
         'review_notes': application.review_notes,
         'documents': documents_data,
         # Qolgan kerakli ma'lumotlar...
     }
     return JsonResponse(data)


@login_required
@user_passes_test(is_admin_or_superadmin)
def application_change_status_api(request, pk):
     # Bu funksiya all_applications.html dagi status o'zgartirish tugmalari uchun
     if request.method == 'POST':
         application = get_object_or_404(Application, pk=pk)
         try:
             data = json.loads(request.body) # JSON bodydan ma'lumotlarni olish
             new_status = data.get('status')
             new_notes = data.get('notes', '')

             if new_status not in [choice[0] for choice in Application.STATUS_CHOICES]:
                 return JsonResponse({'success': False, 'error': 'Noto\'g\'ri status'}, status=400)

             application.status = new_status
             # Agar yangi izoh bo'lsa, eskilariga qo'shish yoki almashtirish
             if new_notes:
                 application.review_notes = f"{application.review_notes}\n---\nAdmin ({request.user.username} - {timezone.now().strftime('%Y-%m-%d %H:%M')}):\n{new_notes}" if application.review_notes else f"Admin ({request.user.username} - {timezone.now().strftime('%Y-%m-%d %H:%M')}):\n{new_notes}"

             application.save()

             # Ariza beruvchiga bildirishnoma yuborish (ixtiyoriy)
             Notification.objects.create(
                 user=application.applicant,
                 message=f"'{application.scholarship.name}' stipendiyasi uchun arizangiz (#{application.id}) holati o'zgardi: {application.get_status_display()}" + (f"\nIzoh: {new_notes[:100]}..." if new_notes else ""),
                 # link=reverse('my_applications') # Yoki ariza detail view
             )

             status_badge_html = f'<span class="status-badge status-{application.status}"><i class="fa-solid fa-..."></i> {application.get_status_display()}</span>' # Ikonkani to'g'rilash kerak

             return JsonResponse({
                 'success': True,
                 'new_status': application.status,
                 'new_status_display': application.get_status_display(),
                 'status_badge_html': status_badge_html
             })
         except json.JSONDecodeError:
             return JsonResponse({'success': False, 'error': 'Noto\'g\'ri JSON format'}, status=400)
         except Exception as e:
             return JsonResponse({'success': False, 'error': f'Server xatosi: {e}'}, status=500)
     raise Http404