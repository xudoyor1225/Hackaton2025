from django.db import models

# Create your models here.
# models.py

from django.db import models
from django.conf import settings # settings.AUTH_USER_MODEL ni ishlatish uchun
from django.utils import timezone # Vaqt bilan ishlash uchun

# --- Foydalanuvchi Profili ---
# Django'ning standart User modelini kengaytirish uchun
class Profile(models.Model):
    # Rol tanlovlari (users.html va data.js dagi qiymatlarga mos kelishi mumkin)
    ROLE_CHOICES = (
        ('applicant', 'Ariza beruvchi'),
        ('reviewer', 'Tekshiruvchi'),
        ('admin', 'Administrator'),
        ('superadmin', 'Super Admin'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant', verbose_name="Rol")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Avatar")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefon raqami")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    iin = models.CharField(max_length=14, null=True, blank=True, verbose_name="JShShIR") # JShShIR (14 raqam)
    address = models.TextField(null=True, blank=True, verbose_name="Yashash manzili")
    # Status User.is_active orqali boshqariladi

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

# --- Stipendiyalar ---
class Scholarship(models.Model):
    # Stipendiya turi tanlovlari (manage_scholarships.html modaliga mos)
    TYPE_CHOICES = (
        ('international', 'Xalqaro'),
        ('state', 'Davlat'),
        ('private', 'Xususiy'),
        ('regional', 'Mintaqaviy'),
        ('corporate', 'Korporativ'),
    )
    # Holat tanlovlari (manage_scholarships.html modaliga mos)
    STATUS_CHOICES = (
        ('active', 'Faol'),
        ('completed', 'Tugallangan'),
        ('draft', 'Qoralama'),
    )
    # Soha tanlovlari (find_scholarships.html filtriga mos, kengaytirish mumkin)
    FIELD_CHOICES = (
        ('all', 'Barcha mutaxassisliklar'),
        ('technical_natural', 'Texnik, Tabiiy fanlar'),
        ('humanities_art', 'Gumanitar fanlar, San\'at'),
        ('social', 'Ijtimoiy ahamiyatga ega'),
        ('science_culture_art', 'Fan, Madaniyat, San\'at'),
        ('it', 'Axborot texnologiyalari'),
        ('agriculture', 'Qishloq xo\'jaligi'),
        ('engineering_geology', 'Muhandislik, Geologiya'),
        # ... boshqa sohalar
    )

    name = models.CharField(max_length=255, verbose_name="Stipendiya nomi")
    provider = models.CharField(max_length=255, verbose_name="Ta'minotchi")
    description = models.TextField(verbose_name="Tavsif va Talablar")
    amount = models.CharField(max_length=100, verbose_name="Miqdori/Qoplash") # "To'liq qoplash" kabi matnlar bo'lishi mumkin
    deadline = models.DateField(verbose_name="Topshirish muddati")
    field = models.CharField(max_length=100, choices=FIELD_CHOICES, verbose_name="Soha/Mutaxassisliklar") # Yoki TextField
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Stipendiya turi")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft', verbose_name="Holati")
    popular = models.BooleanField(default=False, verbose_name="Ommabop")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Stipendiya"
        verbose_name_plural = "Stipendiyalar"
        ordering = ['-created_at'] # Sukut bo'yicha saralash

# --- Arizalar ---
class Application(models.Model):
    # Holat tanlovlari (all_applications.html filtriga mos)
    STATUS_CHOICES = (
        ('submitted', 'Yuborilgan'),
        ('reviewing', 'Ko\'rib chiqilmoqda'),
        ('clarification', 'Aniqlashtirish talab etiladi'),
        ('approved', 'Ma\'qullangan'),
        ('rejected', 'Rad etilgan'),
        ('withdrawn', 'Qaytarib olingan'), # Foydalanuvchi o'zi qaytarib olsa
    )

    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications', verbose_name="Ariza beruvchi")
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications', verbose_name="Stipendiya")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan sana") # dashboard.html dagi 'date'
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Oxirgi yangilanish") # all_applications.html dagi 'updateDate'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', verbose_name="Holati")
    review_notes = models.TextField(null=True, blank=True, verbose_name="Ko'rib chiquvchi izohlari") # all_applications.html dagi 'Tekshiruvchi izohlari'

    # --- Ariza topshirishdagi ma'lumotlar (submit_aplications.html dan) ---
    # (Bu ma'lumotlar Profile'da ham bo'lishi mumkin, lekin ariza paytidagi holatni saqlash uchun bu yerga qo'shildi)
    applicant_full_name = models.CharField(max_length=255, verbose_name="Ariza beruvchi F.I.Sh.")
    applicant_birth_date = models.DateField(verbose_name="Ariza beruvchi tug'ilgan sana")
    applicant_iin = models.CharField(max_length=14, verbose_name="Ariza beruvchi JShShIR")
    applicant_phone = models.CharField(max_length=20, verbose_name="Ariza beruvchi telefoni")
    applicant_email = models.EmailField(verbose_name="Ariza beruvchi email")
    applicant_address = models.TextField(verbose_name="Ariza beruvchi manzili")

    university = models.CharField(max_length=255, verbose_name="Ta'lim muassasasi")
    faculty = models.CharField(max_length=255, verbose_name="Fakultet/Mutaxassislik")
    course = models.PositiveSmallIntegerField(verbose_name="Kurs/O'quv yili")
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="O'rtacha baho (GPA)") # 5.00 format
    achievements = models.TextField(null=True, blank=True, verbose_name="Yutuqlar va Tajriba")
    essay = models.TextField(null=True, blank=True, verbose_name="Esse")

    confirm_accuracy = models.BooleanField(default=False, verbose_name="To'g'rilik tasdiqlangan")
    confirm_terms = models.BooleanField(default=False, verbose_name="Shartlarga rozilik bildirilgan")

    def __str__(self):
        return f"Ariza #{self.id} - {self.applicant.username} uchun {self.scholarship.name}"

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"
        ordering = ['-submission_date']

# --- Arizaga biriktirilgan hujjatlar ---
class Document(models.Model):
    # Hujjat turi (submit_aplications.html ga mos)
    DOC_TYPE_CHOICES = (
        ('id_card', 'Shaxsni tasdiqlovchi hujjat/Pasport'),
        ('transcript', 'Baho daftarchasi/Attestat'),
        ('motivation', 'Motivatsion xat'),
        ('recommendation', 'Tavsiyanoma'),
        ('other', 'Boshqa'),
    )

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents', verbose_name="Ariza")
    document_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, verbose_name="Hujjat turi")
    file = models.FileField(upload_to='application_documents/', verbose_name="Fayl")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan sana")

    def __str__(self):
        return f"{self.get_document_type_display()} - Ariza #{self.application.id}"

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"

# --- FAQ (Yordam Markazi uchun) ---
# (help_center.html dan kelib chiqib)
class FAQItem(models.Model):
    question = models.CharField(max_length=255, verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ Savol-Javob"
        verbose_name_plural = "FAQ Savol-Javoblar"
        ordering = ['order']

# --- Bildirishnomalar (ixtiyoriy, lekin ko'p sahifalarda ko'rsatilgan) ---
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name="Foydalanuvchi")
    message = models.TextField(verbose_name="Xabar matni")
    link = models.URLField(null=True, blank=True, verbose_name="Havola") # Bildirishnomani bosganda o'tish uchun
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def __str__(self):
        return f"{self.user.username} uchun bildirishnoma"

    class Meta:
        verbose_name = "Bildirishnoma"
        verbose_name_plural = "Bildirishnomalar"
        ordering = ['-created_at']