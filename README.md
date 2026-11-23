# Kurs Telegram boti

Guruhdagi talabalarning kurs haqidagi savollariga `courses.md` asosida Claude yordamida javob beradi.

## Ishga tushirish
1. @BotFather → `/newbot` → token oling. `/setprivacy` → **Disable** (bot guruhdagi barcha xabarlarni ko'rishi uchun).
2. Botni guruhga qo'shing.
3. `courses.md` ni to'ldiring.
4. ```
   pip install -r requirements.txt
   export TELEGRAM_BOT_TOKEN=... ANTHROPIC_API_KEY=... ADMIN_CONTACT=@admin
   python bot.py
   ```
