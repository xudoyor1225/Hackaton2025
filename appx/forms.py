# forms.py

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    AuthenticationForm,
    PasswordChangeForm
)
from django.contrib.auth.models import User
from django.db import transaction
from .models import Profile, Scholarship, Application, Document

# --- Ro'yxatdan o'tish uchun Forma ---
class RegistrationForm(BaseUserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Ism")
    last_name = forms.CharField(max_length=150, required=True, label="Familiya")
    email = forms.EmailField(required=True, label="Email manzil")

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = BaseUserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu email manzili allaqachon ro'yxatdan o'tgan.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.is_active = True # Yangi user faol bo'lsin
        if commit:
            user.save()
            Profile.objects.create(user=user, role='applicant') # Sukut bo'yicha 'applicant'
        return user

# --- Login uchun Forma (Standart AuthenticationForm ni ishlatsak ham bo'ladi) ---
class CustomAuthenticationForm(AuthenticationForm):
    pass # O'zgartirishlar kerak bo'lmasa, bo'sh qoldiring

# --- Profilni tahrirlash uchun forma ---
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'phone', 'birth_date', 'iin', 'address')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

# --- User ma'lumotlarini tahrirlash uchun (profile_settings uchun) ---
class CustomUserChangeForm(forms.ModelForm):
     first_name = forms.CharField(max_length=150, required=False, label="Ism")
     last_name = forms.CharField(max_length=150, required=False, label="Familiya")
     # Emailni o'zgartirishga ruxsat berilmasa, read-only qilish mumkin
     # email = forms.EmailField(required=True, disabled=True)

     class Meta:
         model = User
         fields = ('first_name', 'last_name')

# --- Stipendiya qo'shish/tahrirlash uchun forma ---
class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ('name', 'provider', 'description', 'amount', 'deadline', 'field', 'type', 'status', 'popular')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'amount': "Masalan: To'liq qoplash / 1 000 000 so'm/oy",
            'popular': '"Ommabop" stipendiyalarni asosiy sahifada ajratib ko\'rsatish uchun.',
        }
        labels = { # O'zbekcha nomlar
            'name': "Stipendiya nomi",
            'provider': "Ta'minotchi",
            'description': "Tavsif va Talablar",
            'amount': "Miqdori/Qoplash",
            'deadline': "Topshirish muddati",
            'field': "Soha/Mutaxassisliklar",
            'type': "Stipendiya turi",
            'status': "Holati",
            'popular': "Ommabop"
        }


# --- Ariza yuborish formasi ---
class ApplicationForm(forms.ModelForm):
    # Hujjatlar
    doc_id_file = forms.FileField(label="Shaxsni tasdiqlovchi hujjat/Pasport", required=True, help_text="PDF, JPG, PNG (maks. 5MB)", widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}))
    doc_transcript_file = forms.FileField(label="Baho daftarchasi/Attestat", required=True, help_text="PDF (maks. 5MB)", widget=forms.ClearableFileInput(attrs={'accept': '.pdf'}))
    doc_motivation_file = forms.FileField(label="Motivatsion xat", required=True, help_text="PDF, DOCX (maks. 5MB)", widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.docx'}))
    doc_recommendation_file = forms.FileField(label="Tavsiyanoma (ixtiyoriy)", required=False, help_text="PDF (maks. 5MB)", widget=forms.ClearableFileInput(attrs={'accept': '.pdf'}))
    # Tasdiqlash
    confirm_accuracy = forms.BooleanField(label="Barcha ma'lumotlarning toʻgʻriligini tasdiqlayman.", required=True)
    confirm_terms = forms.BooleanField(label="Ma'lumotlarni qayta ishlash shartlariga roziman.", required=True)

    class Meta:
        model = Application
        fields = [
            'applicant_full_name', 'applicant_birth_date', 'applicant_iin',
            'applicant_phone', 'applicant_email', 'applicant_address',
            'university', 'faculty', 'course', 'gpa', 'achievements',
            'essay',
            # Checkboxlar va fayllar alohida
        ]
        widgets = {
            'applicant_birth_date': forms.DateInput(attrs={'type': 'date'}),
            'applicant_address': forms.Textarea(attrs={'rows': 3}),
            'achievements': forms.Textarea(attrs={'rows': 5}),
            'essay': forms.Textarea(attrs={'rows': 8}),
        }
        labels = { # O'zbekcha nomlar
            'applicant_full_name': "Toʻliq ism (F.I.Sh.)",
            'applicant_birth_date': "Tugʻilgan sana",
            'applicant_iin': "JShShIR",
            'applicant_phone': "Bogʻlanish telefoni",
            'applicant_email': "Bogʻlanish uchun Email",
            'applicant_address': "Yashash manzili",
            'university': "Ta'lim muassasasi",
            'faculty': "Fakultet/Mutaxassislik",
            'course': "Kurs/Oʻquv yili",
            'gpa': "Oʻrtacha baho (GPA)",
            'achievements': "Yutuqlar va Tajriba",
            'essay': "Esse (agar talab qilinsa)",
        }

# --- Foydalanuvchi qo'shish/tahrirlash uchun forma ---
class UserForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(max_length=150, required=True, label="Toʻliq ism")
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True, label="Rol")
    is_active = forms.BooleanField(required=False, label="Faol", initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})) # Bootstrap uchun class
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Parol", min_length=8, help_text="O'zgartirmaslik uchun bo'sh qoldiring (kamida 8 belgi).")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.cleaned_data.get('user_id')
        query = User.objects.filter(email__iexact=email)
        if user_id:
            query = query.exclude(pk=user_id)
        if query.exists():
            raise forms.ValidationError("Bu email manzili allaqachon ro'yxatdan o'tgan.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        user_id = self.cleaned_data.get('user_id')
        if not user_id and not password:
            raise forms.ValidationError("Yangi foydalanuvchi uchun parol kiritilishi shart.")
        if password and len(password) < 8:
             raise forms.ValidationError("Parol kamida 8 belgidan iborat bo'lishi kerak.")
        # Murakkablikni tekshirish (ixtiyoriy)
        # import re
        # if password and not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', password):
        #     raise forms.ValidationError("Parolda kichik, katta harf va raqam bo'lishi kerak.")
        return password