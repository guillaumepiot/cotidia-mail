from django.apps import AppConfig


class MailConfig(AppConfig):
    name = "cotidia.mail"
    label = "mail"

    def ready(self):
        import cotidia.mail.signals
