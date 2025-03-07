from dataclasses import dataclass
from environs import Env


@dataclass
class Tgbot:
    token: str


@dataclass
class Config:
    tgbot: Tgbot


def load_config():
    env = Env()
    env.read_env()

    return Config(
        Tgbot(
            token=env('BOT_TOKEN')
        )
    )
