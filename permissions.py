"""Central permission registry for sub-admins.

Single source of truth for labels, callback routes and UI menu permissions.
Adding a new admin callback should only require adding its route here.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class PermissionSpec:
    key: str
    label: str
    callbacks: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()

REGISTRY = (
    PermissionSpec("stats", "📊 آمار", ("admin_stats",)),
    PermissionSpec("requests", "📥 صف درخواست‌ها", ("admin_request_queue", "admin_order_queue", "dismissorder_", "dismisscustomorder_", "clearorders", "clearorders_confirm", "clearorders_do")),
    PermissionSpec("receipts", "🧾 تایید رسیدها", ("admin_pending_receipts", "approve_", "reject_", "approvepay|", "rejectpay|", "approvecustom_", "rejectcustom_", "clearreceipts", "clearreceipts_confirm", "clearreceipts_do")),
    PermissionSpec("users", "👥 کاربران و سرویس‌ها", ("admin_userlist", "userpage_", "useropen_", "accounting_", "admin_search", "useractions_", "pm_", "toggleblock_", "svcs_", "svcdetail_", "svcdelete_", "svcrestore_", "svcpurge", "svcpurge_", "svcpurgeconfirm_", "svcedit_", "svcedit_link_", "svcedit_qr_", "admin_userlist_active", "admin_userlist_all")),
    PermissionSpec("broadcast", "📢 پیام همگانی", ("admin_broadcast",)),
    PermissionSpec("discounts", "🎟 مدیریت تخفیف", ("admin_discount", "discdetail_", "discdelete", "discdelete_", "discdeleteconfirm_", "discedit_", "discedit_value_", "discedit_uses_", "discedit_minorder_", "discedit_maxuser_", "discedit_expiry_", "discedit_users_", "discedit_plans_", "discplan", "discplan_", "discplaned_", "new_discount", "disctype_")),
    PermissionSpec("agency", "🤝 نمایندگی", ("admin_agency", "new_agent", "deleteagent_", "agentopen_", "editagentpercent_")),
    PermissionSpec("plans", "🗂 مدیریت پلن‌های VIP", ("admin_vip_categories", "newvip", "newvipcat", "vipcat", "admincat_", "vipcatdesc_", "delvip", "delvipcat_", "vipplan", "vipplan_", "newvipplan_", "delvipplan_", "movevip", "movevipcat_", "movevipplan_")),
    PermissionSpec("vpn_panel", "🛡️ پنل‌های VPN و نگاشت", (
        "admin_vpn_panels", "vpntype|", "vpndetail|", "vpntest|", "vpnedit", "vpntoggle|", "vpndelete", "vpnmap", "vpnadd",
        "panelchoose|", "panelsend|", "panelcatalog|", "panelmap|", "sendvip_", "sendcustomorder_",
        "panelcustom_", "panelcustompanel|", "panelcustompick|", "panelrevoke_", "panelrenew_", "panelrenewpick|", "paneldisable_", "panelenable_",
    )),
    PermissionSpec("referrals", "🤝 مدیریت دعوت‌ها", ("admin_referrals", "refpage_", "refdetail_")),
    PermissionSpec("guides", "📚 مدیریت راهنما", ("admin_guides", "guide", "guidenew", "guideadminopen_", "guidemove_", "guideeditname_", "guideeditcontent_", "guidedelete_", "guidedeleteconfirm_")),
    PermissionSpec("stickers", "🎬 استیکرهای منو", ("admin_stickers", "sticker", "stickeropen_", "stickerset_", "stickeroff_", "stickeron_", "stickerreset_")),
    PermissionSpec("botinfo", "ℹ️ اطلاعات ربات", ("admin_botinfo", "botinfo", "botinfo_open", "botinfo_channels", "botinfo_channel_add", "botinfo_edit_", "botinfo_channel_del_", "channel")),
    PermissionSpec("backup", "💾 بکاپ", ("admin_backup",)),
    PermissionSpec("orders_toggle", "🔴/🟢 روشن و خاموش کردن سفارشات", ("admin_orders_off", "admin_orders_on")),
    PermissionSpec("settings", "⚙️ تست و بساز سرویس خودت", ("admin_free_test_settings", "free_test", "admin_custom_build_settings")),
    PermissionSpec("logs", "🦖 لاگ خطاها و Audit", ("errlog", "errlogrefresh", "errlogclear", "errlogclearconfirm", "errlogsentryguide", "errlogdetail_", "admin_audit_logs")),
    PermissionSpec("health", "🩺 سلامت ربات", ("admin_health", "admin_cache_status", "cache_clear")),
    PermissionSpec("texts", "📝 ویرایش متن و دکمه‌ها", ("admin_text_editor", "ui_cat:", "ui_screen:", "ui_edit_text:", "ui_button:", "ui_layout:", "ui_move:", "textedit_", "textbtn_", "textlayout_", "ui_mode:", "ui_toggle:", "ui_auto", "ui_edit_auto:", "ui_buttons_page:", "ui_button_page:", "ui_screen_textpage:", "ui_cbtn_")),
)

PERMISSION_LABELS = {x.key: x.label for x in REGISTRY}

def permission_for_callback(data: str | None) -> str | None:
    d = data or ""
    if d in {"admin_back", "noop"}:
        return None
    for spec in REGISTRY:
        for prefix in spec.callbacks:
            if d == prefix or d.startswith(prefix):
                return spec.key
    return None

def permission_for_message(text: str | None) -> str | None:
    text = text or ""
    aliases = {
        "📊 آمار":"stats", "📥 صف درخواست‌ها":"requests", "👥 لیست کاربران":"users", "🔍 جستجوی حرفه‌ای":"users",
        "📢 پیام همگانی":"broadcast", "🎟 مدیریت تخفیف":"discounts", "🤝 نمایندگی (تخفیف VIP)":"agency",
        "🗂 دسته‌بندی‌های VIP":"plans", "🖥 مدیریت پنل‌های VPN":"vpn_panel", "🤝 مدیریت دعوت‌ها":"referrals",
        "📚 مدیریت راهنما":"guides", "🦖 لاگ خطاها (Sentry)":"logs", "🦖 لاگ خطاها و Audit":"logs", "🦖 لاگ خطاها":"logs", "ℹ️ اطلاعات ربات":"botinfo",
        "🎬 استیکرهای منو":"stickers", "💾 بکاپ":"backup", "🎁 تنظیم تست رایگان":"settings", "🧩 تنظیم بساز سرویس خودت":"settings",
        "📝 ویرایش متن و دکمه‌ها":"texts", "🔴 خاموش کردن سفارشات":"orders_toggle", "🟢 روشن کردن سفارشات":"orders_toggle",
        "🩺 سلامت ربات":"health", "🚀 وضعیت کش":"health", "👮 مدیریت ادمین‌ها":"manage_admins", "🧾 رسیدهای در انتظار":"receipts",
    }
    return aliases.get(text)
