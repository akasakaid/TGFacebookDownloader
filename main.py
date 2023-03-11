import sys
from core.Polling import poling


if __name__ == "__main__":
    try:
        poling()
    except KeyboardInterrupt:
        sys.exit()
