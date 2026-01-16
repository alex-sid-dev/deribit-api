from dataclasses import dataclass
from os import environ as env
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    user: str
    password: str
    host: str
    port: str
    db_name: str

    @property
    def uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass(frozen=True, slots=True)
class RedisConfig:
    host: str
    port: str

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


@dataclass(frozen=True, slots=True)
class Configs:
    db: PostgresConfig
    redis: RedisConfig

    @classmethod
    def load(cls, env_path: str = ".env") -> "Configs":
        load_dotenv(dotenv_path=env_path)
        return cls(
            db=PostgresConfig(
                user=env["POSTGRES_USER"],
                password=env["POSTGRES_PASSWORD"],
                host=env["POSTGRES_HOST"],
                port=env["POSTGRES_PORT"],
                db_name=env["POSTGRES_DB"],
            ),
            redis=RedisConfig(
                host=env.get("REDIS_HOST", "localhost"),
                port=env.get("REDIS_PORT", "6379"),
            ),
        )


def load_configs(env_path: str = ".env") -> Configs:
    return Configs.load(env_path)