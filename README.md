# Solitario cartablanca en Flet

A partir del tutorial de solitario
<https://flet.dev/docs/tutorials/python-solitaire/>
para ir aprendiendo.

## Lecciones aprendidas

### No te saltes el tutorial

por saltarme en el paso 3 y agregar una carta de mas, el ejemplo petaba y perdi media hora o mas.

Y luego por saltarlo otra vez y no leer el texto, estuve intentando arreglar
un trozo que estaba roto a drede.

### La actualizacion es mas facil de lo que pensaba

el cambiar estados y mantener responsablidiades separadas es mas facil de lo que pensaba.
de todas maneras es tedioso.

### Hay mucho escrito sobre ms32 free cell

- faq sobre el juego <https://www.solitairelaboratory.com/fcfaq.html>

- the SO answer <https://boardgames.stackexchange.com/questions/15287/is-there-any-configuration-of-free-cell-that-cannot-be-solved>

- the original 32k, in python <https://rosettacode.org/wiki/Deal_cards_for_FreeCell>

### De todas las posibles combinaciones, hay repetidas

si tomamos las 52! combinaciones (8x10^67) de cartas, en 8 columnas repetibles,
hay 1.75x10^64 combinaciones. (segun GPT-3).

El comparador de juegos deberia tener esto en cuenta, y no comparar juegos repetidos.

## TODO y Desarrollo

- [x] Crear un tablero
- [ ] Separar logica de tablero, de la logica de juego/Klondike y FreeCell
- [ ] Mejorar las posiciones verticales. y tb la separacion de cartas
- [ ] Arreglar el 'restart stock' que no se reinicia.
- [ ] Crear un menu de opciones un poco decente.
- [ ] ter minar lo de las semillas aleatorias.

### Wish list

- [ ] Poder escoger la semilla
- [ ] Crear un solver para el juego
- [ ] Puntuacion y tiempo
- [ ] Guardar y cargar estadisticas
- [ ] Comparar partida del usuario con la mejor partida posible
- [ ] Identificar 'juegos imposibles' y 'juegos dificiles'
- [ ] graficos sobre las estadisticas
