from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from app.crud.category import get_categories_with_products
from app.crud.product import read_product, get_products_in_category
from app.db.session import get_db
from app.telebot.actions import get_menu_with_back_button


# Option: View Products - Show categories
async def view_products(business_identifier, update: Update):
    db = next(get_db())  # Get a database session

    query = update.callback_query
    await query.answer()

    # Fetch categories with products
    status, categories = get_categories_with_products(business_identifier, db)

    if status == 200 and categories:
        category_buttons = [
            [InlineKeyboardButton(cat.name, callback_data=f'category_{cat.id}')]
            for cat in categories
        ]
        category_buttons.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='close_menu')])

        # Attempt to edit the message if it exists; otherwise, send a new message
        if query.message and query.message.text:
            # Edit the existing message
            await query.edit_message_text(
                text="✨ Ready to dive into our product collection? ✨\n\nChoose a category below and discover top picks tailored just for you!",
                reply_markup=InlineKeyboardMarkup(category_buttons)
            )
        else:
            # Fallback: send a new message if there's no message to edit
            await update.effective_chat.send_message(
                text="✨ Ready to dive into our product collection? ✨\n\nChoose a category below and discover top picks tailored just for you!",
                reply_markup=InlineKeyboardMarkup(category_buttons)
            )

    elif status == 404:
        # No categories found
        await query.edit_message_text(
            text="No categories with products found.",
            reply_markup=get_menu_with_back_button()
        )

    else:
        # Error case
        await query.edit_message_text(
            text="An error occurred. Please try again later.",
            reply_markup=get_menu_with_back_button()
        )

    print("callback_query", update.callback_query)

    db.close()



# Show products in a selected category
async def view_products_in_category(business_identifier: str, update: Update, context):
    query = update.callback_query
    await query.answer()

    # Extract category_id from the callback data
    callback_data = query.data  # e.g., "category_3"
    category_id = int(callback_data.split('_')[1])  # Extract the ID part

    db = next(get_db())
    status, products = get_products_in_category(business_identifier, category_id, db)
    db.close()

    if status == 200:
        product_buttons = [
            [InlineKeyboardButton(product["name"], callback_data=f'product_{product["id"]}')]
            for product in products
        ]

        product_buttons.append([InlineKeyboardButton("⬅️ Back to Categories", callback_data='view_products')])

        await query.edit_message_text(
            text="✨ Here are some fantastic products just for you! ✨\nSelect a product for more details:",
            reply_markup=InlineKeyboardMarkup(product_buttons)
        )
    else:
        await query.edit_message_text(
            text="No products found in this category. Please choose a different category.",
            reply_markup=get_menu_with_back_button()
        )



# Show details for a selected product
async def show_product_details(business_identifier: str, product_id, update: Update):
    query = update.callback_query
    await query.answer()

    db = next(get_db())
    status, product = read_product(db, product_id, business_identifier)
    db.close()

    if status == 200:
        # Prepare product details message
        product_details = f"✨ *{product['name']}* ✨\n\n{product['description']}\n\n" \
                          f"💲 *Price*: ${product['price']}\n" \
                          f"📦 *In Stock*: {'Yes' if product['in_stock'] else 'No'}"

        await query.message.reply_photo(
            photo=product['image_url'],
            caption=product_details,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back to Products", callback_data=f'category_{product['category_id']}')],
                [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='close_menu')]
            ])
        )
    elif status == 404:
        await query.edit_message_text(
            text="Hmm, we couldn’t find that product. Please select another one.",
            reply_markup=get_menu_with_back_button()
        )
    else:
        await query.edit_message_text(
            text="An error occurred. Please try again later.",
            reply_markup=get_menu_with_back_button()
        )


# Optional: Add a callback handler for 'view_categories' to trigger view_products again
# async def handle_back_to_categories(update: Update, context):
#     query = update.callback_query
#     await query.answer()
#     # You might need to pass the `business_identifier` here or retrieve it from context/session
#     await view_products(business_identifier, update)
