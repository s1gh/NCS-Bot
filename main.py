import sys
from base.bot import NCSBot
from base.helper import Logger
from irc.client import ServerConnectionError

bot = NCSBot()

def main():
    logger = Logger('NCSBot')
    try:
        logger.info('Connecting to IRC Server ...')
    except ServerConnectionError as err:
        logger.error(err)
        sys.exit(1)
    except OSError:
        logger.critical('Could not connect to IRC server!')
        return
    try:
        bot.start()
    finally:
        bot.connection.disconnect()
        bot.reactor.loop.close()
        logger.info('Disconnected from server!')

if __name__ == '__main__':
    main()
