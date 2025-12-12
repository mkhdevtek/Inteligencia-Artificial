Para este proyecto se realizó fine-tunning utilizando el modelo `unsloth/Llama3.2-Instruct`, tomado como base para conocimiento de programación.

## Dataset
El dataset recolectado, fue un dataset sintético generado con ayuda de herramientas de inteligencia artificial como `ChatGpt` y `Claude`, generando el [`dataset.jsonl`](dataset.jsonl). Sin embargo, se realizó una limpieza a través de un script de python [`clean_dataset.py`](clean_dataset.py).

### Limpieza
Una vez generamos el dataset mas limpio utilizamos el script [`train_tutor.py`](train_tutor.py) para realizar el entrenamiento del modelo de unsloth con el dataset sintético obtenido.

## Entrenamiento
Este proceso fue el mas tardado durando hasta 17 horas de entrenamiento

![](attachments/Pasted%20image%2020251210134443.png)

![](attachments/Pasted%20image%2020251210223530.png)

### Conversión a .gguf
Una vez que el proceso de fine-tunning termina, procedemos a convertir el modelo generado a un archivo `.gguf` el cual va a leer Ollama para generar el modelo. Para ello se utilizó la herramienta [`llama.cpp`](https://github.com/ggml-org/llama.cpp) para realizar la conversión y generación del modelo final.

![](attachments/Pasted%20image%2020251210225734.png)

![](attachments/Pasted%20image%2020251210225803.png)

![](attachments/Pasted%20image%2020251210225824.png)

## Generación del modelo Ollama
Finalmente a través de la generación de un [`Modelfile`](Modelfile), en el cual indicamos el modelo que preentrenamos con la línea `FROM ./tutor_algoritmos.gguf` y generamos el modelo de Ollama con el comando `ollama create tutor_programacion_final -f Modelfile`.  

![](attachments/Pasted%20image%2020251210230658.png)

## Resultado
Finalmente, los resultados del modelo fueron moderadamente satisfactorios permitiendo responder las preguntas de programación que realizaría el alumno:

![](attachments/Pasted%20image%2020251212115720.png)