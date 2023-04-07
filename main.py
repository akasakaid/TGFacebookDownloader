import sys
from core.Polling import poling


if __name__ == "__main__":
    try:
        print('~' * 50)
        print('- BOT ACTIVE NOW !!')
        print('~' * 50)
        poling()
    except KeyboardInterrupt:
        sys.exit()
