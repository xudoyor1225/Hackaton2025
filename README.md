# 🚀 SHAFFOF IMKONIYAT 

[![Litsenziya](https://img.shields.io/badge/Litsenziya-MIT-blue.svg)](https://opensource.org/licenses/MIT) 
[![Python Versiyasi](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django Versiyasi](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/) 

**Talabalar uchun grantlar (stipendiyalar) topish, ularga ariza topshirish va arizalar holatini kuzatish imkonini beruvchi veb-platforma. Administratorlar uchun grantlarni va foydalanuvchilarni boshqarish vositalari mavjud.**

Loyiha skrinshoti]![image](https://github.com/user-attachments/assets/8bc7d4ac-be71-40bd-bf9e-d8462abe37f3)
(images/screenshot.png) 
       ![image](https://github.com/user-attachments/assets/18cc5f6b-b1ca-4a60-a5d4-683e2ca9fe4f)
       ![image](https://github.com/user-attachments/assets/7822a632-266b-4f89-83f4-e5cda5591fea)
       ![image](https://github.com/user-attachments/assets/de47103a-b6fb-4896-8944-fff4320ac810)
       ![image](https://github.com/user-attachments/assets/58ea4fa6-080a-4be7-8af5-6d25ea6ce396)





---

## 📖 Mundarija

*   [🌟 Loyiha Haqida](#-loyiha-haqida)
    *   [🛠️ Texnologiyalar](#️-texnologiyalar)
    *   [🎯 Asosiy Xususiyatlar](#-asosiy-xususiyatlar)
*   [⚙️ Boshlash](#️-boshlash)
    *   [📋 Talablar](#-talablar)
    *   [🚀 O'rnatish](#-o'rnatish)
*   [💻 Foydalanish](#-foydalanish)
    *   [🔑 Autentifikatsiya](#-autentifikatsiya)
    *   [👤 Foydalanuvchi Sahifalari](#-foydalanuvchi-sahifalari)
    *   [👑 Admin Sahifalari](#-admin-sahifalari)
*   [🔌 API Endpoints](#-api-endpoints)
*   [📁 Fayl Strukturasi](#-fayl-strukturasi)
*   [🤝 Hissa Qo'shish](#-hissa-qoshish)
*   [📄 Litsenziya](#-litsenziya)
*   [📧 Bog'lanish](#-boglanish)
*   [🙏 Minnatdorchilik](#-minnatdorchilik-ixtiyoriy)

---

## 🌟 Loyiha Haqida

Ushbu loyiha talabalarga mos grantlarni topish jarayonini osonlashtirish va ariza topshirishni markazlashtirish maqsadida ishlab chiqilgan. Platforma quyidagi imkoniyatlarni taqdim etadi: grantlar bazasini ko'rish, filtrlash, onlayn ariza to'ldirish va topshirilgan arizalar statusini kuzatib borish. Shuningdek, platforma administratorlari uchun grantlarni, arizalarni va foydalanuvchilarni boshqarish uchun qulay interfeys mavjud.

### 🛠️ Texnologiyalar

Loyiha quyidagi texnologiyalar yordamida qurilgan:

*   **Backend:**
    *   ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
    *   ![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white) <!-- Django versiyasini aniqlashtiring -->
    *   ![SQLite3](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white) (Rivojlantirish uchun)
*   **Frontend:**
    *   ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
    *   ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
    *   ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) ( AJAX so'rovlari va interaktiv elementlar uchun)
    *   ![Chart.js](https://www.chartjs.org/) yoki boshqa diagramma kutubxonasi (`analytics` sahifasi uchun)
*   **Virtual Muhit:** `venv` (yoki sizning `virtualm`)

### 🎯 Asosiy Xususiyatlar

*   🔐 **Foydalanuvchi Autentifikatsiyasi:** Ro'yxatdan o'tish, xavfsiz tizimga kirish va chiqish.
*   📊 **Foydalanuvchi Paneli (Dashboard):** Umumiy ma'lumotlar va tezkor havolalar.
*   📈 **Analitika Sahifasi:** Arizalar yoki boshqa statistikalar vizualizatsiyasi.
*   🎓 **Grantlarni Qidirish:** Mavjud grantlarni qidirish va filtrlash imkoniyati.
*   📝 **Onlayn Ariza Topshirish:** Tanlangan grantga ariza to'ldirish va yuborish.
*   📄 **Mening Arizalarim:** Foydalanuvchi topshirgan arizalar ro'yxati va ularning statusi.
*   ⚙️ **Sozlamalar:** Profil ma'lumotlarini va xavfsizlik parametrlarini (parol) o'zgartirish.
*   🆘 **Yordam Markazi:** Foydalanuvchilar uchun qo'llanma yoki yordam sahifasi.
*   👑 **Admin Imkoniyatlari:**
    *   📑 Barcha arizalarni ko'rish va statusini o'zgartirish.
    *   💰 Grantlarni boshqarish (yaratish, tahrirlash, aktiv/nofaol qilish).
    *   👥 Foydalanuvchilarni boshqarish (yaratish, tahrirlash, bloklash/aktivlashtirish).
*   🔌 **API Endpointlari:** Frontend qismining backend bilan dinamik aloqasi uchun (AJAX).

---

## ⚙️ Boshlash

Loyihani mahalliy kompyuteringizda ishga tushirish uchun quyidagi amallarni bajaring.

### 📋 Talablar

Loyihani ishga tushirishdan oldin quyidagilar o'rnatilganligiga ishonch hosil qiling:

*   **Python:** Versiya 3.10 yoki undan yuqori. [Python rasmiy sayti](https://www.python.org/downloads/).
*   **pip:** Python paket menejeri.
*   **Git:** Versiyalarni boshqarish tizimi. [Git rasmiy sayti](https://git-scm.com/downloads/).

### 🚀 O'rnatish

1.  **Repository'ni klonlash (nusxalash):**
    ```bash
    git clone [SIZNING_REPOSITORY_HAVOLANGIZ] # GitHub/GitLab havolangizni shu yerga qo'ying
    cd hakaton # Yoki sizning loyiha papkangiz nomi
    ```
    *(Agar hali repository'ga yuklamagan bo'lsangiz, bu qadamni tashlab, keyingi qadamdan boshlang).*

2.  **Virtual muhitni aktivlashtirish:**
    ```bash
    # Linux/macOS uchun:
    source virtualm/bin/activate
    # Windows (Command Prompt) uchun:
    .\virtualm\Scripts\activate
    # Windows (PowerShell) uchun:
    .\virtualm\Scripts\Activate.ps1
    ```
    *(Agar `virtualm` ishlamasa, `python -m venv venv` bilan yangi muhit yarating va `venv` bilan aktivlashtiring).*


3.  **Kerakli paketlarni o'rnatish:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ma'lumotlar bazasi migratsiyalarini qo'llash:**
    ```bash
    python manage.py migrate
    ```

5.  **(Ixtiyoriy lekin Tavsiya Etiladi) Superuser (administrator) yaratish:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Rivojlantirish serverini ishga tushirish:**
    ```bash
    python manage.py runserver
    ```

7.  **🎉 Tayyor!** Brauzeringizda [http://127.0.0.1:8000/](http://127.0.0.1:8000/) manzilini oching.

---

## 💻 Foydalanish

Server ishga tushgandan so'ng, platformaning turli qismlariga quyidagi manzillar orqali kirishingiz mumkin:

### 🔑 Autentifikatsiya

*   `/login/`: Tizimga kirish sahifasi.
*   `/register/`: Yangi foydalanuvchini ro'yxatdan o'tkazish.
*   `/logout/`: Tizimdan chiqish.

### 👤 Foydalanuvchi Sahifalari

*   `/` (yoki `/dashboard/`): Asosiy boshqaruv paneli.
*   `/analytics/`: Statistika va analitika sahifasi.
*   `/scholarships/find/`: Grantlarni qidirish sahifasi.
*   `/apply/`: Tanlangan grantga ariza topshirish sahifasi.
*   `/my-applications/`: Foydalanuvchi topshirgan arizalar ro'yxati.
*   `/settings/profile/`: Profil sozlamalari.
*   `/settings/security/`: Parolni o'zgartirish kabi xavfsizlik sozlamalari.
*   `/help-center/`: Yordam markazi yoki qo'llanmalar.

### 👑 Admin Sahifalari

*(Bu sahifalarga kirish uchun odatda superuser yoki maxsus ruxsatlar kerak bo'ladi)*

*   `/applications/all/`: Barcha topshirilgan arizalar ro'yxati.
*   `/manage/scholarships/`: Grantlarni boshqarish interfeysi (yaratish, tahrirlash).
*   `/manage/users/`: Foydalanuvchilarni boshqarish interfeysi.
*   `/admin/`: Standart Django admin paneli (agar sozlanagan bo'lsa).

---

## 🔌 API Endpoints

Loyiha frontend qismi (JavaScript) bilan ma'lumot almashish uchun quyidagi asosiy API endpointlaridan foydalanadi:

*   **Arizalar (Applications):**
    *   `GET /api/applications/<int:pk>/details/`: Ariza tafsilotlarini olish.
    *   `POST /api/applications/<int:pk>/change-status/`: Ariza statusini o'zgartirish (masalan, "Ko'rib chiqilmoqda", "Tasdiqlandi", "Rad etildi").
*   **Grantlar (Scholarships):**
    *   `POST /api/scholarships/create/`: Yangi grant yaratish.
    *   `PUT /api/scholarships/update/<int:pk>/`: Mavjud grantni tahrirlash/yangilash.
    *   `POST /api/scholarships/toggle-status/<int:pk>/`: Grantni aktiv yoki nofaol qilish.
*   **Foydalanuvchilar (Users):**
    *   `POST /api/users/create-update/`: Yangi foydalanuvchi yaratish yoki mavjudini tahrirlash (admin tomonidan).
    *   `GET /api/users/details/<int:pk>/`: Foydalanuvchi ma'lumotlarini olish.
    *   `POST /api/users/toggle-status/<int:pk>/`: Foydalanuvchini aktivlashtirish yoki bloklash.

*(Bu endpointlar odatda sahifani yangilamasdan ma'lumotlarni olish yoki o'zgartirish uchun AJAX so'rovlari orqali chaqiriladi).*

