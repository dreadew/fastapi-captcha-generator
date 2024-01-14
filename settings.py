from envparse import Env

env = Env()

DATABASE_URL = env.str(
	"DATABASE_URL",
	default="postgresql+asyncpg://postgres:1234@localhost:5432/notion"
)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)