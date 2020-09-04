def is_admin(claims: dict) -> bool:
    return claims["is_admin"]


def is_staff(claims: dict) -> bool:
    return claims["is_staff"]


def is_customer(claims: dict) -> bool:
    return claims["is_customer"]
