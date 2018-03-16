# Local Image Descriptors

Esta segunda tarea tiene que ver con la utilización de descriptores locales de imagenes, como Harris o SIFT. Estos descriptores son ampliamente utilizados para distintas aplicaciones como pegado de imágenes, reconocimiento de objetos, navegación de robots, etc. 

Deberán modificar este archivo ``README.md`` en dónde describan la documentación del código que están adjuntando. En particular deben cumplir con lo siguiente:

1. Un programa en dónde utilicen el código de ejemplo del capítulo 2 del detector de esquinas de Harris y modifiquen parámetros, cambien imágenes, número de detecciones, etc. Las imágenes o archivos binarios que utilicen deben subirlas al repositorio también en una carpeta llamada ``data``. Debe llevar el nombre ``ch02-harris-example.py``. 
2. Deben resolver el ejercicio 1 del final del capítulo. Debe llevar el nombre ``ch02-ex1.py``. 
3. Bonificación por cualquier ejercicio o programa adicional.

Ejemplo de la estructura del repositorio a subir

	tarea2-descriptores-locales-JuanPerez/
	.
	├── README.md
	├── ch02-harris-example.py
	├── ch02-ex1.py
	├── data
	│   ├── image.jpg
  
## Recomendación para cargar archivos/imágenes

Debido a que algunos de nosotros trabajamos en equipos bajo algun sabor unix (Linux,OSX,etc.) y otros en Windows, es recomendable que a la hora de definir un camino (*path*) hacia una imagen u otro archivo dentro de su programa utilicen ``os.path``. Un ejemplo sencillo es [el siguiente:][path_link]

 	 Ejecutando en Windows sale esto 
	  print os.path.abspath("/var/lib/blob_files/myfile.blob")
	  >>> C:\var\lib\blob_files\myfile.blob
  
	  En unix sale esto
	  /var/lib/blob_files/myfile.blob
  

[path_link]: https://stackoverflow.com/questions/13162372/using-absolute-unix-paths-in-windows-with-python
