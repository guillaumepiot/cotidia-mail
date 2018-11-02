from django.urls import reverse


def admin_menu(context):
    return [
        {
            "icon": "envelope",
            "text": "Email",
            "description": "See email template and logs.",
            "nav_items": [
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
        }
    ]
