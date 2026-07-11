from fastapi import APIRouter


router = APIRouter()


# ---- get user - AUTH
@router.get("/auth")
async def get_user():
    return {'user': 'authenticated'}