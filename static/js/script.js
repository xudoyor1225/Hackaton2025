// js/script.js

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded and parsed");

    // --- ОБЩИЕ МЕХАНИЗМЫ ИНТЕРАКТИВНОСТИ ---

    // 1. Переключение Сайдбара и Оверлей
    const sidebar = document.getElementById('sidebar');
    const menuToggleBtn = document.getElementById('menu-toggle');
    const mainWrapper = document.querySelector('.main-content-wrapper');
    let sidebarOverlay = null; // Создадим оверлей динамически

    if (menuToggleBtn && sidebar && mainWrapper) {
        console.log("Sidebar toggle elements found");

        // Функция для создания оверлея (для мобильных)
        function createOverlay() {
            if (sidebarOverlay) return; // Уже создан
            sidebarOverlay = document.createElement('div');
            sidebarOverlay.classList.add('sidebar-overlay');
            document.body.appendChild(sidebarOverlay);
            sidebarOverlay.addEventListener('click', toggleSidebar); // Закрытие по клику на оверлей
            console.log("Sidebar overlay created");
        }

        // Функция для управления сайдбаром
        function toggleSidebar() {
            const isMobile = window.innerWidth <= 992;
            console.log(`Toggling sidebar. Is mobile: ${isMobile}`);

            if (isMobile) {
                // На мобильных открываем/закрываем выдвижением слева
                sidebar.classList.toggle('open');
                if (!sidebarOverlay) createOverlay(); // Создать оверлей если его нет
                // Показать/скрыть оверлей
                 sidebarOverlay.classList.toggle('active', sidebar.classList.contains('open'));
                 // Блокировка скролла фона
                 document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';

            } else {
                // На десктопе сворачиваем/разворачиваем
                sidebar.classList.toggle('collapsed');
                mainWrapper.style.marginLeft = sidebar.classList.contains('collapsed') ? '80px' : '280px'; // Явное управление margin
            }

            // Перерисовка графиков после анимации сайдбара
            if (window.Chart && typeof Chart.instances === 'object') {
                setTimeout(() => {
                     Object.values(Chart.instances).forEach(chart => {
                         if (chart && chart.ctx && chart.ctx.canvas.offsetParent !== null) { // Проверяем видимость графика
                             chart.resize();
                             console.log("Resized chart:", chart.id);
                         }
                     });
                }, 350); // Время анимации сайдбара
            }
        }

        menuToggleBtn.addEventListener('click', toggleSidebar);

        // Начальная проверка состояния сайдбара при загрузке
        if (window.innerWidth <= 992) {
             // На мобильных сайдбар по умолчанию скрыт, margin у контента 0
             mainWrapper.style.marginLeft = '0';
             sidebar.classList.remove('collapsed'); // Убираем collapsed если он был
        } else {
             // На десктопе проверяем, был ли он свернут (например, через localStorage)
             const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
             if (isCollapsed) {
                 sidebar.classList.add('collapsed');
                 mainWrapper.style.marginLeft = '80px';
             } else {
                 sidebar.classList.remove('collapsed');
                 mainWrapper.style.marginLeft = '280px';
             }
        }

         // Сохранение состояния сайдбара (только для десктопа)
         const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                if (mutation.attributeName === 'class' && window.innerWidth > 992) {
                    const isNowCollapsed = sidebar.classList.contains('collapsed');
                    localStorage.setItem('sidebarCollapsed', isNowCollapsed);
                    console.log("Sidebar state saved:", isNowCollapsed);
                }
            });
         });
         observer.observe(sidebar, { attributes: true });


         // Обновление при ресайзе окна
         window.addEventListener('resize', () => {
             const isMobile = window.innerWidth <= 992;
             if (isMobile) {
                 // Если перешли на мобильный вид и сайдбар был открыт (не collapsed), закрываем его
                 if (!sidebar.classList.contains('collapsed') && !sidebar.classList.contains('open')) {
                    // sidebar.classList.add('open'); // Или оставляем закрытым? Лучше закрытым
                 }
                 mainWrapper.style.marginLeft = '0'; // Всегда 0 на мобильных
                 sidebar.classList.remove('collapsed'); // Убрать десктопное сворачивание
                 // Скрыть оверлей если он активен и сайдбар закрыт
                 if (sidebarOverlay && sidebarOverlay.classList.contains('active') && !sidebar.classList.contains('open')) {
                    sidebarOverlay.classList.remove('active');
                    document.body.style.overflow = '';
                 }
             } else {
                 // Если перешли на десктоп
                 const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true'; // Восстанавливаем состояние
                 sidebar.classList.toggle('collapsed', isCollapsed);
                 mainWrapper.style.marginLeft = isCollapsed ? '80px' : '280px';
                 sidebar.classList.remove('open'); // Убрать мобильное открытие
                 if (sidebarOverlay) sidebarOverlay.classList.remove('active'); // Скрыть оверлей
                 document.body.style.overflow = ''; // Разблокировать скролл
             }
         });

    } else {
        console.error("Sidebar toggle elements not found!");
    }

    // 2. Анимация счетчиков в карточках статистики
    const counters = document.querySelectorAll('.stat-card-value[data-target]');
    const animateCounter = (counter) => {
        const target = +counter.getAttribute('data-target');
        const duration = 1500; // ms
        const stepTime = Math.max(1, Math.floor(duration / target)); // Минимальное время шага 1мс
        let current = 0;
        counter.innerText = '0'; // Начинаем с 0
        counter.classList.add('counting');

        const timer = setInterval(() => {
            const increment = Math.max(1, Math.ceil(target / (duration / stepTime))); // Увеличиваем шаг если цель большая
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
                counter.classList.remove('counting');
            }
             // Форматирование числа с разделителями (пробелами)
            counter.innerText = current.toLocaleString('ru-RU');
        }, stepTime);
    };

    // Используем Intersection Observer для запуска анимации при появлении карточки
    const observerOptions = {
        root: null, // viewport
        threshold: 0.1 // Запустить когда 10% элемента видно
    };

    const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                animateCounter(counter);
                observer.unobserve(counter); // Запустить анимацию один раз
                console.log("Animating counter:", counter.getAttribute('data-target'));
            }
        });
    }, observerOptions);

    counters.forEach(counter => {
        counterObserver.observe(counter);
    });

    // 3. Система Уведомлений (Toast)
    const notificationsContainer = document.getElementById('notifications-container');

    // Глобальная функция для показа уведомлений
    window.showToast = function(message, title = 'Уведомление', type = 'info', duration = 5000) {
         console.log(`Showing toast: ${type} - ${title}`);
         if (!notificationsContainer) {
             console.error("Notifications container not found!");
             return;
         }

         const toast = document.createElement('div');
         toast.classList.add('toast-notification', type);
         toast.style.animationDuration = `${duration}ms`; // Для прогресс-бара

         const icons = {
             success: 'fa-solid fa-check-circle',
             error: 'fa-solid fa-times-circle',
             info: 'fa-solid fa-info-circle',
             warning: 'fa-solid fa-exclamation-triangle'
         };

         toast.innerHTML = `
             <i class="toast-icon ${icons[type]}"></i>
             <div class="toast-content">
                 <h4>${title}</h4>
                 <p>${message}</p>
             </div>
             <button class="toast-close" aria-label="Закрыть уведомление">×</button>
         `;

         // Вставляем новое уведомление сверху
         notificationsContainer.prepend(toast);

         // Анимация появления (управляется CSS @keyframes slideInRight)

         // Автоматическое скрытие
         const hideTimeout = setTimeout(() => {
             toast.classList.add('fade-out');
             // Удаляем после анимации исчезновения
             toast.addEventListener('animationend', (e) => {
                 // Убедимся что это анимация fadeOutRight
                 if (e.animationName === 'fadeOutRight') {
                     toast.remove();
                     console.log("Toast removed automatically");
                 }
             });
         }, duration);

         // Закрытие по кнопке
         toast.querySelector('.toast-close').addEventListener('click', () => {
             clearTimeout(hideTimeout); // Отменяем автоскрытие
             toast.classList.add('fade-out');
             toast.addEventListener('animationend', (e) => {
                  if (e.animationName === 'fadeOutRight') {
                     toast.remove();
                     console.log("Toast removed by user");
                 }
             });
         });
     }

    // Кнопка для теста уведомлений (если есть на странице)
    const showToastBtn = document.getElementById('show-toast-btn');
     if(showToastBtn) {
         showToastBtn.addEventListener('click', () => {
             const types = ['success', 'error', 'info', 'warning'];
             const titles = {
                 success: 'Успех!',
                 error: 'Ошибка!',
                 info: 'Информация',
                 warning: 'Внимание!'
             };
             const messages = [
                 'Операция успешно завершена.',
                 'Не удалось выполнить запрос. Попробуйте еще раз.',
                 'Система будет перезагружена через 5 минут.',
                 'Обнаружена подозрительная активность.'
             ];
             const randomType = types[Math.floor(Math.random() * types.length)];
             showToast(messages[Math.floor(Math.random() * messages.length)], titles[randomType], randomType);
         });
     }

    // Показать приветственное уведомление (только на дашборде?)
    if (document.body.classList.contains('dashboard-page')) { // Добавим класс к body на странице дашборда
        setTimeout(() => {
            showToast('Добро пожаловать в обновленный дашборд "Прозрачный Шанс"!', 'Привет, Айдос!', 'success', 7000);
        }, 1500); // Чуть позже после загрузки
    }

    // 4. Активация текущего пункта меню в сайдбаре
    const currentPath = window.location.pathname.split("/").pop(); // Получаем имя файла (e.g., dashboard.html)
    const sidebarLinks = document.querySelectorAll('.sidebar-menu .menu-link');

    sidebarLinks.forEach(link => {
        const linkPath = link.getAttribute('href').split("/").pop();
        link.classList.remove('active'); // Сначала убираем active со всех
        if (linkPath === currentPath || (currentPath === '' && linkPath === 'dashboard.html')) { // Условие для главной страницы
            link.classList.add('active');
            console.log("Active sidebar link set to:", currentPath || 'dashboard.html');
        }
    });

    // 5. Плавная прокрутка по якорям (если понадобится)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if(targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // 6. Инициализация тултипов (если будем использовать, например, Tippy.js)
    // Пример с data-tooltip атрибутом:
    // <button data-tooltip="Нажмите для сохранения">Сохранить</button>
    // if (typeof tippy === 'function') {
    //     tippy('[data-tooltip]', {
    //         content(reference) {
    //             return reference.getAttribute('data-tooltip');
    //         },
    //         animation: 'shift-away',
    //         theme: 'light-border', // Можно создать кастомную тему
    //     });
    // }


}
); // End DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    console.log("Dashboard page specific JS loaded");

    // ... (Код инициализации таблицы, пагинации, поиска, сортировки - без изменений) ...
    const tableBody = document.querySelector('#applications-table tbody');
    const placeholderRow = document.querySelector('#applications-table .table-placeholder');
    const paginationWrapper = document.getElementById('table-pagination');
    let currentPage = 1;
    const rowsPerPage = 5;
    let currentTableData = [];
    let currentSort = { column: 'date', direction: 'desc' };
    const statusClasses = { /* ... */ };
    const statusIcons = { /* ... */ };

    function renderTableRows(data) { /* ... (код без изменений) ... */ }
    function renderPagination(totalRows) { /* ... (код без изменений) ... */ }
    function sortData(data, column, direction) { /* ... (код без изменений) ... */ }
    function updateSortHeaders() { /* ... (код без изменений) ... */ }
    function findApplicant(id) { /* ... */ }
    function findScholarship(id) { /* ... */ }

    function initTable() {
        console.log("Initializing table...");
        if (placeholderRow) placeholderRow.style.display = 'table-row'; // Показать плейсхолдер сначала
        // Имитация загрузки данных таблицы
        setTimeout(() => {
             if(placeholderRow) placeholderRow.style.display = 'none'; // Скрыть после "загрузки"
             currentTableData = sortData(demoApplications, currentSort.column, currentSort.direction);
             renderTableRows(currentTableData);
             renderPagination(currentTableData.length);
             console.log("Table initialized with", currentTableData.length, "rows");
             updateSortHeaders();
         }, 800); // Небольшая задержка для имитации
    }
    initTable(); // Вызов инициализации таблицы

    const searchInput = document.getElementById('table-search-input');
    if (searchInput) { /* ... (код поиска без изменений) ... */ }
    const tableHeaders = document.querySelectorAll('#applications-table th[data-sort]');
    tableHeaders.forEach(header => { /* ... (код сортировки без изменений) ... */ });

    // --- ИНИЦИАЛИЗАЦИЯ И ОБНОВЛЕНИЕ ФУТУРИСТИЧНОГО ЧАРТА ---
    async function initializeFuturisticChart(chartId, dataProvider) { // dataProvider - функция или объект
        const chartContainer = document.getElementById('chart-container');
        const loader = document.getElementById(`${chartId}-loader`);
        const summaryContainer = document.getElementById('chart-summary');
        const summaryItems = { // Объект для доступа к элементам сводки
             total: document.getElementById('summary-total'),
             approved: document.getElementById('summary-approved'),
             pending: document.getElementById('summary-pending'),
             rejected: document.getElementById('summary-rejected'),
             // Добавь другие если есть
        };

        if (!chartContainer || !loader || !summaryContainer) {
            console.error("Futuristic Chart Wrapper elements not found for", chartId);
             if (loader) displayChartError(chartId, 'Ошибка структуры HTML для графика');
            return;
        }

        // Скрыть сводку перед загрузкой
        summaryContainer.style.opacity = '0';
        Object.values(summaryItems).forEach(el => { if (el) el.textContent = '--'; }); // Сброс значений

        try {
             // Получаем данные (если dataProvider - функция, вызываем её)
            const chartData = typeof dataProvider === 'function' ? await dataProvider() : dataProvider;

            if (!chartData || !chartData.labels || !chartData.data) {
                 throw new Error("Получены неверные данные для графика.");
            }

             // Вызываем асинхронную функцию инициализации и ЖДЕМ ее завершения
            const chartInstance = await initApplicationsStatusChart(chartId, chartData); // Используем новую функцию

            // Если график успешно создан (не null)
            if (chartInstance) {
                 console.log(`[Script] Chart ${chartId} successfully initialized, updating summary.`);
                // Обновляем блок сводки
                const total = chartData.data.reduce((sum, value) => sum + (isNaN(value) ? 0 : value), 0);
                const approvedIndex = chartData.labels.findIndex(l => l.includes('Одобрена'));
                const pendingIndex = chartData.labels.findIndex(l => l.includes('рассмотрении'));
                const rejectedIndex = chartData.labels.findIndex(l => l.includes('Отклонена'));
                // Добавь другие индексы

                if(summaryItems.total) summaryItems.total.textContent = total.toLocaleString('ru-RU');
                if(summaryItems.approved) summaryItems.approved.textContent = (approvedIndex > -1 ? chartData.data[approvedIndex].toLocaleString('ru-RU') : '0');
                if(summaryItems.pending) summaryItems.pending.textContent = (pendingIndex > -1 ? chartData.data[pendingIndex].toLocaleString('ru-RU') : '0');
                if(summaryItems.rejected) summaryItems.rejected.textContent = (rejectedIndex > -1 ? chartData.data[rejectedIndex].toLocaleString('ru-RU') : '0');
                // Обнови другие

                 // Плавно показываем блок сводки
                 summaryContainer.style.transition = 'opacity 0.5s ease-in-out 0.2s'; // Задержка появления
                 summaryContainer.style.opacity = '1';

            } else {
                 console.warn(`[Script] Chart instance for ${chartId} was null. Summary not updated.`);
                 // Ошибка уже должна быть показана лоадером/displayChartError
            }

        } catch (error) {
            // Ошибка будет показана через displayChartError из chart-config.js
            console.error("[Script] Error during chart initialization process:", error);
            summaryContainer.style.opacity = '0'; // Убедимся, что сводка скрыта
        }
    }

    // Вызов функции инициализации для графика на дашборде
    if (document.getElementById('applicationsChart')) {
         // Передаем объект данных напрямую
        initializeFuturisticChart('applicationsChart', analyticsData.applicationsByStatus);
    }

    // Обработчик кнопки обновления в карточке графика
    const chartRefreshBtn = document.querySelector('.futuristic-card .chart-actions button[title="Обновить"]');
    if (chartRefreshBtn) {
        chartRefreshBtn.addEventListener('click', async () => {
             showToast('Обновление аналитики...', 'Информация', 'info', 1500);
             chartRefreshBtn.disabled = true;
             chartRefreshBtn.querySelector('i').classList.add('fa-spin'); // Анимация иконки

             // --- ПРОВАЙДЕР ДАННЫХ (ИМИТАЦИЯ ЗАПРОСА) ---
             const getNewAnalyticsData = async () => {
                 await new Promise(resolve => setTimeout(resolve, 900)); // Имитация задержки сети
                 // Генерируем "новые" случайные данные для примера
                  const newStatusData = {
                      labels: analyticsData.applicationsByStatus.labels,
                      data: analyticsData.applicationsByStatus.data.map(val => Math.max(0, val + Math.floor(Math.random() * 20) - 10))
                  };
                  // Можно добавить проверку, если сервер вернул ошибку
                  // if (Math.random() < 0.1) throw new Error("Сервер не ответил");
                  return newStatusData;
             };
             // --- КОНЕЦ ПРОВАЙДЕРА ---

             try {
                // Перезапускаем инициализацию, передавая функцию-провайдер данных
                await initializeFuturisticChart('applicationsChart', getNewAnalyticsData);
             } finally {
                 chartRefreshBtn.disabled = false;
                 chartRefreshBtn.querySelector('i').classList.remove('fa-spin'); // Убираем анимацию
             }
        });
    }

    // --- ОСТАЛЬНОЙ КОД ДЛЯ ДАШБОРДА ---
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) { logoutBtn.addEventListener('click', (e) => { /* ... */ }); }

    // Показ точки уведомлений (пример)
    const notificationBadge = document.querySelector('.notification-badge');
     const clarificationIndex = analyticsData.applicationsByStatus.labels.findIndex(l => l.includes('уточнения'));
    if (notificationBadge && clarificationIndex > -1 && analyticsData.applicationsByStatus.data[clarificationIndex] > 0) {
         const count = analyticsData.applicationsByStatus.data[clarificationIndex];
         notificationBadge.style.display = 'flex'; // Используем flex для центрирования
         notificationBadge.textContent = count;
         // Стили для бейджа можно задать в CSS
    }

     // Анимация счетчиков в стат. карточках
     const statValues = document.querySelectorAll('.stat-card-value[data-target]');
     statValues.forEach(valueEl => {
         const target = +valueEl.getAttribute('data-target');
         const duration = 1500; // Длительность анимации
         const startTime = performance.now();

         function animateCount(currentTime) {
             const elapsedTime = currentTime - startTime;
             const progress = Math.min(1, elapsedTime / duration);
             const currentVal = Math.floor(progress * target);
             valueEl.textContent = currentVal.toLocaleString('ru-RU');

             if (progress < 1) {
                 requestAnimationFrame(animateCount);
             } else {
                 valueEl.textContent = target.toLocaleString('ru-RU'); // Установить точное значение в конце
             }
         }
         requestAnimationFrame(animateCount);
     });

}); // Конец DOMContentLoaded