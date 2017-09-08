from django.core.urlresolvers import reverse


def admin_menu(context):
    return [
        {
            "text": "Notices",
            "url": reverse("mail-admin:list"),
            "icon": "envelope",
        },
        {
            "text": "Logs",
            "url": reverse("mail-admin:logs"),
            "icon": "file-text-o",
            "permissions": [
                "perms.mail.add_emaillog",
                "perms.auth.change_add_emaillog"
            ],
        }
    ]
