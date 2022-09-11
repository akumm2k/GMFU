import sys
from src.make_and_move import make_and_move

if __name__ == '__main__':
    assert len(sys.argv) == 2, 'why so many?'

    url = sys.argv[-1]
    print(sys.argv)
    make_and_move(url)