"""Telegram guruhlarida kurs haqidagi savollarga avtomatik javob beruvchi bot."""
import logging
import os
from pathlib import Path

import anthropic
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("kurs-bot")

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
MODEL = os.environ.get("CLAUDE_MODEL", "claude-haiku-5-5")
ADMIN_CONTACT = os.environ.get("ADMIN_CONTACT", "administrator")
KNOWLEDGE = Path(__file__).with_name("courses.md").read_text(encoding="utf-8")

SYSTEM = f"""Sen o'quv markazining Telegram guruhidagi yordamchisan.
Talabalar kurslar haqida savol beradi. Faqat quyidagi MA'LUMOT asosida, o'zbek tilida
(talaba qaysi tilda yozsa shu tilda), qisqa va xushmuomala javob ber.
Ma'lumotda yo'q narsani o'ylab topma: "Bu haqida {ADMIN_CONTACT} aniq javob beradi" de.
Agar xabar kurs/o'qishga oid savol bo'lmasa (suhbat, salomlashish, boshqa mavzu),
faqat bitta so'z yoz: SKIP

MA'LUMOT:
{KNOWLEDGE}
"""

client = anthropic.AsyncAnthropic()


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    if not msg or not msg.text:
        return
    try:
        resp = await client.messages.create(
            model=MODEL,
            max_tokens=500,
            system=SYSTEM,
            messages=[{"role": "user", "content": msg.text}],
        )
    except Exception:
        log.exception("Claude xatosi")
        return
    text = resp.content[0].text.strip()
    if text.upper().startswith("SKIP"):
        return
    await msg.reply_text(text)


def main() -> None:
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    app.run_polling()


if __name__ == "__main__":
    main()
