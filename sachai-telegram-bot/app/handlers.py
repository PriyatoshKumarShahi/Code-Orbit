from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from app.logger import get_logger
from app.backend_client import verify_text_with_backend
from app.formatter import format_verification_result

logger = get_logger(__name__)
MAX_TELEGRAM_MESSAGE_LENGTH = 4096

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.first_name}) started the bot.")
    
    welcome_text = (
        f"Namaste {user.first_name}! 🙏 I am <b>SachAI</b>, your personal misinformation safety assistant.\n\n"
        "I am here to protect you from fake news, scams, and dangerous rumors.\n\n"
        "💡 <b>How to use me:</b>\n"
        "Simply <b>paste</b> or <b>forward</b> any suspicious WhatsApp message, news claim, or link directly into this chat.\n\n"
        "I will instantly analyze it, check its history, and give you a Fake News Score along with the potential consequences if it spreads."
    )
    await update.message.reply_text(welcome_text, parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🤖 <b>SachAI Help</b>\n\n"
        "1. Found a suspicious message on WhatsApp or social media?\n"
        "2. Copy the text or forward it directly to me.\n"
        "3. Wait a few seconds while I check my database and AI models.\n"
        "4. I will reply with the verdict and explain why it is real or fake.\n\n"
        "Stay safe and verify before you share!"
    )
    await update.message.reply_text(help_text, parse_mode="HTML")

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages and forwards."""
    text = update.message.text
    user = update.effective_user
    
    logger.info(f"Received text message from User {user.id} (Length: {len(text)})")
    
    # Show typing action to the user
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # Call the FastAPI backend
    data = await verify_text_with_backend(text)
    
    if not data:
        error_msg = "Sorry, SachAI verification is temporarily unavailable. Please try again in a moment."
        await update.message.reply_text(error_msg)
        return
        
    # Format the JSON response into an HTML message
    reply_text = format_verification_result(data)
    if len(reply_text) > MAX_TELEGRAM_MESSAGE_LENGTH:
        reply_text = reply_text[: MAX_TELEGRAM_MESSAGE_LENGTH - 1]

    try:
        await update.message.reply_text(reply_text, parse_mode="HTML")
    except BadRequest as exc:
        logger.warning(f"HTML reply failed, falling back to plain text: {exc}")
        fallback_text = (
            "SachAI analyzed your message, but rich formatting failed.\n\n"
            + reply_text.replace("<b>", "").replace("</b>", "")
            .replace("<i>", "").replace("</i>", "")
        )
        if len(fallback_text) > MAX_TELEGRAM_MESSAGE_LENGTH:
            fallback_text = fallback_text[: MAX_TELEGRAM_MESSAGE_LENGTH - 1]
        await update.message.reply_text(fallback_text)

async def unsupported_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages that are not text (e.g., photos, videos, voice notes)."""
    # TODO: In the future, we can extract text from images using the backend's image extraction
    # or handle voice notes. For now, kindly ask for text.
    logger.info(f"Received unsupported message type from User {update.effective_user.id}")
    
    msg = (
        "I see you sent a photo, video, or voice note! 📸🎙️\n\n"
        "Currently, I can only analyze <b>Text</b> messages. Please copy the text from the image or forward a text message instead.\n\n"
        "(Support for image and voice analysis is coming soon!)"
    )
    await update.message.reply_text(msg, parse_mode="HTML")
