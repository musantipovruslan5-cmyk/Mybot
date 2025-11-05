import os

# Локальная версия без переменных окружения
TOKEN = "8562829264:AAHsrKNbET63BzX9Df8U7zxEZpd8SMb6bG0"  # Токен бота
admin = 7489815425  # Chat ID администратора

chat_bota = 'https://t.me/MalotNFT'
instruction = 'Отсутствует'
nicknameadm = 'malotNFT'
procent = 6
chat_id_bot = admin
channel_id = admin
db = 'db.db'

replenish = (
    '⚠️ Пополнение баланса\n\n'
    '🥝 Qiwi \n\n'
    f'👉 Номер(Qiwi) - <b><code>{admin}</code></b>\n'
    '👉 Комментарий - <code>{code}</code>\n'
    '👉 До 15 000 рублей!'
)

com_percent = 10# === Переменные среды (Render Environment Variables) ===
TOKEN = os.environ.get("TOKEN")      # Токен бота
admin = int(os.environ.get("ADMIN")) # Chat ID администратора

# Остальные настройки бота
chat_bota = 'https://t.me/MalotNFT'
instruction = 'Отсутствует'
nicknameadm = 'malotNFT'
procent = 6
chat_id_bot = admin
channel_id = admin
db = 'db.db'

replenish = (
    '⚠️ Пополнение баланса\n\n'
    '🥝 Qiwi \n\n'
    f'👉 Номер(Qiwi) - <b><code>{admin}</code></b>\n'
    '👉 Комментарий - <code>{code}</code>\n'
    '👉 До 15 000 рублей!'
)

com_percent = 10
