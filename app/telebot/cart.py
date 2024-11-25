from itertools import product

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.helpers import escape_markdown

from app.crud.cart import add_item_to_cart, get_user_item, empty_cart_items, remove_cart_item
from app.db.session import get_db
from app.telebot.actions import get_menu_with_back_button


async def add_to_cart(business_identifier, product_id, chat_id, user_info, context):
    db = next(get_db())  # Get a database session

    #Add to cart
    status, response = add_item_to_cart(db, business_identifier, product_id, user_info)

    if status == 201 or status == 402:
        await context.bot.send_message(
            chat_id=chat_id,
            text=response["message"],
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 View Cart", callback_data='view_cart')],
                [InlineKeyboardButton("✅ Checkout", callback_data='proceed_to_checkout')],
                [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='close_menu')]
            ])
        )

    elif status == 404:
        # No categories found
        await context.bot.send_message(
            chat_id=chat_id,
            text=response["message"],
            reply_markup=get_menu_with_back_button()
        )

    else:
        # Error case
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ An error occurred. Please try again later.",
            reply_markup=get_menu_with_back_button()
        )

    db.close()



async def view_cart(chat_id, user_info, context):
    db = next(get_db())  # Get a database session

    # Get cart items
    status, response = get_user_item(db, user_info.id)

    if status == 200:
        cart_items = response["cart"]

        # Check if the cart is empty
        if not cart_items:
            await context.bot.send_message(
                chat_id=chat_id,
                text="🛒 Your cart is empty. Add some products to your cart first!",
                reply_markup=get_menu_with_back_button()  # Replace with your main menu function
            )
        else:
            # Construct the cart display message
            cart_message = "🛒 *Your Cart Items:*\n\n"
            for item in cart_items:
                product_name = escape_markdown(item['product_name'], version=2)
                product_price = f"{item['product_price']:.2f}".replace(".", "\\.")
                cart_message += (
                    f"📦 *{product_name}*: \\${product_price}\n"
                )

            # Add instructions or actions for the user
            cart_message += "\n\nTap below to proceed to checkout or manage your cart\n"

            # Send the cart message with options
            keyboard = [
                [InlineKeyboardButton("✅ Checkout", callback_data="proceed_to_checkout")],
                [InlineKeyboardButton("❌ Remove an Item", callback_data="delete_item")],
                [InlineKeyboardButton("🗑 Clear Cart", callback_data="clear_cart")],
                [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='close_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=chat_id,
                text=cart_message,
                parse_mode="MarkdownV2",  # Use Markdown version 2
                reply_markup=reply_markup
            )

    elif status == 404:
        await context.bot.send_message(
            chat_id=chat_id,
            text=response["message"],
            reply_markup=get_menu_with_back_button()
        )

    else:
        # Error case
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ An error occurred. Please try again later.",
            reply_markup=get_menu_with_back_button()
        )

    db.close()





async def list_cart_items(chat_id, user_info, context):
    db = next(get_db())  # Get a database session

    # Get cart items
    status, response = get_user_item(db, user_info.id)

    if status == 200:
        cart_items = response["cart"]

        # Check if the cart is empty
        if not cart_items:
            await context.bot.send_message(
                chat_id=chat_id,
                text="🛒 Your cart is empty. Add some products to your cart first!",
                reply_markup=get_menu_with_back_button()  # Replace with your main menu function
            )
        else:
            # Construct the cart display message
            cart_message = "🛒 *Your Cart Items:*\n\n"
            product_buttons = [
                [InlineKeyboardButton(item['product_name'], callback_data=f'remove_{item['product_id']}')]
                for item in cart_items
            ]

            # Add instructions or actions for the user
            cart_message += "Tap an item to remove from cart.\n"

            # Send the cart message with options
            product_buttons.append([InlineKeyboardButton("🛒 View Cart", callback_data='view_cart')])
            product_buttons.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='close_menu')])

            await context.bot.send_message(
                chat_id=chat_id,
                text=cart_message,
                reply_markup=InlineKeyboardMarkup(product_buttons)
            )


    elif status == 404:
        # No categories found
        await context.bot.send_message(
            chat_id=chat_id,
            text=response["message"],
            reply_markup=get_menu_with_back_button()
        )

    else:
        # Error case
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ An error occurred. Please try again later.",
            reply_markup=get_menu_with_back_button()
        )

    db.close()


async def remove_item(chat_id, product_id, user_info, context):
    db = next(get_db())  # Get a database session

    status, response = remove_cart_item(db, product_id, user_info.id)

    if status == 200:
        # Add instructions or actions for the user
        message = "✅ Item deleted successfully\n"

        # Send the cart message with options
        keyboard = [
            [InlineKeyboardButton("🛒 View Cart", callback_data='view_cart')],
            [InlineKeyboardButton("✅ Checkout", callback_data='proceed_to_checkout')],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='close_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif status == 404:
        await context.bot.send_message(
            chat_id=chat_id,
            text=response["message"],
            reply_markup=get_menu_with_back_button()
        )

    else:
        # Error case
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ An error occurred. Please try again later.",
            reply_markup=get_menu_with_back_button()
        )

    db.close()



async def clear_cart(chat_id, user_info, context):
    db = next(get_db())  # Get a database session

    status, response = empty_cart_items(db, user_info.id)

    if status == 200:
        cart_items = response["message"]

        # Check if the cart is empty
        if not cart_items:
            await context.bot.send_message(
                chat_id=chat_id,
                text="🛒 Your cart is empty. Add some products to your cart first!",
                reply_markup=get_menu_with_back_button()  # Replace with your main menu function
            )
        else:
            # Send the cart message with options
            keyboard = [
                [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='close_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(
                chat_id=chat_id,
                text="✅ Cart items cleared successfully",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )


    elif status == 404:
        await context.bot.send_message(
            chat_id=chat_id,
            text=response["message"],
            reply_markup=get_menu_with_back_button()
        )

    else:
        # Error case
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ An error occurred. Please try again later.",
            reply_markup=get_menu_with_back_button()
        )

    db.close()

