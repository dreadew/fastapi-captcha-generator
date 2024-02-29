from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from api.schemas import ShowCaptcha

from utils.captcha import gen_captcha_img

utils_router = APIRouter()
@utils_router.get('/captcha')
async def generate_captcha(icons_count: int = 3, bg_height: int = 200, bg_width: int = 400) -> ShowCaptcha:
	if icons_count <= 0 or icons_count >= 5:
		raise HTTPException(status_code=404, detail="количество иконок должно быть > 0 && < 5 ")
	
	if bg_height < 100 or bg_height > 400 or bg_width < 100 or bg_width > 400:
		raise HTTPException(status_code=404, detail="высота/ширина изображения должна быть > 100 && <= 400 ")
	
	captcha_image, captcha_data, icons = await gen_captcha_img(icons_count, bg_height, bg_width)
	return JSONResponse(content={'img': captcha_image, 'data': captcha_data, 'icons': icons})