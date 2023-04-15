from fastapi import FastAPI, Request, Response, APIRouter

home_router = APIRouter()

@home_router.get('/')
async def home_page():
    return 'Wellcome to server'

