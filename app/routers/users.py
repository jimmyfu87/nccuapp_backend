from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["users"])
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me", tags=["users"])
def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
def read_user(username: str):
    return {"username": username}