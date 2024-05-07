from app.instance import server
from config.config import config_dir
from app.models.jogo_model import *
from app.controllers.user_controller import *

print(config_dir)

from app.controllers.jogo_controller import *
from app.controllers.user_controller import *

if __name__ == '__main__':
    server.run()