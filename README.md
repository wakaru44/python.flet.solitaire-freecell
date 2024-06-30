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

### Flet. container no es gesture dectector.

mientras que las cartas son 'gesture detectors', los contenedores no lo son.
y las cartas usan 'on_tap' y los containers 'on_click'. o algo asi.

## Tasks y Desarrollo

- [x] Crear un tablero
- [x] Separar logica de tablero, de la logica de juego/Klondike y FreeCell
- [x] Mejorar las posiciones verticales. y tb la separacion de cartas
- [x] Bug: las cartas no vuelven a fundaciones. el drop nofunciona. era un mal _is_near_enough.
- [x] Arreglar el 'restart stock' que no se reinicia. era que el container usa on_click no on_tap.
- [x] Refactor card sizes based on <https://en.wikipedia.org/w/index.php?title=Standard_52-card_deck&section=4>
- [x] UI: la proporcion de las cartas es rara, y la separacion demasiada.
- [x] Bug: doble click en carta no mueve el dragable stack.
- [x] Feat: Implantar 'New Game' y refactorizar componentes.
- [x] UI: el resize parece que se ha roto, quiza despues de 'new game'. era problema de que no se estaba eliminanndo.
- [x] Feat: crear nuevos juegos.
- [ ] Feat: Escribir un solitario free cell
- [ ] Crear un menu de opciones un poco decente.
- [ ] Bug: el envio automatico en klondike se salta algunas normas y coloca cartas fuera de orden.
- [ ] UI: the menu dosnt close when clicking.
- [ ] terminar lo de las semillas aleatorias.

### Wish list

- [ ] Poder escoger la semilla
- [ ] Crear un solver para el juego
- [ ] Puntuacion y tiempo
- [ ] Guardar y cargar estadisticas
- [ ] Comparar partida del usuario con la mejor partida posible
- [ ] Identificar 'juegos imposibles' y 'juegos dificiles'
- [ ] graficos sobre las estadisticas
