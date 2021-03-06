# Local Image Descriptors

PEDRO NEL MENDOZA VANEGAS

Este repositorio se trata sobre la temática del capítulo 2 del libro guía del curso de Visión Artificial. Los ejemplos y el ejercicio que serán desarrollados están basados en el libro de Jan Erik Solem titulado ``Programming Computer Vision with Python_ Tools and algorithms for analyzing images``. Dicha temática se centra en la utilización del descriptor local de imagen de Harris, el cual es ampliamente usado en muchas aplicaciones de ingeniería y en la ciencia. 

# Contenido

1. ``ch02-ex1.py``: En este programa para resolver el ejercicio 1 del capítulo 2 del libro guía, lo que se lleva a cabo es la modificación de la función para hacer matching de puntos de esquinas de Harris, de modo que también se tome una máxima distancia de pixeles entre puntos (se hace referencia a la distancia máxima euclidiana o euclídea entre dos puntos) para que ellos sean considerados como correspondencias, en busca de que el matching sea más robusto. 

Fundamentalmente, se realizaron cambios en las funciones match y match_twosided: 

-En cuanto a la función match, se agregaron locs1 y locs2 como parámetros, además de desc1, desc2 y threshold que estaban en la función match original. Adicionalmente, se calculó la distancia máxima de pixeles entre puntos y se implementó un condicional if de modo que dicha distancia fuera menor o igual a un valor determinado (en este caso 100). De esta forma se garantiza que el número de comparaciones de los descriptores de las imágenes 1 y 2 sea menor, haciendo el matching más robusto.

-A la función match_twosided, se le agregaron locs1 y locs2 como parámetros, además de los que ya tenía originalmente. Entonces, en el cálculo de las correspondencias, se agregaron los parámetros locs1 y locs2, permitiendo lo dicho en el párrafo anterior y obteniendo un matching más robusto.

2. ``ch02-harris-example.py``: Se implementan 3 funciones en conjunto para la detección de esquinas de Harris, dichas funciones son: 1) compute_harris_response, la cual es usada para computar la función de respuesta del detector de esquinas de Harris para cada pixel en una imagen en escala de grises; 2) get_harris_points, función empleada para retornar esquinas de una imagen de respuesta de Harris, tomando una distancia llamada min_dist que es el mínimo número de pixeles que separan esquinas y límites de la imagen; 3) plot_harris_points, función utilizada para dibujar esquinas encontradas en la imagen. 

Se lee una imagen en escala de grises y se realizan 3 procesos:

-Proceso 1: Variación del parámetro sigma para tomar diferentes escalas de los filtros gaussianos usados (los parámetros min_dist=10, threshold=0.1 permanecen igual). Se puede evidenciar que en la medida que incrementa el valor de sigma (parámetro que define la escala de los filtros gaussianos usados en el proceso de detección de esquinas), se hace más díficil la detección de puntos interesantes, es decir de esquinas de la imagen a través del Detector de esquinas de Harris; esto se debe a que la desviación estándar aumenta el emborronamiento de la imagen, por lo que se puede ver que cada vez que aumenta sigma, los puntos detectados como esquinas se superponen unos con otros.

-Proceso 2: Variación del parámetro min_dist (los parámetros sigma=3, threshold=0.1 permanecen igual). Se nota que a medida que aumenta el valor de min_dist (que corresponde al número mínimo de pixeles que separa las esquinas y el límite de la imagen), el número de 
detecciones de puntos interesantes o de esquinas en la imagen disminuye; esto permite una mejor visualización de puntos detectados. Esto se logra también gracias a que el detector de esquinas de Harris elimina puntos cuya medida de esquina no es más grande que los valores de esquina de todos los puntos dentro de una cierta distancia (min_dist).

-Proceso 3: Variación del parámetro threshold (los parámetros sigma=3, min_dist=10 permanecen igual). Se observa que con el incremento del valor de threshold (que se refiere a un umbral para la selección de puntos de esquinas), se puede ver que el número de detecciones
de puntos de interés o esquinas en la imagen decrementa; esto se puede explicar por el hecho de que el threshold hace un mapa de esquina para la eliminación de las esquinas débiles. Este es un enfoque que a menudo da buenos resultados, unido con la restricción que impone el valor de min_dist.

3. ``ch02-harris-example2.py``: Se implementan un conjunto de funciones para conformar una única función que lleva a cabo el matching de puntos de esquinas de Harris. El resultado de la función consiste en las correspondencias luego de aplicar la correlación cruzada normalizada a los patches o porciones rectangulares de cada una de las dos imágenes alrededor de puntos de esquinas de Harris. Para lograr esto, se leen dos imágenes convertidas a escala de grises, se computa la función de respuesta de Harris para cada pixel en las dos imágenes, se obtienen los puntos de esquinas de Harris en ambas imágenes, se obtienen descriptores para cada imagen, se hacen las correspondencias y se dibujan las mismas.
