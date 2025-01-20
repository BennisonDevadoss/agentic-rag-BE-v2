from config.models import User

USERS = [
    User(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        role_id=1,  # Admin role_id
        is_otp_verified=True,
    ),
    User(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        role_id=2,  # User role_id
        is_otp_verified=True,
    ),
]
