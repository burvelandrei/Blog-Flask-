from dataclasses import dataclass
from environs import Env


@dataclass
class DB:
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    def __str__(self) -> str:
        return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


def load_config(path: str | None = None) -> DB:
    env: Env = Env()
    env.read_env(path)

    return DB(
        db_host=env("DB_host"),
        db_port=int(env("DB_port")),
        db_user=env("DB_user"),
        db_password=env("DB_password"),
        db_name=env("DB_name"),
    )


if __name__ == "__main__":
    config_db: DB = load_config()
    print(config_db)
