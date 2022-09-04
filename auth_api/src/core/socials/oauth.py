
from authlib.integrations.flask_client import OAuth

from core.socials.service_provider.google import Google
from core.socials.service_provider.mail import MailRu
from core.socials.service_provider.vk import VKontakte
from core.socials.service_provider.yandex import Yandex

SOCIALS = (VKontakte, Yandex, Google, MailRu)

oauth = OAuth()

for social in SOCIALS:
    params = social().get_params()
    _ = oauth.register(**params)
