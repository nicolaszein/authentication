import urllib.parse as urlparse
from dataclasses import dataclass
from peewee import PostgresqlDatabase

from grades.settings import DATABASE_URL


@dataclass
class DatabaseConfig:
    name: str
    user: str
    password: str
    host: str
    port: int


def parse_database_url(url):
    url = urlparse.urlparse(url)

    path = url.path[1:]
    path = path.split('?', 2)[0]

    config = {
        'name': path,
        'user': url.username,
        'password': url.password,
        'host': url.hostname,
        'port': url.port,
    }

    return DatabaseConfig(**config)


config = parse_database_url(DATABASE_URL)

DATABASE = PostgresqlDatabase(
    config.name,
    user=config.user,
    password=config.password,
    host=config.host,
    port=config.port,
    autocommit=True,
    autorollback=True
)
