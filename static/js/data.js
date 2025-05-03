// js/data.js

const demoApplicants = [
    { id: 1, avatar: 'https://i.pravatar.cc/40?img=11', name: 'Aliya Beketova', email: 'aliya.b@example.com', role: 'Ariza beruvchi', registered: '2024-03-10', status: 'Faol' },
    { id: 2, avatar: 'https://i.pravatar.cc/40?img=7', name: 'Marat Sadiqov', email: 'marat.s@example.com', role: 'Ariza beruvchi', registered: '2024-03-12', status: 'Faol' },
    { id: 3, avatar: 'https://i.pravatar.cc/40?img=5', name: 'Gulnara Isayeva', email: 'gulnara.i@example.com', role: 'Ariza beruvchi', registered: '2024-03-15', status: 'Faol' },
    { id: 4, avatar: 'https://i.pravatar.cc/40?img=8', name: 'Yerlan Jumabayev', email: 'erlan.j@example.com', role: 'Ariza beruvchi', registered: '2024-03-18', status: 'Faol' },
    { id: 5, avatar: 'https://i.pravatar.cc/40?img=2', name: 'Dinara Karimova', email: 'dinara.k@example.com', role: 'Administrator', registered: '2024-02-01', status: 'Faol' },
    { id: 6, avatar: 'https://i.pravatar.cc/40?img=9', name: 'Nurlan Ospanov', email: 'nurlan.o@example.com', role: 'Ariza beruvchi', registered: '2024-04-01', status: 'Faol' },
    { id: 7, avatar: 'https://i.pravatar.cc/40?img=6', name: 'Janar Axmetova', email: 'zhanar.a@example.com', role: 'Ariza beruvchi', registered: '2024-04-05', status: 'Faol' },
    { id: 8, avatar: 'https://i.pravatar.cc/40?img=3', name: 'Bauirjan Temirbekov', email: 'baur.t@example.com', role: 'Ariza beruvchi', registered: '2024-04-10', status: 'Faol emas' },
    { id: 9, avatar: 'https://i.pravatar.cc/40?img=4', name: 'Aydos Erbolatov', email: 'aidos.e@example.com', role: 'Super Admin', registered: '2024-01-15', status: 'Faol' },
    { id: 10, avatar: 'https://i.pravatar.cc/40?img=10', name: 'Sanjar Mirzagali', email: 'sanzhar.m@example.com', role: 'Tekshiruvchi', registered: '2024-02-20', status: 'Faol' },
];

const demoScholarships = [
    { id: 1, name: 'Prezidentning "Bolashaq" stipendiyasi', provider: '"Xalqaro dasturlar markazi" AJ', deadline: '2024-09-15', amount: 'To\'liq qoplash', field: 'Barcha mutaxassisliklar', type: 'Xalqaro', popular: true, status: 'Faol' },
    { id: 2, name: 'Qozog\'iston Respublikasi Ta\'lim va Fan Vazirligi Granti', provider: 'Qozog\'iston Respublikasi Ta\'lim va Fan Vazirligi', deadline: '2024-07-31', amount: 'To\'liq qoplash', field: 'Texnika, Tabiiy fanlar', type: 'Davlat', popular: true, status: 'Faol' },
    { id: 3, name: 'Abay nomidagi stipendiya', provider: '"Abay" jamg\'armasi', deadline: '2024-08-20', amount: '50 000 tenge/oy', field: 'Gumanitar fanlar, San\'at', type: 'Xususiy', popular: false, status: 'Faol' },
    { id: 4, name: 'Ostona shahri Munitsipal stipendiyasi', provider: 'Ostona shahar Hokimligi', deadline: '2024-10-01', amount: '35 000 tenge/oy', field: 'Ijtimoiy ahamiyatga ega', type: 'Hududiy', popular: false, status: 'Faol' },
    { id: 5, name: 'Birinchi Prezident Jamg\'armasi', provider: 'Nursulton Nazarboyev Jamg\'armasi', deadline: '2024-09-01', amount: 'Turli xil', field: 'Fan, Madaniyat, San\'at', type: 'Xususiy', popular: true, status: 'Faol' },
    { id: 6, name: '"Tech Orda" IT-Granti', provider: 'Astana Hub', deadline: '2024-08-10', amount: '600 000 tengegacha', field: 'Axborot texnologiyalari', type: 'Xususiy', popular: false, status: 'Faol' },
    { id: 7, name: '"Keng-Dala" stipendiyasi', provider: '"KazAgroFinance" AJ', deadline: '2024-06-30', amount: '40 000 tenge/oy', field: 'Qishloq xo\'jaligi', type: 'Korporativ', popular: false, status: 'Yakunlangan' },
    { id: 8, name: 'Chevron stipendiyasi', provider: 'Chevron Korporatsiyasi', deadline: '2024-11-01', amount: 'To\'liq qoplash + stajirovka', field: 'Muhandislik, Geologiya', type: 'Korporativ', popular: true, status: 'Faol' },
];

const demoApplications = [
    { id: 1, applicantId: 1, scholarshipId: 1, date: '2024-05-15', status: 'Ma\'qullangan', reviewNotes: 'A\'lo GPA ko\'rsatkichlari va motivatsion xat.', updateDate: '2024-05-25' },
    { id: 2, applicantId: 2, scholarshipId: 2, date: '2024-05-18', status: 'Ko\'rib chiqilmoqda', reviewNotes: null, updateDate: '2024-05-18' },
    { id: 3, applicantId: 3, scholarshipId: 3, date: '2024-05-12', status: 'Rad etilgan', reviewNotes: 'O\'qish yo\'nalishi bo\'yicha talablarga mos kelmaslik.', updateDate: '2024-05-20' },
    { id: 4, applicantId: 4, scholarshipId: 4, date: '2024-05-20', status: 'Yuborilgan', reviewNotes: null, updateDate: '2024-05-20' },
    { id: 5, applicantId: 1, scholarshipId: 5, date: '2024-05-14', status: 'Aniqlashtirish talab etiladi', reviewNotes: 'Ko\'ngillilik faoliyatini tasdiqlovchi hujjat taqdim etish kerak.', updateDate: '2024-05-22' },
    { id: 6, applicantId: 6, scholarshipId: 1, date: '2024-05-19', status: 'Ko\'rib chiqilmoqda', reviewNotes: null, updateDate: '2024-05-19' },
    { id: 7, applicantId: 7, scholarshipId: 3, date: '2024-05-11', status: 'Ma\'qullangan', reviewNotes: 'Portfolio bo\'yicha yuqori ball.', updateDate: '2024-05-19' },
    { id: 8, applicantId: 2, scholarshipId: 6, date: '2024-05-21', status: 'Yuborilgan', reviewNotes: null, updateDate: '2024-05-21' },
    { id: 9, applicantId: 4, scholarshipId: 2, date: '2024-05-22', status: 'Ko\'rib chiqilmoqda', reviewNotes: null, updateDate: '2024-05-22' },
    { id: 10, applicantId: 3, scholarshipId: 8, date: '2024-05-10', status: 'Rad etilgan', reviewNotes: 'Ingliz tili darajasi past.', updateDate: '2024-05-18' },
    { id: 11, applicantId: 6, scholarshipId: 5, date: '2024-05-23', status: 'Yuborilgan', reviewNotes: null, updateDate: '2024-05-23' },
    { id: 12, applicantId: 7, scholarshipId: 2, date: '2024-05-24', status: 'Aniqlashtirish talab etiladi', reviewNotes: 'Tavsiyanoma mavjud emas.', updateDate: '2024-05-28' },
    // Добавьте больше данных для пагинации и разнообразия
];

// Функция для получения данных по ID (имитация запроса)
function findApplicant(id) {
    return demoApplicants.find(a => a.id === id);
}

function findScholarship(id) {
    return demoScholarships.find(s => s.id === id);
}

// Данные для аналитики (могут генерироваться на основе demoApplications)
const analyticsData = {
    applicationsByStatus: {
        labels: ['Ma\'qullangan', 'Ko\'rib chiqilmoqda', 'Rad etilgan', 'Yuborilgan', 'Aniqlashtirish talab etiladi'],
        data: [
            demoApplications.filter(d => d.status === 'Ma\'qullangan').length, // Updated status string
            demoApplications.filter(d => d.status === 'Ko\'rib chiqilmoqda').length, // Updated status string
            demoApplications.filter(d => d.status === 'Rad etilgan').length, // Updated status string
            demoApplications.filter(d => d.status === 'Yuborilgan').length, // Updated status string
            demoApplications.filter(d => d.status === 'Aniqlashtirish talab etiladi').length, // Updated status string
        ]
    },
    applicationsOverTime: {
        // Пример данных: помесячно за полгода
        labels: ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyn'], // Translated month abbreviations
        datasets: [
            { label: 'Yuborildi', data: [15, 25, 40, 55, 70, 65], borderColor: '#6366F1', tension: 0.3, pointRadius: 4, pointBackgroundColor: '#6366F1' }, // Translated label
            { label: 'Ma\'qullandi', data: [5, 8, 12, 18, 22, 20], borderColor: '#10B981', tension: 0.3, pointRadius: 4, pointBackgroundColor: '#10B981' }, // Translated label
            { label: 'Rad etildi', data: [2, 4, 7, 10, 15, 13], borderColor: '#EF4444', tension: 0.3, pointRadius: 4, pointBackgroundColor: '#EF4444' } // Translated label
        ]
    },
    successRateByScholarshipType: {
        labels: ['Davlat', 'Xalqaro', 'Xususiy', 'Hududiy', 'Korporativ'], // Translated labels
        // Процент одобренных от поданных (нужно посчитать из demoApplications) - пока заглушки
        data: [65, 75, 50, 60, 70]
    },
    userRoles: {
        labels: ['Ariza beruvchi', 'Administrator', 'Super Admin', 'Tekshiruvchi', 'Faol emas'], // Translated labels
        data: [
            demoApplicants.filter(u => u.role === 'Ariza beruvchi' && u.status === 'Faol').length, // Updated role and status strings
            demoApplicants.filter(u => u.role === 'Administrator').length, // Updated role string
            demoApplicants.filter(u => u.role === 'Super Admin').length, // Updated role string
            demoApplicants.filter(u => u.role === 'Tekshiruvchi').length, // Updated role string
            demoApplicants.filter(u => u.status === 'Faol emas').length, // Updated status string
        ]
    }
};

// Данные для FAQ
const faqData = [
    { q: 'Stipendiyaga qanday ariza topshirish mumkin?', a: '"Stipendiyalarni Topish" bo\'limiga o\'ting, sizni qiziqtirgan dasturni tanlang va "Ariza Yuborish" tugmasini bosing. Anketaning barcha kerakli maydonlarini to\'ldiring va hujjatlarni biriktiring.' },
    { q: 'Odatda qanday hujjatlar talab qilinadi?', a: 'Standart to\'plam shaxsni tasdiqlovchi hujjat, ilovasi bilan attestat/diplom, motivatsion xat, tavsiyanomalar, yutuqlar to\'g\'risidagi ma\'lumotnomalarni (agar mavjud bo\'lsa) o\'z ichiga oladi. Aniq ro\'yxat muayyan stipendiyaga bog\'liq.' },
    { q: 'Arizamning holatini qanday bilsam bo\'ladi?', a: 'Arizangiz holati "Mening Arizalarim" bo\'limida ko\'rsatiladi. Shuningdek, holat o\'zgarishi haqida elektron pochtangizga bildirishnomalar olasiz.' },
    { q: 'Yuborilgan arizani tahrirlay olamanmi?', a: 'Arizani yuborgandan keyin tahrirlash odatda mumkin emas. Yuborishdan oldin barcha ma\'lumotlarni diqqat bilan tekshiring. Agar jiddiy o\'zgartirishlar kiritish kerak bo\'lsa, qo\'llab-quvvatlash xizmatiga murojaat qiling.' },
    { q: 'Agar ariza holati "Aniqlashtirish talab etiladi" bo\'lsa, nima qilish kerak?', a: 'Ariza tafsilotlarida ("Mening Arizalarim" bo\'limi) tekshiruvchining izohini diqqat bilan o\'qing. Odatda qo\'shimcha hujjatlar taqdim etish yoki xatolarni tuzatish talab qilinadi. Buni imkon qadar tezroq bajaring.' },
    { q: 'Parolni qanday tiklash mumkin?', a: 'Kirish sahifasida "Parolni unutdingizmi?" havolasini bosing. Elektron pochtangizga yuborilgan ko\'rsatmalarga amal qiling.' }
];