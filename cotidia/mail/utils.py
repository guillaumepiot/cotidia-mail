import inspect
import importlib

from cotidia.mail import settings as mail_settings
from cotidia.mail.notice import Notice


def getNoticeClass(slug, apps=mail_settings.COTIMAIL_APPS):
    for app_module in apps:
        # Import module specify in the notification apps setting
        module = importlib.import_module(app_module)

        # Browse through all the classes that extend Notice and matches
        # the slug
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Notice) and obj.identifier == slug:
                return obj
    return None


def getNoticeNames(apps=mail_settings.COTIMAIL_APPS):
    NOTICE_NAMES = []

    for app_module in apps:
        # Import module specify in the notification apps setting
        module = importlib.import_module(app_module)

        # Browse through all the classes that extend Notice
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Notice):
                NOTICE_NAMES.append((obj.identifier, obj.name))

    NOTICE_NAMES = sorted(NOTICE_NAMES, key=lambda obj: obj[1])

    return NOTICE_NAMES


def getNoticeMap(apps=mail_settings.COTIMAIL_APPS):
    NOTICE_MAP = []

    for app_module in apps:
        # Import module specify in the notification apps setting
        module = importlib.import_module(app_module)

        # Browse through all the classes that extend Notice
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Notice):
                NOTICE_MAP.append(obj())

    NOTICE_MAP = sorted(NOTICE_MAP, key=lambda obj: obj.name)

    return NOTICE_MAP
