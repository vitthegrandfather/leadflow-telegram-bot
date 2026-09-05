from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.models.enums import LeadStatus


def admin_home_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Recent leads", callback_data="a:p:0")],
            [InlineKeyboardButton(text="Export CSV", callback_data="a:x")],
        ]
    )


def lead_list_keyboard(
    leads: list, *, page: int, total: int, per_page: int = 5
) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=lead.public_id, callback_data=f"a:l:{lead.id}")]
        for lead in leads
    ]
    nav: list[InlineKeyboardButton] = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="Newer", callback_data=f"a:p:{page - 1}"))
    if (page + 1) * per_page < total:
        nav.append(InlineKeyboardButton(text="Older", callback_data=f"a:p:{page + 1}"))
    if nav:
        rows.append(nav)
    rows.append([InlineKeyboardButton(text="Export CSV", callback_data="a:x")])
    rows.append([InlineKeyboardButton(text="Admin home", callback_data="a:h")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def lead_actions_keyboard(lead_id: int) -> InlineKeyboardMarkup:
    status_row = [
        InlineKeyboardButton(text=status.label, callback_data=f"a:s:{lead_id}:{status.value}")
        for status in LeadStatus
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            status_row[:2],
            status_row[2:],
            [InlineKeyboardButton(text="Add note", callback_data=f"a:n:{lead_id}")],
            [InlineKeyboardButton(text="Back to list", callback_data="a:p:0")],
        ]
    )
