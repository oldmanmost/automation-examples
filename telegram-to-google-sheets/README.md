# 📊 Telegram → Google Sheets Automation

Скрипт, который автоматически сохраняет заявки из Telegram-бота в структурированную Google-таблицу. Идеальное решение для малого бизнеса, чтобы не терять лиды.

## 🎯 Возможности
- Пошаговый сбор данных (Имя → Телефон → Запрос) через FSM
- Мгновенная запись новой строки в Google Sheets с датой и временем
- Автоматическое создание заголовков таблицы при первом запуске
- Обработка ошибок (если таблица недоступна, бот не "упадёт")

## 🚀 Как настроить и запустить
1. Установите зависимости: `pip install aiogram gspread oauth2client`
2. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/), включите **Google Sheets API** и **Google Drive API**.
3. Создайте Service Account, скачайте JSON-ключ и переименуйте его в `credentials.json`.
4. Откройте `credentials.json`, скопируйте `client_email` и дайте этому email-адресу права **Редактора** на вашу Google-таблицу.
5. Замените `YOUR_TOKEN_HERE` в `main.py` на токен вашего бота.
6. Запустите: `python main.py`

## 🛠 Технологии
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green)
![Google Sheets API](https://img.shields.io/badge/Google-Sheets_API-red)

---
🛒 **Заказать настройку такой связки для вашего бизнеса:** [Мой профиль на Kwork](https://kwork.ru/user/noonelex)
