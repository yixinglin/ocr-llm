import os
from dataclasses import dataclass
import yaml
@dataclass
class Server:
    host: str
    port: int

@dataclass
class Auth:
    private_key: str
    public_key: str

@dataclass
class OpenAiConfig:
    api_key: str

@dataclass
class Logging:
    path: str


@dataclass
class FileConfig:
    quote_path: str
    image_path: str

@dataclass
class MongoDBConfig:
    uri: str
    port: int

@dataclass
class VipServiceConfig:
    root: str
    domain: str


@dataclass
class HsmsVipConfig:
    uri: str
    port: int
    username: str
    password: str

@dataclass
class DatabasesConfig:
    hsms_vip: HsmsVipConfig

@dataclass
class Config:
    debug: bool
    env: str
    version: str
    title: str
    summary: str
    email: str
    author: str
    url: str
    server: Server
    auth: Auth
    openai: OpenAiConfig
    logging: Logging
    file: FileConfig
    mongodb: MongoDBConfig
    vip_service: VipServiceConfig
    databases: DatabasesConfig



def load_config(config_path: str) -> Config:
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)

    hsms_vip_config = HsmsVipConfig(
        **config_dict['databases']['hsms_vip']
    )

    databases_config = DatabasesConfig(
        hsms_vip=hsms_vip_config
    )

    c = Config(
        debug=config_dict['debug'],
        env=config_dict['env'],
        version=config_dict['version'],
        title=config_dict['title'],
        summary=config_dict['summary'],
        email=config_dict['email'],
        author=config_dict['author'],
        url=config_dict['url'],
        server=Server(**config_dict['server']),
        auth=Auth(**config_dict['auth']),
        openai=OpenAiConfig(**config_dict['openai']),
        logging=Logging(**config_dict['logging']),
        file=FileConfig(**config_dict['file']),
        mongodb=MongoDBConfig(**config_dict['mongodb']),
        vip_service=VipServiceConfig(**config_dict['vip_service']),
        databases=databases_config
    )

    os.makedirs(c.logging.path, exist_ok=True)
    os.makedirs(c.file.quote_path, exist_ok=True)
    os.makedirs(c.file.image_path, exist_ok=True)
    os.makedirs(c.vip_service.root, exist_ok=True)
    return c

from dotenv import load_dotenv
load_dotenv()
# 读取环境变量
conf_file_path = os.getenv('CONFIG_FILE')
config = load_config(conf_file_path)

