from django.urls import reverse


def admin_menu(context):
    return [
        {
            "text": "Notices",
            "url": reverse("mail-admin:list"),
            "icon": "envelope",
            "permissions": [
                "mail.add_emaillog",
                "mail.change_emaillog"
            ],
        },
        {
            "text": "Logs",
            "url": reverse("mail-admin:logs"),
            "icon": "file-alt",
            "permissions": [
                "mail.add_emaillog",
                "mail.change_emaillog"
            ],
        }
    ]
