<h1 align="center">New York taxi duration prediction Project</h1>

<p align="center">
<b>Jose Franco Arroyave Cardona</b><br>
Ingenieria de Sistemas | Modelos y Simulacion de Sistemas I<br>
</p>

## Dataset
https://www.kaggle.com/competitions/nyc-taxi-trip-duration

## Fase-1

Para la primera fase del proyecto sustituto se construyeron dos notebooks, el primero está centrado en la limpieza de datos, el segundo se encarga del entrenamiento del modelo, se puede encontrar información adicional dentro de cada notebook.

### Entregables
*  [1. Cleaning.ipynb](https://colab.research.google.com/drive/1FO0axUCSU46ABWc1ovqmEV99VVX-47Nl)
*  [2. Training and testing.ipynb](https://colab.research.google.com/drive/1RTpJFyidsf1eorbYX0gkjl3ObW6Hc9mt?usp=sharing)

### Ejecución

Cada notebook está dispuesto para que pueda ser ejecutado sin necesidad de hacer configuraciones adicionales, el notebook se encarga de clonar este repositorio en el ambiente de ejecución con el fin de tener todos los recursos necesarios.

Se recomienda ejecutarlo desde Colab de Google o un ambiente Linux, esto debido a que se utilizan comandos de terminal Linux para el manejo de archivos.


## Fase-2

Para la segunda fase del proyecto sustituto se contruyeron un contener de Docker con todos los recursos necesario par a hacer entrenamiento de modelos y predicciones a paritir de la entreda de conjuntos de datos.

### Entregables

* **trian.py:** Cuenta con al logica para hacer limpieza de datos y entrenamiento de nuevos modelos predictivos. El parametro **--data_file** permite identificar el nombre del archivo donde se encuentran los datos que seran usando para entrenar el modelo, este debe estar almacenado en el directorio **data**.

    ```python train.py --data_file train.csv``` Ejemplo para ejecutar el script.

* **predict.py:** Cuenta con al logica para hacer predicciones utilizando un modelo previamente entrenado y un listado de datos en formato csv. El parametro **--data_file** permite identificar el nombre del archivo donde se encuentran los datos que seran usando para hacer las predicciones este debe estar almacenado en el directorio **data**. El paramentro **--model_file** permite definir el nombre del archivo donde esta almacenado el modelo a utilizar, este debe estar almacenado en el directorio **nodels**.

    ```python predict.py --data_file train.csv --model_file model.cbm``` Ejemplo para ejecutar el script.

* **tools.py:** Conjunto de utilidades para la limpieza de datos.

* **requirements.txt:** Librerias requeridas por python para la ejecución del proyecto.

* **data/:** Directorio donde se almacenar los datos para entrenamiento de modelos, realización de predicciones y sus resultados. 

* **models/:** Directorio donde se almacenan los modelos preentrenados para las predicciones.

### Ejecución

Para la ejecucion de proyecto se debe tener instalado docker, clonar o descargar el repositorio github y seguir las siguientes instrucciones:

1. Dentro del directorio fase-2 se encuentra el archivo dockerfile, desde una terminal windows o linux se debe ejecutar el siguiente comando sobre este directorio para crear el contenedor con todas las dependencias y los script.

```
    docker build -t my_model_container .
```

2. Luego de crear el contenedor, se puede comenzar a entenar los modelos, en la raiz del proyecto puede encontrar la carpeta **data** donde se encuentra los conjuntos de datos de entrenamiento y prueba, es necesario copiar los datos de entrenamiento a la carpeta **data** dentro de fase-2, luego se puede ejecutar el script de entrenamiento pasando como paramentro el nombre del archivos del conjunto de datos.

Windows power shell:
```
docker run --rm -v ${pwd}/models:/app/models -v ${pwd}/data:/app/data my_model_container python train.py --data_file train.csv
```
Linux:
```
docker run --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data my_model_container python train.py --data_file train.csv
```

3. Para las predicciones, se puede ulilizar el modelo prentrenado que se encuentra en la caprta **model** en la raiz del repositorio, debe ser copiado a la carpeta **models** dentro de **fase-2**, igualmente para los datos, deben ser copiados a la carpeta **data**, luego puede ser ejecutado el comando de predicción, ajustando los parametros a los nombre del modelo y los datos utilizados.

Windows power shell:
```
docker run --rm -v ${pwd}/models:/app/models -v ${pwd}/data:/app/data my_model_container python predict.py --data_file train.csv --model_file model.cbm
```
Linux:
```
docker run --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data my_model_container python predict.py --data_file train.csv --model_file model.cbm
```





<p align="center">
<span>Modelos-y-Simulaciones-I</span><br>
<span>Universidad de Antioquia</span><br>
<span>202402</span><br>
</p>
