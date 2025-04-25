import pyotp


def generate_otp(secret_key: str, expiry_time: int = 300) -> str:
    """
    Generates an OTP for a specific user.
    """
    totp = pyotp.TOTP(secret_key, interval=expiry_time)
    return totp.now()


def validate_otp(secret_key: str, otp: str, expiry_time: int = 300) -> bool:
    """
    Validates the OTP for a specific user.
    """
    totp = pyotp.TOTP(secret_key, interval=expiry_time)
    return totp.verify(otp)
