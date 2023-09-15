# TrabajoFinalGrado
Commit 1
rootTesting: Archivo que crea un widget the Tkinter que permite seleccionar un archivo mxl y displayearlo (siempre que no sea excesivamente grande. Tamanio debe ser testeado y ajustado en funcion del maximo del dispositivo.)

testMultiplePages: Funcion de test para recibir un archivo y dividirlo en multiples paginas segun un numero seteado de paginas maxima (hardcodeado dentro de la funcion). Las paginas se almacenan en la carpeta testPages.

Commit 2
testMultiplePages: Contiene la funcion divide_musicxml_in_pages que divide un score que recibe en un path y un int para el numero de compases (measures) por pagina, y retorna un array de scores que representan cada pagina del score.

testScorehighlight: contiene la funcion color_numbered_measure que recibe un score, un int con el numero del compas(measure) a colorear y un color para que sea coloreado, y retorna el score con el compas ingresado coloreado en el color ingresado. 

testScoreToImage: Contiene un prototipo de la logica para convertir un archivo mxl en un png.