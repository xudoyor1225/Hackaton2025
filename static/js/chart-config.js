// js/chart-config.js

// --- ФУТУРИСТИЧНАЯ ЦВЕТОВАЯ ПАЛИТРА ---
const futuristicColors = {
    // Основные неоновые/яркие цвета
    cyan: 'rgba(0, 221, 255, 1)',
    magenta: 'rgba(255, 0, 255, 1)',
    lime: 'rgba(50, 255, 50, 1)',
    yellow: 'rgba(255, 255, 0, 1)',
    orange: 'rgba(255, 165, 0, 1)',
    purple: 'rgba(155, 89, 182, 1)',
    red: 'rgba(255, 0, 0, 1)', // Яркий красный для ошибок/отклонений

    // Цвета для текста и фона (темная тема)
    textPrimary: 'rgba(230, 230, 230, 1)', // Светлый текст
    textSecondary: 'rgba(160, 160, 160, 1)', // Менее яркий текст
    backgroundDark1: 'rgba(15, 18, 26, 1)',    // Очень темный фон (для тултипов)
    backgroundDark2: 'rgba(25, 28, 36, 1)',    // Темный фон (для карточки)
    borderLight: 'rgba(0, 221, 255, 0.2)',   // Голубая рамка (слабая)
    borderMedium: 'rgba(0, 221, 255, 0.4)', // Голубая рамка (средняя)

    // Цвета для статусов (пример с прозрачностью для фона)
    approvedBg: 'rgba(50, 255, 50, 0.7)',
    pendingBg: 'rgba(255, 165, 0, 0.7)',
    rejectedBg: 'rgba(255, 0, 0, 0.7)',
    submittedBg: 'rgba(0, 221, 255, 0.7)',
    clarificationBg: 'rgba(155, 89, 182, 0.7)',
    archivedBg: 'rgba(160, 160, 160, 0.7)',

    // Цвета для границ статусов (полная непрозрачность)
    approvedBorder: 'rgba(50, 255, 50, 1)',
    pendingBorder: 'rgba(255, 165, 0, 1)',
    rejectedBorder: 'rgba(255, 0, 0, 1)',
    submittedBorder: 'rgba(0, 221, 255, 1)',
    clarificationBorder: 'rgba(155, 89, 182, 1)',
    archivedBorder: 'rgba(160, 160, 160, 1)',
};

// --- ХЕЛПЕРЫ ---

/**
 * Создает линейный градиент для фона графика.
 * @param {CanvasRenderingContext2D} ctx - Контекст канваса.
 * @param {object} chartArea - Область графика Chart.js (chart.chartArea).
 * @param {string} colorStart - Начальный цвет градиента (rgba).
 * @param {string} colorEnd - Конечный цвет градиента (rgba).
 * @param {boolean} vertical - Направление градиента (true = вертикальный).
 * @returns {CanvasGradient|string} - Градиент или начальный цвет, если область не определена.
 */
function createGradient(ctx, chartArea, colorStart, colorEnd, vertical = true) {
    if (!chartArea) {
        return colorStart; // Возвращаем базовый цвет, если область еще не готова
    }
    const gradient = vertical
        ? ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top)
        : ctx.createLinearGradient(chartArea.left, 0, chartArea.right, 0);

    // Добавляем цвета: конечный (часто более прозрачный) в начале (0), начальный в конце (1)
    gradient.addColorStop(0, colorEnd);
    gradient.addColorStop(1, colorStart);
    return gradient;
}

/**
 * Уничтожает предыдущий инстанс графика.
 * @param {string} canvasId ID элемента canvas.
 */
function destroyChartInstance(canvasId) {
    if (window.chartInstances && window.chartInstances[canvasId]) {
        window.chartInstances[canvasId].destroy();
        delete window.chartInstances[canvasId];
        console.log(`[Chart] Destroyed previous instance: ${canvasId}`);
    }
}

/**
 * Управляет видимостью лоадера для графика.
 * @param {string} canvasId ID элемента canvas.
 * @param {boolean} show Показать или скрыть лоадер.
 * @param {string|null} message Сообщение (если null, используется стандартное).
 */
function handleChartLoader(canvasId, show = true, message = null) {
    const loaderElement = document.getElementById(`${canvasId}-loader`);
    if (!loaderElement) return;

    const spinner = loaderElement.querySelector('.spinner');
    const messageElement = loaderElement.querySelector('span');

    if (show) {
        loaderElement.style.opacity = '1';
        loaderElement.style.pointerEvents = 'auto';
        loaderElement.classList.remove('hidden');
        if (spinner) spinner.style.display = 'block';
        if (messageElement) messageElement.textContent = message || 'Загрузка данных...';
        console.log(`[Chart] Showing loader for ${canvasId}`);
    } else {
        // Плавное скрытие через CSS transition
        loaderElement.style.opacity = '0';
        loaderElement.style.pointerEvents = 'none';
        setTimeout(() => {
            // Добавляем класс hidden после завершения анимации, чтобы убрать из потока
            loaderElement.classList.add('hidden');
            console.log(`[Chart] Hiding loader for ${canvasId}`);
        }, 300); // Должно совпадать с длительностью transition в CSS
    }
}

/**
 * Показывает сообщение об ошибке на месте графика.
 * @param {string} canvasId ID элемента canvas.
 * @param {string} errorMsg Сообщение об ошибке.
 */
function displayChartError(canvasId, errorMsg = "Не удалось загрузить график") {
    handleChartLoader(canvasId, true); // Показываем лоадер/контейнер ошибки

    const loaderElement = document.getElementById(`${canvasId}-loader`);
    if (loaderElement) {
        const spinner = loaderElement.querySelector('.spinner');
        const messageElement = loaderElement.querySelector('span');
        if (spinner) spinner.style.display = 'none'; // Скрыть спиннер
        if (messageElement) messageElement.innerHTML = `<i class="fa-solid fa-triangle-exclamation fa-beat" style="margin-right: 8px; color: ${futuristicColors.red};"></i> ${errorMsg}`; // Иконка с анимацией
    }
    // Можно также скрыть сам canvas, если он мешает
    const canvasElement = document.getElementById(canvasId);
    if (canvasElement) canvasElement.style.display = 'none';

    console.error(`[Chart] Error for ${canvasId}: ${errorMsg}`);
}

// --- Глобальное хранилище инстансов ---
if (!window.chartInstances) {
    window.chartInstances = {};
}

// --- БАЗОВЫЕ ОПЦИИ ДЛЯ ВСЕХ ГРАФИКОВ (Футуристичные) ---
const futuristicDefaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
        duration: 1200,
        easing: 'easeInOutQuint', // Плавный, но выразительный easing
        delay: (context) => { // Небольшая задержка для элементов для "волнового" эффекта
            let delay = 0;
            if (context.type === 'data' || context.type === 'elements') {
                delay = context.dataIndex * 40 + context.datasetIndex * 80;
            }
            return delay;
        },
    },
    layout: {
        padding: { top: 15, bottom: 15, left: 10, right: 10 }
    },
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 25,
                font: { size: 13, family: "'Inter', sans-serif", weight: 500 },
                color: futuristicColors.textSecondary,
                usePointStyle: true,
                pointStyle: 'rectRounded', // Стиль маркеров
                boxWidth: 12,
                boxHeight: 8,
            },
             // Эффект при наведении на легенду (подсветка)
             onHover: (event, legendItem, legend) => {
                const ci = legend.chart;
                if (ci.getActiveElements().length || legend.legendHitBoxes.length === 0) return;

                const index = legendItem.datasetIndex ?? legendItem.index;
                ci.data.datasets.forEach((dataset, i) => {
                    ci.getDatasetMeta(i).data.forEach(element => {
                        element.options.backgroundColor = i === index
                             ? element.options.backgroundColor.replace(/[\d\.]+\)/, '1)') // Делаем непрозрачным
                             : element.options.backgroundColor.replace(/[\d\.]+\)/, '0.2)'); // Делаем полупрозрачным
                         element.options.borderColor = i === index
                             ? element.options.borderColor.replace(/[\d\.]+\)/, '1)')
                             : element.options.borderColor.replace(/[\d\.]+\)/, '0.3)');
                    });
                });
                ci.update();
             },
             onLeave: (event, legendItem, legend) => {
                const ci = legend.chart;
                 ci.data.datasets.forEach((dataset, i) => {
                     // Восстанавливаем исходные цвета (сложно без сохранения, используем базовые)
                     // Лучше хранить исходные цвета при инициализации или использовать reset
                     ci.getDatasetMeta(i).hidden = !ci.isDatasetVisible(i); // Просто восстанавливаем видимость
                 });
                ci.reset(); // Сброс к исходному состоянию
                ci.update();
            }
        },
        tooltip: {
            enabled: true,
            backgroundColor: futuristicColors.backgroundDark1, // Темный фон
            padding: 14,
            titleFont: { size: 15, weight: 'bold', family: "'Inter', sans-serif" },
            bodyFont: { size: 13, family: "'Inter', sans-serif" },
            titleColor: futuristicColors.cyan, // Заголовок в акцентном цвете
            bodyColor: futuristicColors.textPrimary,
            borderColor: futuristicColors.borderMedium, // Рамка в акцентном цвете
            borderWidth: 1,
            cornerRadius: 8,
            usePointStyle: true, // Использовать стиль точки данных
            boxPadding: 5, // Отступ внутри тултипа
            callbacks: { // Улучшенный callback для форматирования
                labelPointStyle: (context) => ({ pointStyle: 'rectRounded', rotation: 0 }),
                label: (context) => {
                    let label = context.dataset.label || context.label || '';
                    if (label) label += ': ';

                    let value = context.parsed;
                    // Обработка разных типов графиков
                    if (context.chart.config.type === 'bar' || context.chart.config.type === 'line') {
                        value = value?.y ?? value?.x; // Берем значение по оси Y или X
                    } else if (context.chart.config.type === 'doughnut' || context.chart.config.type === 'pie') {
                         value = context.parsed;
                    }

                    if (value !== null && value !== undefined && !isNaN(value)) {
                        label += value.toLocaleString('ru-RU'); // Форматирование числа

                        // Добавление процентов для Pie/Doughnut
                        if (context.chart.config.type === 'doughnut' || context.chart.config.type === 'pie') {
                            const total = context.dataset.data.reduce((a, b) => a + (isNaN(b) ? 0 : b), 0);
                            if (total > 0) {
                                const percentage = ((value / total) * 100).toFixed(1) + '%';
                                label += ` (${percentage})`;
                            }
                        }
                        // Добавление процентов для Bar (если ось X - проценты и горизонтальный)
                        if (context.chart.config.type === 'bar' && context.chart.options?.scales?.x?.max === 100 && context.chart.options?.indexAxis === 'y'){
                             label += '%';
                        }
                    } else {
                         label += 'N/A'; // Если значение некорректно
                    }
                    return ' ' + label; // Небольшой отступ
                },
                // Цветной квадрат перед лейблом
                 labelColor: function(context) {
                     const ds = context.dataset;
                     const idx = context.dataIndex;
                     return {
                         borderColor: Array.isArray(ds.borderColor) ? ds.borderColor[idx] : ds.borderColor || futuristicColors.borderMedium,
                         backgroundColor: Array.isArray(ds.backgroundColor) ? ds.backgroundColor[idx] : ds.backgroundColor || futuristicColors.cyan,
                         borderWidth: 1,
                         borderRadius: 2,
                     };
                 },
            }
        },
        // Можно добавить плагины, например, datalabels для показа значений на графике
        // import ChartDataLabels from 'chartjs-plugin-datalabels'; Chart.register(ChartDataLabels);
        // datalabels: { color: '#FFF', ... }
    },
    scales: { // Базовые настройки осей (для Line/Bar)
        x: {
            ticks: { color: futuristicColors.textSecondary, font: { family: "'Inter', sans-serif" } },
            grid: {
                color: futuristicColors.borderLight, // Слабая пунктирная сетка
                drawBorder: false,
                borderDash: [3, 4],
            }
        },
        y: {
             ticks: { color: futuristicColors.textSecondary, font: { family: "'Inter', sans-serif" } },
            grid: {
                color: futuristicColors.borderLight,
                drawBorder: false,
                 borderDash: [3, 4],
            }
        }
    },
     interaction: { // Улучшенное взаимодействие
        mode: 'index', // Тултип для всех элементов по оси X
        intersect: false, // Срабатывает даже если не точно на точке/баре
    },
     hover: { // Эффекты при наведении
        mode: 'nearest',
        intersect: true,
        animationDuration: 150 // Быстрая реакция на наведение
    },
};


// --- ФУНКЦИИ ИНИЦИАЛИЗАЦИИ ГРАФИКОВ ---

/**
 * Инициализация Doughnut графика статусов заявок (Футуристичный стиль)
 * @param {string} canvasId ID элемента canvas
 * @param {object} data Данные для графика ({ labels: string[], data: number[] })
 * @returns {Promise<Chart|null>} Promise, который разрешится с инстансом Chart.js или null при ошибке.
 */
async function initApplicationsStatusChart(canvasId, data) {
    const ctxElement = document.getElementById(canvasId);
    if (!ctxElement) {
        console.error(`[Chart] Canvas element "${canvasId}" not found.`);
        return null;
    }
    const ctx = ctxElement.getContext('2d');
    if (!data || !data.labels || !data.data || data.labels.length !== data.data.length) {
        displayChartError(canvasId, `Неверные или неполные данные для графика ${canvasId}`);
        return null;
    }

    console.log(`[Chart] Initializing Doughnut: ${canvasId}`);
    destroyChartInstance(canvasId); // Уничтожаем старый перед созданием нового
    handleChartLoader(canvasId, true); // Показываем лоадер

    // Определяем цвета динамически на основе лейблов
    const backgroundColors = data.labels.map(label => {
        if (label.includes('Одобрена')) return futuristicColors.approvedBg;
        if (label.includes('рассмотрении')) return futuristicColors.pendingBg;
        if (label.includes('Отклонена')) return futuristicColors.rejectedBg;
        if (label.includes('Подана')) return futuristicColors.submittedBg;
        if (label.includes('уточнения')) return futuristicColors.clarificationBg;
        if (label.includes('архиве')) return futuristicColors.archivedBg;
        return futuristicColors.textSecondary; // Цвет по умолчанию
    });
    const borderColors = data.labels.map(label => {
        if (label.includes('Одобрена')) return futuristicColors.approvedBorder;
        if (label.includes('рассмотрении')) return futuristicColors.pendingBorder;
        if (label.includes('Отклонена')) return futuristicColors.rejectedBorder;
        if (label.includes('Подана')) return futuristicColors.submittedBorder;
        if (label.includes('уточнения')) return futuristicColors.clarificationBorder;
        if (label.includes('архиве')) return futuristicColors.archivedBorder;
        return futuristicColors.textPrimary;
    });

    const chartConfig = {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Статусы заявок',
                data: data.data,
                backgroundColor: backgroundColors,
                borderColor: futuristicColors.backgroundDark2, // Граница под цвет фона для "вырезанности"
                borderWidth: 3,
                hoverOffset: 12, // Больше смещение при наведении
                hoverBorderColor: futuristicColors.textPrimary, // Белая граница при наведении
                hoverBorderWidth: 1,
                 hoverBackgroundColor: backgroundColors.map(color => color.replace('0.7)', '0.9)')) // Ярче при наведении
            }]
        },
        options: {
            ...futuristicDefaultOptions,
            cutout: '70%', // Большая "дырка" для футуристичности
            plugins: {
                ...futuristicDefaultOptions.plugins,
                legend: {
                    ...futuristicDefaultOptions.plugins.legend,
                     position: 'right', // Легенда справа удобнее для Doughnut
                     align: 'center',
                     labels: {
                        ...futuristicDefaultOptions.plugins.legend.labels,
                         boxWidth: 10,
                         padding: 20,
                     }
                 },
                 // Тултип уже настроен в базовых опциях
            }
        }
    };

    return new Promise((resolve, reject) => {
         // Используем requestAnimationFrame для отрисовки после того как DOM готов
         requestAnimationFrame(() => {
             try {
                 const chartInstance = new Chart(ctx, chartConfig);
                 window.chartInstances[canvasId] = chartInstance; // Сохраняем инстанс
                 handleChartLoader(canvasId, false); // Скрываем лоадер СРАЗУ после создания
                 console.log(`[Chart] Initialized Doughnut: ${canvasId}`);
                 resolve(chartInstance);
             } catch (error) {
                 displayChartError(canvasId, `Ошибка отрисовки Doughnut графика: ${error.message}`);
                 reject(error);
             }
         });
    });
}


/**
 * Инициализация Line графика динамики (Футуристичный стиль)
 * @param {string} canvasId ID элемента canvas
 * @param {object} data Данные ({ labels: string[], datasets: { label: string, data: number[], color?: string }[] })
 * @returns {Promise<Chart|null>} Promise с инстансом Chart.js или null.
 */
async function initApplicationsTrendChart(canvasId, data) {
    const ctxElement = document.getElementById(canvasId);
    if (!ctxElement) { console.error(`[Chart] Canvas element "${canvasId}" not found.`); return null; }
    const ctx = ctxElement.getContext('2d');
    if (!data || !data.labels || !data.datasets) { displayChartError(canvasId, `Неверные данные для Line графика ${canvasId}`); return null; }

    console.log(`[Chart] Initializing Line: ${canvasId}`);
    destroyChartInstance(canvasId);
    handleChartLoader(canvasId, true);

    const chartConfig = {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: data.datasets.map((dataset, index) => {
                 // Выбираем цвет из палитры или используем переданный
                const baseColor = dataset.color || [futuristicColors.cyan, futuristicColors.magenta, futuristicColors.lime, futuristicColors.yellow][index % 4];
                const colorStart = baseColor; // Цвет линии
                const colorEnd = baseColor.replace(/, 1\)/, ', 0.05)'); // Цвет для градиента (почти прозрачный)

                return {
                    label: dataset.label,
                    data: dataset.data,
                    borderColor: colorStart,
                    borderWidth: 3, // Линия потолще
                    tension: 0.4, // Сглаживание
                    pointRadius: 0, // Без точек по умолчанию
                    pointHoverRadius: 7, // Большие точки при наведении
                    pointBackgroundColor: colorStart,
                    pointBorderColor: futuristicColors.backgroundDark2, // Обводка под цвет фона
                    pointHoverBackgroundColor: colorStart,
                    pointHoverBorderColor: futuristicColors.textPrimary, // Белая обводка при наведении
                    pointHoverBorderWidth: 2,
                    fill: true, // Включаем заливку под линией
                    backgroundColor: (context) => { // Функция для градиента
                        const chart = context.chart;
                        const { ctx, chartArea } = chart;
                        return createGradient(ctx, chartArea, colorStart, colorEnd, true); // Вертикальный градиент
                    },
                };
            })
        },
        options: {
            ...futuristicDefaultOptions,
            scales: { // Настройки осей для Line
                y: {
                    beginAtZero: true,
                    ticks: { color: futuristicColors.textSecondary, font: { family: "'Inter', sans-serif" } },
                    grid: { color: futuristicColors.borderLight, drawBorder: false, borderDash: [3, 4] }
                },
                x: {
                    ticks: { color: futuristicColors.textSecondary, font: { family: "'Inter', sans-serif" } },
                    grid: { display: false } // Убрать вертикальную сетку
                }
            },
            plugins: {
                ...futuristicDefaultOptions.plugins,
                 legend: { // Легенда сверху, слева
                     position: 'top',
                     align: 'start',
                     labels: { ...futuristicDefaultOptions.plugins.legend.labels, usePointStyle: true }
                 },
                 // Тултип настроен в базе (mode: 'index')
            },
        }
    };

    return new Promise((resolve, reject) => {
         requestAnimationFrame(() => {
             try {
                 const chartInstance = new Chart(ctx, chartConfig);
                 window.chartInstances[canvasId] = chartInstance;
                 handleChartLoader(canvasId, false);
                 console.log(`[Chart] Initialized Line: ${canvasId}`);
                 resolve(chartInstance);
             } catch (error) {
                  displayChartError(canvasId, `Ошибка отрисовки Line графика: ${error.message}`);
                 reject(error);
             }
         });
     });
}

/**
 * Инициализация Bar графика успеваемости (Футуристичный стиль, горизонтальный)
 * @param {string} canvasId ID элемента canvas
 * @param {object} data Данные ({ labels: string[], data: number[] })
 * @returns {Promise<Chart|null>} Promise с инстансом Chart.js или null.
 */
async function initSuccessRateChart(canvasId, data) {
    const ctxElement = document.getElementById(canvasId);
    if (!ctxElement) { console.error(`[Chart] Canvas element "${canvasId}" not found.`); return null; }
    const ctx = ctxElement.getContext('2d');
    if (!data || !data.labels || !data.data) { displayChartError(canvasId, `Неверные данные для Bar графика ${canvasId}`); return null; }

    console.log(`[Chart] Initializing Bar: ${canvasId}`);
    destroyChartInstance(canvasId);
    handleChartLoader(canvasId, true);

    const chartConfig = {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: '% Одобрения', // Лейбл для тултипа
                data: data.data,
                // Градиент для каждого бара
                 backgroundColor: (context) => {
                    const chart = context.chart;
                    const {ctx, chartArea} = chart;
                    if (!chartArea) return null;

                    const colors = [futuristicColors.cyan, futuristicColors.magenta, futuristicColors.lime, futuristicColors.yellow, futuristicColors.orange, futuristicColors.purple];
                    const baseColor = colors[context.dataIndex % colors.length];
                    const colorStart = baseColor;
                    const colorEnd = baseColor.replace(/, 1\)/, ', 0.4)'); // Полупрозрачный конец

                    // Горизонтальный градиент для горизонтального бара
                    return createGradient(ctx, chartArea, colorStart, colorEnd, false);
                 },
                 borderColor: (context) => { // Цвет границы соответствует основному цвету
                    const colors = [futuristicColors.cyan, futuristicColors.magenta, futuristicColors.lime, futuristicColors.yellow, futuristicColors.orange, futuristicColors.purple];
                     return colors[context.dataIndex % colors.length];
                 },
                borderWidth: 1,
                borderRadius: { // Скругление "конца" бара
                    topLeft: 0, // Для горизонтального - topRight и bottomRight
                    bottomLeft: 0,
                    topRight: 6,
                    bottomRight: 6,
                },
                 borderSkipped: false, // Рисовать границу со всех сторон
                barPercentage: 0.7, // Бары чуть тоньше
                categoryPercentage: 0.8, // Расстояние между категориями
            }]
        },
        options: {
            ...futuristicDefaultOptions,
            indexAxis: 'y', // Горизонтальные бары
            scales: {
                x: { // Ось значений (%)
                    min: 0, // Начинаем с 0
                    max: 100, // Заканчиваем на 100
                    ticks: { color: futuristicColors.textSecondary, font: { family: "'Inter', sans-serif" }, callback: value => value + '%' },
                    grid: { color: futuristicColors.borderLight, drawBorder: false, borderDash: [3, 4] }
                },
                y: { // Ось категорий
                    ticks: { color: futuristicColors.textPrimary, font: { family: "'Inter', sans-serif", weight: 500 } }, // Ярче текст категорий
                    grid: { display: false } // Убрать горизонтальную сетку
                }
            },
            plugins: {
                ...futuristicDefaultOptions.plugins,
                 legend: { display: false }, // Легенда не нужна для одного датасета
                  // Тултип настроен в базе
            }
        }
    };

     return new Promise((resolve, reject) => {
         requestAnimationFrame(() => {
             try {
                 const chartInstance = new Chart(ctx, chartConfig);
                 window.chartInstances[canvasId] = chartInstance;
                 handleChartLoader(canvasId, false);
                 console.log(`[Chart] Initialized Bar: ${canvasId}`);
                 resolve(chartInstance);
             } catch (error) {
                  displayChartError(canvasId, `Ошибка отрисовки Bar графика: ${error.message}`);
                 reject(error);
             }
         });
     });
}

// Можно добавить другие функции инициализации (например, initUserRolesChart для Pie) по аналогии...