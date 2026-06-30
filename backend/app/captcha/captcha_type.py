from enum import Enum


class CaptchaType(str, Enum):

    NONE = "none"

    TURNSTILE = "turnstile"

    HCAPTCHA = "hcaptcha"

    RECAPTCHA = "recaptcha"

    IMAGE = "image"

    UNKNOWN = "unknown"