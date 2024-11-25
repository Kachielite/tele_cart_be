import asyncio
from re import match

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from app.core.config import settings
from app.crud.business import business_by_identifier
from app.db.session import get_db
from app.telebot.actions import get_main_menu_keyboard
from app.telebot.cart import add_to_cart, view_cart, list_cart_items, clear_cart, remove_item
from app.telebot.product import view_products, view_products_in_category, show_product_details

# Temporary session data for user interactions
session_data = {}

# https://t.me/e_cart24_bot?start=ISHF81A


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = context.args

    print(update.effective_chat)
    print(update)
    # Use a session directly with `next`
    db = next(get_db())  # Using `next()` to fetch one instance from the generator

    # Check if there’s a business identifier
    if args:
        business_identifier = args[0]
        status, business = business_by_identifier(business_identifier, db)

        if status == 200:
            session_data[chat_id] = business_identifier
            business_name = business["name"]
            business_description = business["description"]
            business_image_url = business["image_url"]

            # Set up a more enticing welcome message
            welcome_message = (
                f"✨ Welcome to *{business_name}*! ✨\n\n"
                f"{business_description or 'Discover an exciting range of products and exclusive offers here.'}\n\n"
                "Tap an option below to explore our offerings and enjoy a delightful shopping experience!"
            )

            # Inline keyboard for first-time actions.py
            keyboard = [
                [InlineKeyboardButton("🛍 View Products", callback_data='view_products')],
                [InlineKeyboardButton("🛒 View Cart", callback_data='view_cart')],
                [InlineKeyboardButton("🚀 Track Order", callback_data='place_order')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send business image first if available, then the welcome message
            if business_image_url:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=business_image_url,
                    caption=welcome_message,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"  # Enables basic Markdown for bold/italic styling
                )
            else:
                # Send the message without an image if no image URL is available
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=welcome_message,
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
        else:
            await context.bot.send_message(chat_id=chat_id, text="Invalid business link. Please try again.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Please start with a valid business link.")

    # Close session after query
    db.close()


# Button handler for inline button interactions
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Retrieve user business context
    chat_id = query.message.chat_id
    business_identifier = session_data.get(chat_id)

    # Check which button was pressed
    if query.data == 'view_products' and business_identifier:
        await view_products(business_identifier, chat_id, context)
    elif match(r'^category_\d+$', query.data):
        await view_products_in_category(business_identifier, chat_id, update, context)
    elif match(r'^product_\d+$', query.data):
        product_id = int(query.data.split('_')[1])
        await show_product_details(business_identifier, chat_id, context, product_id)
    elif match(r'^cart_\d+$', query.data):
        cart_product_id = int(query.data.split('_')[1])
        await add_to_cart(business_identifier, cart_product_id, chat_id, update.effective_chat, context)
    elif query.data == "view_cart":
        await view_cart(chat_id, update.effective_chat, context)
    elif query.data == "delete_item":
        await list_cart_items(chat_id, update.effective_chat, context)
    elif match(r'^remove_\d+$', query.data):
        id = int(query.data.split('_')[1])
        await remove_item(chat_id, id, update.effective_chat, context)
    elif query.data == "clear_cart":
        await clear_cart(chat_id, update.effective_chat, context)
    elif query.data == 'close_menu':
        await get_main_menu_keyboard(chat_id, context)



# Error handler for better error management
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"An error occurred: {context.error}")

# Function to register handlers and run the bot
async def run_bot():
    application = Application.builder().token(settings.telegram_token).build()

    # Add command and callback handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))


    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

# Main function to start the event loop
def main():
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

if __name__ == '__main__':
    main()

