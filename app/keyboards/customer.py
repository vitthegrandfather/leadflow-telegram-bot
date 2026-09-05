from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.models.enums import ContactMethod, ServiceCategory


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Submit a request", callback_data="m:s")],
            [InlineKeyboardButton(text="My requests", callback_data="m:r")],
            [InlineKeyboardButton(text="About", callback_data="m:a")],
        ]
    )


def category_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=item.label, callback_data=f"c:cat:{item.value}")]
        for item in ServiceCategory
    ]
    rows.append([InlineKeyboardButton(text="Cancel", callback_data="c:x")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def contact_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=item.label, callback_data=f"c:cm:{item.value}")]
        for item in ContactMethod
    ]
    rows.append([InlineKeyboardButton(text="Cancel", callback_data="c:x")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Confirm", callback_data="c:ok")],
            [
                InlineKeyboardButton(text="Edit", callback_data="c:ed"),
                InlineKeyboardButton(text="Cancel", callback_data="c:x"),
            ],
        ]
    )


def edit_field_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Name", callback_data="c:e:name")],
            [InlineKeyboardButton(text="Phone", callback_data="c:e:phone")],
            [InlineKeyboardButton(text="Service", callback_data="c:e:cat")],
            [InlineKeyboardButton(text="Brief", callback_data="c:e:desc")],
            [InlineKeyboardButton(text="Contact", callback_data="c:e:cm")],
            [InlineKeyboardButton(text="Cancel", callback_data="c:x")],
        ]
    )


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Main menu", callback_data="m:h")]]
    )
