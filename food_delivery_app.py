MENU = {"Pizza":950,
        "Pasta":420,
        "Burger":880,
        "Fries":760,
        "Tacos":310,
        "Sushi":280
       }

USE_KEYBOARD = True
USE_SWAPS = True

KEY_ROWS = ["zxcvbnm","asdfghjkl","qwertyuiop"]
KEY_POSITION = {key:(row,col)
                for row,keys in enumerate(KEY_ROWS)
                for col,key in enumerate(keys)
               }


def are_neighbours(x,y):
    if x == y not in KEY_POSITION or y not in KEY_POSITION:
        return False
    (r1,c1),(r2,c2) = KEY_POSITION[x], KEY_POSITION[y]
    return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1

