from threading import local

from paymentbot.config import Settings


class Shared(local):
    settings: Settings


shared = Shared()
