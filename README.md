<h1 align="center">New York taxi duration prediction Project</h1>

<p align="center">
<b>Jose Franco Arroyave Cardona</b><br>
Ingeniería de Sistemas | Modelos y Simulación de Sistemas I<br>
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

Para la segunda fase del proyecto sustituto se construyó un contener de Docker con todos los recursos necesario par a hacer entrenamiento de modelos y predicciones a partir de la entrada de conjuntos de datos.

### Entregables

* **trian.py:** Cuenta con la lógica para hacer limpieza de datos y entrenamiento de nuevos modelos predictivos. El parámetro **--data_file** permite identificar el nombre del archivo donde se encuentran los datos que serán usando para entrenar el modelo, este debe estar almacenado en el directorio **data**.

    ```python train.py --data_file train.csv``` Ejemplo para ejecutar el script.

* **predict.py:** Cuenta con la lógica para hacer predicciones utilizando un modelo previamente entrenado y un listado de datos en formato .csv. El parámetro **--data_file** permite identificar el nombre del archivo donde se encuentran los datos que serán usando para hacer las predicciones, este debe estar almacenado en el directorio **data**. El parámetro **--model_file** permite definir el nombre del archivo donde está almacenado el modelo a utilizar, este debe estar almacenado en el directorio **models**.

    ```python predict.py --data_file train.csv --model_file model.cbm``` Ejemplo para ejecutar el script.

* **tools.py:** Conjunto de utilidades para la limpieza de datos.

* **requirements.txt:** Librerías requeridas por Python para la ejecución del proyecto.

* **data/:** Directorio donde se almacenan los datos para entrenamiento de modelos, realización de predicciones y sus resultados. 

* **models/:** Directorio donde se almacenan los modelos preentrenados para las predicciones.

### Ejecución

Para la ejecución de proyecto se debe tener instalado Docker, clonar o descargar el repositorio GitHub y seguir las siguientes instrucciones:

1. Dentro del directorio fase-2 se encuentra el archivo Dockerfile, desde una terminal Windows o Linux se debe ejecutar el siguiente comando sobre este directorio para crear el contenedor con todas las dependencias y los scripts.

    ```
    docker build -t my_model_container .
    ```

2. Luego de crear el contenedor, se puede comenzar a entrenar los modelos, en la raíz del proyecto puede encontrar la carpeta **data** donde se encuentra los conjuntos de datos de entrenamiento y prueba, es necesario copiar los datos de entrenamiento a la carpeta **data** dentro de fase-2, luego se puede ejecutar el script de entrenamiento pasando como parámetro el nombre del archivo del conjunto de datos.

    Windows Power Shell:
    ```
    docker run --rm -v ${pwd}/models:/app/models -v ${pwd}/data:/app/data my_model_container python train.py --data_file train.csv
    ```
    Linux:
    ```
    docker run --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data my_model_container python train.py --data_file train.csv
    ```

3. Para las predicciones, se puede utilizar el modelo preentrenado que se encuentra en la carpeta **model** en la raíz del repositorio, debe ser copiado a la carpeta **models** dentro de **fase-2**, igualmente para los datos, deben ser copiados a la carpeta **data**, luego puede ser ejecutado el comando de predicción, ajustando los parámetros a los nombres del modelo y los datos utilizados.

    Windows Power Shell:
    ```
    docker run --rm -v ${pwd}/models:/app/models -v ${pwd}/data:/app/data my_model_container python predict.py --data_file train.csv --model_file model.cbm
    ```
    Linux:
    ```
    docker run --rm -v $(pwd)/models:/app/models -v $(pwd)/data:/app/data my_model_container python predict.py --data_file train.csv --model_file model.cbm
    ```

## Fase-3

Para la tercera fase del proyecto se utilizó FastAPI para implementar una API rest que permita entrenar modelos y hacer predicciones a través de endpoints, utilizando los resultados de las bases anteriores.

### Entregables

* **requirements.txt:** Librerías requeridas por Python para la ejecución del proyecto.

* **Dockerfile:** Conjunto de utilidades para la limpieza de datos.

* **app (Proyecto FastAPI):** Para la implementación de una API rest se utilizó el frame work FastAPI, el cual facilita la creación y despliegue de los endpoint. En la carpeta app/ se encuentra almacenada toda la lógica, el proyecto tiene un archivo principal app.py que se encarga de desplegar los servicios necesarios. En la carpeta services/ se encuentra la lógica correspondiente al entrenamiento del modelo y las predicciones. En la carpeta utils/ se encuentra las funcionalidades que pueden ser recicladas en diferentes partes de la aplicación. En la ruta models/ se encuentra los diferentes modelos que son entrenados por la aplicación y en data/ se almacenan los resultados de las predicciones. 


### Ejecución

Para la ejecución de proyecto se debe tener instalado Docker, se debe clonar o descargar el repositorio GitHub y seguir las siguientes instrucciones:

**Nota:** En el repositorio de GitHub, carpeta data/, podrá encontrar las fuentes de datos para realizar los proceso de entrenamiento y predicción, también un modelo preentrenado en la carpeta model/.

1. Dentro del directorio fase-3 se encuentra el archivo Dockerfile, desde una terminal Windows o Linux se debe ejecutar el siguiente comando sobre el directorio para crear el contenedor con todas las dependencias necesarias para el despliegue del proyecto.

    ```
    docker build -t my_model_container .
    ```

2. Luego de crear el contenedor, se puede desplegar utilizando el siguiente comando.

    Windows Power Shell:
    ```
    docker run --rm -v ${pwd}/app:/app/app -p 8000:8000 my_model_container uvicorn app.app:app --host 0.0.0.0 --port 8000
    ```
    Linux:
    ```
    docker run --rm -v $(pwd)/app:/app/app -p 8000:8000 my_model_container uvicorn app.app:app --host 0.0.0.0 --port 8000
    ```
    Con este comando se ejecuta el contenedor, se monta la carpeta **app** como un volumen y se conecta el puerto 8000 del contenedor con el del equipo anfitrión. La sentencia ```uvicorn app.app:app --host 0.0.0.0 --port 8000``` ejecuta el servidor de aplicación de FastAPI en el puerto 8000 del contenedor, de esta forma puede ser accedido desde el navegador web del equipo anfitrión a través de http://127.0.0.1:8000.

3. Para interactuar con los servicios, FastAPI cuenta con un complemento de documentación la cual puede ser accedido a través de la URL http://127.0.0.1:8000/docs, el proyecto cuenta con 4 endpoints.

    <img src=resources/images/fase3_01.png />

    En la parte superior derecha de cada endpoint se encuentra el botón "Try it out", al presionarlo se activará el endpoint para establecer los parámetros y comenzar a ejecutarlos.

    <img src=resources/images/fase3_02.png />

    

* **/train:** El primer endpoint se encarga de entrenar un nuevo modelo, se espera como parámetro un archivo en formato .csv con la data en el formato adecuado, al presionar el botón "Execute" se comenzara a realizar el entrenamiento.
    <img src=resources/images/fase3_05.png />

    El modelo resultante se almacena en la ruta app/models/ en formato .cbm, al terminar el entrenamiento, se establece como opción por defecto para realizar las predicciones.

    <img src=resources/images/fase3_06.png />

* **/predict:** Para el endpoint de predicciones, se espera como parámetro un archivo .csv con la data debidamente formateada.
    <img src=resources/images/fase3_09.png />
Al terminar de hacer las predicciones, se visualiza la opción para descargar los resultados en formato plano .csv, estos archivos también estarán disponibles en la carpeta app/data/ dentro del proyecto.
    <img src=resources/images/fase3_10.png />

* **/models:** Este endpoint devuelve un diccionario con los modelos disponibles en la ruta app/models/, por defecto el proyecto cuenta con un modelo preentrenado, "model.cbm", el cual se utiliza por defecto cada vez que el proyecto inicia su ejecución.
    <img src=resources/images/fase3_07.png />

* **/setModel:** Dado que proyecto permite tener múltiples modelos entrenados se dispone un endpoint para hacer el cambio entre ellos, como parámetro se espera el nombre del archivo del modelo que está almacenado en la ruta app/models/, estos nombres puede ser consultados con el endpoint /models.
<img src=resources/images/fase3_08.png />


<p align="center">
<span>Modelos-y-Simulaciones-I</span><br>
<span>Universidad de Antioquia</span><br>
<span>202402</span><br>
</p>