import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from app.core.config import settings

# Sample business data
businesses = {
    "business123": {"name": "Fashion Store", "products": ["T-shirt", "Jeans", "Cap"]},
    "tech456": {"name": "Tech Gadgets", "products": ["Smartphone", "Tablet", "Headphones"]}
}

# Temporary session data for user interactions
session_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = context.args

    # Check if there’s a business identifier
    if args:
        business_id = args[0]
        if business_id in businesses:
            session_data[chat_id] = business_id
            business_name = businesses[business_id]["name"]

            # Inline keyboard for first-time actions
            keyboard = [
                [InlineKeyboardButton("View Products", callback_data='view_products')],
                [InlineKeyboardButton("Place Order", callback_data='place_order')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send welcome message with inline buttons
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Welcome to {business_name}! Choose an option below to get started.",
                reply_markup=reply_markup
            )
        else:
            await context.bot.send_message(chat_id=chat_id, text="Invalid business link. Please try again.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Please start with a valid business link.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Retrieve user business context
    chat_id = query.message.chat_id
    business_id = session_data.get(chat_id)

    # Check which button was pressed
    if query.data == 'view_products':
        products = businesses[business_id]["products"]
        product_list = "\n".join(products)
        await context.bot.send_message(chat_id=chat_id, text=f"Available products:\n{product_list}")
    elif query.data == 'place_order':
        await context.bot.send_message(chat_id=chat_id, text="To place an order, please type the product name.")


# Register the bot handlers
async def run_bot():
    application = Application.builder().token(settings.telegram_token).build()

    # Add command and callback handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

if __name__ == '__main__':
    main()
