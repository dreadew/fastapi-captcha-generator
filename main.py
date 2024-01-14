import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.handlers import user_router, utils_router
from api.login_handler import login_router

app = FastAPI(title='notion-clone')

origins = ['http://localhost:3000']
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*']
)

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix='/users', tags=['users'])
main_api_router.include_router(utils_router, prefix='/utils', tags=['utils'])
main_api_router.include_router(login_router, prefix='/login', tags=['login'])
app.include_router(main_api_router)

if __name__ == '__main__':
	uvicorn.run(app, host='localhost', port=3030)