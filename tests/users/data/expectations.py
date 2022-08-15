from core.models.base_models import Status


def expect_user(firstname: str, lastname: str, phone: str):
    return {
        "status": Status.SUCCESS,
        "message": "retrieval succesful",
        "payload": {
            "firstname": firstname,
            "lastname": lastname,
            "phone": phone
        }
    }
