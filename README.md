# Local Image Descriptors

PEDRO NEL MENDOZA VANEGAS

Este repositorio se trata sobre la temática del capítulo 2 del libro guía del curso de Visión Artificial. Los ejemplos y el ejercicio que serán desarrollados están basados en el libro de Jan Erik Solem titulado ``Programming Computer Vision with Python_ Tools and algorithms for analyzing images``. Dicha temática se centra en la utilización del descriptor local de imagen de Harris, el cual es ampliamente usado en muchas aplicaciones de ingeniería y en la ciencia. 

# Contenido

1. ``
## Recomendación para cargar archivos/imágenes

Debido a que algunos de nosotros trabajamos en equipos bajo algun sabor unix (Linux,OSX,etc.) y otros en Windows, es recomendable que a la hora de definir un camino (*path*) hacia una imagen u otro archivo dentro de su programa utilicen ``os.path``. Un ejemplo sencillo es [el siguiente:][path_link]

 	 Ejecutando en Windows sale esto 
	  print os.path.abspath("/var/lib/blob_files/myfile.blob")
	  >>> C:\var\lib\blob_files\myfile.blob
  
	  En unix sale esto
	  /var/lib/blob_files/myfile.blob
  

[path_link]: https://stackoverflow.com/questions/13162372/using-absolute-unix-paths-in-windows-with-python
