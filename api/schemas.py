import re
from pydantic import BaseModel

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")

class TunedModel(BaseModel):
	class Config:
		'''tells pydantic to convert even non dict obj to json'''

		orm_mode = True

class ShowCaptcha(TunedModel):
	image_b64: str
	icon_locations: list
	icons_b64: list[str]