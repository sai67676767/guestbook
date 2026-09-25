// Базовый URL нашего API (nginx проксирует /api/ на бэкенд)
const API_URL = '/api/messages';

// Находим элементы на странице
const form = document.getElementById('message-form');
const nameInput = document.getElementById('name-input');
const textInput = document.getElementById('text-input');
const messagesList = document.getElementById('messages-list');
const submitBtn = form.querySelector('button[type="submit"]');


// --- Загрузка и отрисовка сообщений ---

async function loadMessages() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Ошибка загрузки');
        const messages = await response.json();
        renderMessages(messages);
    } catch (error) {
        messagesList.innerHTML = `<p class="error-state">Не удалось загрузить сообщения 😔</p>`;
        console.error(error);
    }
}


function renderMessages(messages) {
    // Если список пустой — показываем заглушку
    if (messages.length === 0) {
        messagesList.innerHTML = `<p class="empty-state">Пока никто не оставил сообщение. Будьте первым! ✨</p>`;
        return;
    }

    // Собираем HTML для всех карточек
    messagesList.innerHTML = messages.map(msg => `
        <div class="message-card" data-id="${msg.id}">
            <div class="message-header">
                <span class="message-name">${escapeHtml(msg.name)}</span>
                <span class="message-date">${formatDate(msg.created_at)}</span>
            </div>
            <div class="message-text">${escapeHtml(msg.text)}</div>
            <button class="delete-btn" onclick="deleteMessage(${msg.id})">Удалить</button>
        </div>
    `).join('');
}


// --- Отправка нового сообщения ---

form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Не перезагружаем страницу

    const name = nameInput.value.trim();
    const text = textInput.value.trim();

    if (!name || !text) return;

    // Блокируем кнопку, чтобы не отправить дважды
    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправка...';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, text })
        });

        if (!response.ok) throw new Error('Ошибка отправки');

        // Очищаем форму
        nameInput.value = '';
        textInput.value = '';

        // Перезагружаем список
        await loadMessages();
    } catch (error) {
        alert('Не удалось отправить сообщение. Попробуйте ещё раз.');
        console.error(error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Отправить';
    }
});


// --- Удаление сообщения ---

async function deleteMessage(id) {
    if (!confirm('Удалить это сообщение?')) return;

    try {
        const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Ошибка удаления');
        await loadMessages();
    } catch (error) {
        alert('Не удалось удалить сообщение.');
        console.error(error);
    }
}


// --- Вспомогательные функции ---

// Защита от XSS: экранируем HTML-символы в имени и тексте
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Форматирование даты: "25.09.2026, 22:34"
function formatDate(isoString) {
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${day}.${month}.${year}, ${hours}:${minutes}`;
}


// --- Запуск при загрузке страницы ---
loadMessages();

