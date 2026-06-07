from classmods import ENVMod
from typing import Optional


class Config:
    def load_config(self) -> None:
        self.flask(**ENVMod.load_args(Config.flask))
        self.general(**ENVMod.load_args(Config.general))
        self.database(**ENVMod.load_args(Config.database))

    @ENVMod.register(section_name='FLASK')
    def flask(
        self,
        host: str = '127.0.0.1',
        port: int = 8000,
        debug: bool = True,
        secret: Optional[str] = None,
    ) -> None:
        self.flask_host = host
        self.flask_port = port
        self.flask_debug = debug
        self.flask_secret = secret

    @ENVMod.register(section_name='general')
    def general(
        self,
        anonymous_mode: bool = False,
    ) -> None:
        self.anonymous_mode = anonymous_mode

    @ENVMod.register(section_name='database')
    def database(
        self,
        connection_string: str = 'sqlite:///../.db/app.db',
    ) -> None:
        self.connection_string = connection_string


cnf = Config()
