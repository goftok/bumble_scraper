from db_bot.bumble_bot import BumbleBot
from db_bot.config import config


def main():
    bumble_bot = BumbleBot(config)
    bumble_bot.run()


if __name__ == "__main__":
    main()
