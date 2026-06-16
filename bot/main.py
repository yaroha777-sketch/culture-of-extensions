import html
import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from generator import PromptGenerator

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# User session states
STATE_IDLE = "idle"
STATE_CLARIFY = "clarify"
STATE_RESULTS = "results"
STATE_EDIT = "edit"

RESULTS_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("✏️ Внести правки", callback_data="edit"),
        InlineKeyboardButton("🔄 Перегенерировать", callback_data="regen"),
    ],
    [InlineKeyboardButton("🆕 Новый запрос", callback_data="new")],
])

EDIT_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🆕 Новый запрос", callback_data="new")],
])

MAX_VARIANT_LEN = 3800


def esc(text: str) -> str:
    return html.escape(text)


def truncate(text: str, limit: int = MAX_VARIANT_LEN) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n<i>[...текст обрезан — скопируй через кнопку копирования]</i>"


def get_generator(context: ContextTypes.DEFAULT_TYPE) -> PromptGenerator:
    return context.application.bot_data["generator"]


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["state"] = STATE_IDLE
    await update.message.reply_html(
        "👋 <b>Привет!</b> Опиши своими словами, что хочешь получить от AI.\n\n"
        "Я сгенерирую <b>2 варианта</b> идеального промпта для Claude — "
        "структурированный (XML) и компактный.\n\n"
        "💡 <i>Пример: «напиши три поста для инстаграм про мой салон красоты»</i>\n\n"
        "Команды: /start — начать заново · /new — новый запрос"
    )


async def cmd_new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["state"] = STATE_IDLE
    await update.message.reply_text("📝 Опиши новый запрос:")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("state", STATE_IDLE)
    text = update.message.text.strip()

    if state == STATE_CLARIFY:
        if text.lower() not in ("пропустить", "skip", "-", "."):
            context.user_data["clarifications"] = text
        await do_generate(update, context)

    elif state == STATE_EDIT:
        await do_edit(update, context, text)

    else:
        await process_new_request(update, context, text)


async def process_new_request(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    generator = get_generator(context)
    context.user_data["original"] = text
    context.user_data["clarifications"] = ""

    thinking = await update.message.reply_text("⏳ Анализирую запрос...")

    try:
        questions = await generator.get_clarifying_questions(text)
    except Exception as e:
        logger.error(f"Clarify error: {e}", exc_info=True)
        questions = ""

    await thinking.delete()

    if questions:
        context.user_data["state"] = STATE_CLARIFY
        await update.message.reply_html(
            f"❓ {esc(questions)}\n\n"
            "<i>Ответь или напиши</i> <b>пропустить</b> <i>для генерации без уточнений</i>"
        )
    else:
        await do_generate(update, context)


async def do_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    generator = get_generator(context)
    original = context.user_data.get("original", "")
    clarifications = context.user_data.get("clarifications", "")

    thinking = await update.message.reply_text("🧠 Генерирую промпты...")

    try:
        v1, v2 = await generator.generate_two_variants(original, clarifications)
    except Exception as e:
        logger.error(f"Generate error: {e}", exc_info=True)
        err_msg = str(e)
        if "401" in err_msg or "auth" in err_msg.lower():
            hint = "❌ Ошибка API: неверный ANTHROPIC_API_KEY. Проверь переменную на Railway."
        elif "429" in err_msg:
            hint = "❌ Превышен лимит Anthropic API. Попробуй через минуту."
        elif "403" in err_msg:
            hint = "❌ Нет доступа к модели. Проверь, что у ключа есть кредиты на console.anthropic.com."
        else:
            hint = f"❌ Ошибка: {err_msg[:200]}"
        await thinking.edit_text(hint)
        context.user_data["state"] = STATE_IDLE
        return

    context.user_data["v1"] = v1
    context.user_data["v2"] = v2
    context.user_data["state"] = STATE_RESULTS

    await thinking.delete()
    await _send_variants(update.message, v1, v2)


async def do_edit(update: Update, context: ContextTypes.DEFAULT_TYPE, instruction: str):
    generator = get_generator(context)
    v1 = context.user_data.get("v1", "")
    v2 = context.user_data.get("v2", "")

    thinking = await update.message.reply_text("✏️ Применяю правки...")

    try:
        new_v1, new_v2 = await generator.apply_edits(v1, v2, instruction)
    except Exception as e:
        logger.error(f"Edit error: {e}")
        await thinking.edit_text("❌ Ошибка. Попробуй описать правку иначе.")
        context.user_data["state"] = STATE_RESULTS
        return

    context.user_data["v1"] = new_v1
    context.user_data["v2"] = new_v2
    context.user_data["state"] = STATE_RESULTS

    await thinking.delete()
    await _send_variants(update.message, new_v1, new_v2)


async def _send_variants(message, v1: str, v2: str):
    """Send variant 1 and variant 2 as separate messages for easy copying."""
    await message.reply_html(
        f"<b>📋 ВАРИАНТ 1</b> — Структурированный (XML):\n\n"
        f"<pre>{esc(truncate(v1))}</pre>"
    )
    await message.reply_html(
        f"<b>📋 ВАРИАНТ 2</b> — Компактный:\n\n"
        f"<pre>{esc(truncate(v2))}</pre>",
        reply_markup=RESULTS_KEYBOARD,
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "new":
        context.user_data.clear()
        context.user_data["state"] = STATE_IDLE
        await query.message.reply_text("📝 Опиши новый запрос:")

    elif action == "regen":
        generator = get_generator(context)
        original = context.user_data.get("original", "")
        clarifications = context.user_data.get("clarifications", "")

        msg = await query.message.reply_text("🔄 Перегенерирую...")

        try:
            v1, v2 = await generator.generate_two_variants(original, clarifications)
        except Exception as e:
            logger.error(f"Regen error: {e}")
            await msg.edit_text("❌ Ошибка. Попробуй ещё раз.")
            return

        context.user_data["v1"] = v1
        context.user_data["v2"] = v2
        context.user_data["state"] = STATE_RESULTS

        await msg.delete()
        await _send_variants(query.message, v1, v2)

    elif action == "edit":
        context.user_data["state"] = STATE_EDIT
        await query.message.reply_html(
            "✏️ <b>Что изменить?</b>\n\n"
            "<i>Примеры:\n"
            "· «сделай более формальным»\n"
            "· «добавь ограничение по длине 200 слов»\n"
            "· «убери XML теги»\n"
            "· «переведи на английский»\n"
            "· «добавь few-shot примеры»</i>",
            reply_markup=EDIT_KEYBOARD,
        )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не задан в .env")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY не задан в .env")

    app = Application.builder().token(token).build()
    app.bot_data["generator"] = PromptGenerator(api_key)

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("new", cmd_new))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
