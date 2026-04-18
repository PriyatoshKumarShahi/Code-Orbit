import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from app.config import Config
from app.logger import get_logger
from app.handlers import (
    start_command,
    help_command,
    text_message_handler,
    unsupported_message_handler
)

logger = get_logger(__name__)

def main() -> None:
    """Start the bot."""
    logger.info("Initializing SachAI Telegram Bot...")
    
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Register message handler for text (ignores commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
    
    # Register message handler for unsupported media (photos, videos, docs, audio)
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.AUDIO | filters.VOICE,
        unsupported_message_handler
    ))

    logger.info("Starting polling mode...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped manually by user.")
    except Exception as e:
        logger.exception("A critical error occurred.")
