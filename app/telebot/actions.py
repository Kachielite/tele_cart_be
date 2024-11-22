# Main menu keyboard without "Back to Main Menu"
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


async def get_main_menu_keyboard(chat_id, context):
    await context.bot.send_message(
        chat_id=chat_id,
        text="Welcome back to the main menu.\n\nTap an option below to explore our offerings and enjoy a delightful shopping experience!",
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍 View Products", callback_data='view_products')],
        [InlineKeyboardButton("🛒 View Cart", callback_data='view_cart')],
    ])
    )

# Keyboard with "Back to Main Menu" for subsequent menus
def get_menu_with_back_button():
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("🛍 View Products", callback_data='view_products')],
            [InlineKeyboardButton("🛒 View Cart", callback_data='view_cart')],
            [InlineKeyboardButton("🚀 Place Order", callback_data='place_order')],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='close_menu')]])

# Show "Main Menu" button after initial /start message
def get_menu_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Main Menu", callback_data='open_menu')]])