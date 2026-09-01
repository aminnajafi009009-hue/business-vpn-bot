"""
handlers/referral.py
نمایش لینک دعوت اختصاصی، کد اختصاصی، و آمار دعوت دوستان
(تعداد دعوت، دعوت‌های موفق، مبلغ آزاد شده، مبلغ در انتظار).
"""

import ui_editor


from aiogram import Router, F, types

import database as db
import bot_info
from utils import show_menu_with_sticker
from keyboards import referral_menu

router = Router(name="referral")


@router.callback_query(F.data == "referral")
async def referral(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if user is None:
        await callback.answer(ui_editor.get_alert_text("msg_18ae2939df", "ابتدا دستور /start را بزنید."), show_alert=True)
        return

    stats = db.get_referral_stats(user["id"])
    referral_enabled = db.get_referral_enabled()
    referral_min_volume = db.get_referral_min_volume_gb()
    referral_reward = db.get_referral_reward_amount()
    invite_link = f"https://t.me/{bot_info.get('bot_username')}?start={stats['invite_code']}"

    text = (
        f"👥 دعوت دوستان و کسب درآمد 💸\n\n"
        f"دوستانتو دعوت کن و به‌ازای هر دعوت موفق، {referral_reward:,} تومان پاداش نقدی بگیر! 🎁\n\n"
        f"🔗 لینک اختصاصی شما:\n{invite_link}\n\n"
        f"🔑 کد اختصاصی: {stats['invite_code']}\n\n"
        f"👤 تعداد دعوت: {stats['invited_count']}\n"
        f"✅ دعوت‌های موفق: {stats['successful_invites']}\n"
        f"🔓 مبلغ آزاد شده: {stats['released_amount']:,} تومان\n"
        f"🔒 مبلغ در انتظار: {user['locked_wallet']:,} تومان\n\n"
        f"ℹ️ {"شرط خرید حداقل " + str(referral_min_volume) + " گیگ فعال است" if referral_enabled else "شرط حداقل حجم خرید خاموش است و هر خرید پولی واجد شرایط است"}. "
        f"پاداش {referral_reward:,} تومان به‌صورت خودکار به کیف پول شما آزاد می‌شود. "
        f"(تست رایگان پاداش را آزاد نمی‌کند)"
    )
    await show_menu_with_sticker(callback.bot, callback.message.chat.id, "referral", text, reply_markup=referral_menu())
    await callback.answer()
