

# necesito calcular el 'cuadrado maximo' que cabe en la pantalla
# y cual seria el tamano relativo de la carta en base a ese cuadrado.
#
# el tamano de la pantalla viene de ft.Page.width y ft.Page.height
# el tamano de carta se actualiza en el metodo resize de la clase Solitaire

def max_square(width, height):
    """
    Calcula el tamano maximo de un cuadrado que cabe en la pantalla.
    @param width: ancho de la pantalla
    @param height: alto de la pantalla
    @return: tupla con el ancho y alto del cuadrado maximo.
    """
    ratio = "2:1"
    smallest_width = height * 2
    smallest_height = width / 2

    width = min(width, smallest_width)
    height = min(height, smallest_height)

    return (width, height)


def _card_size(table_width, table_height):
    """
    Calcula el tamano de la carta en base al cuadrado maximo.
    @param width: ancho de la pantalla
    @param height: alto de la pantalla
    @return: tupla con el ancho y alto de la carta.
    """
    ratio = "3:4"
    rows = 8
    cols = 7
    margin = 25

    # defensive programming
    if table_width < 1000 or table_height < 500:
        table_height = 500
        table_width = 1000

    card_width = (table_width / rows) - (margin * 2)
    card_height = card_width * \
        int(ratio.split(":")[1]) / int(ratio.split(":")[0])
    return (card_width, card_height)

# tests
print("max squares")
assert max_square(1000, 500)  ==  (1000,500) 
assert max_square(1600, 800)  ==  (1600,800) 
assert max_square(1600, 500)  ==  (1000,500) 
assert max_square(1000, 800)  ==  (1000,500) 


print("cards")
assert _card_size(1000, 500) == (75, 100)
assert _card_size(1600, 800) == (150, 200)
print(_card_size(1400, 800) , "== ",(150, 200))
assert _card_size(1600, 500) == (150, 200)
assert _card_size(1000, 800) == (75, 100)

print("casos putos")
assert _card_size(100, 200) == (75, 100)
assert _card_size(20000, -1) == (75, 100)

# print("casos putos")
# print(card_size(100, 200) == (75, 100))
# print(card_size(20000, -1), " == ", (75, 100))
