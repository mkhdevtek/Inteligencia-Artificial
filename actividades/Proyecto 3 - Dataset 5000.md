---
tags:
  - actividad
  - inteligencia-artificial
  - unidad-4
---
Para este proyecto se utilizaron modelos de Ollama, específicamente `llama3.2` y `deepseek-r1:1.5b`. Y utilizando Anything LLM como chat intermediario para realizar las preguntas sobre el tema.

En un proyecto de Anything LLM se carga el archivo csv del dataset de 5000 tweets sintéticos como **RAG** y se realizo la siguiente pregunta:
![[Pasted image 20251207174122.png]]

La respuesta no fue 100% precisa, sin embargo, entendió el contexto proporcionado y como realizar una lectura.

Después de verificar que el modelo entienda el contexto del documento embebido se realizó la pregunta principal *¿Está la Generación Z viviendo una crisis de sentido debido a la hiperconectividad, el exceso de información y la falta de proyectos compartidos?*

![[Pasted image 20251207174304.png]]

Esta respuesta nos indica que el modelo realizó un razonamiento lógico en base al texto proporcionado.

![[Pasted image 20251208153134.png]]


![[Pasted image 20251208153513.png]]


![[Pasted image 20251208154312.png]]


![[Pasted image 20251208154647.png]]

![[penultima.jpg]]

![[ultima.jpg]]

![[Pasted image 20251208160536.png]]![[Pasted image 20251208160538.png]]![[Pasted image 20251208160538.png]]![[Pasted image 20251208160538.png]]![[Pasted image 20251208160538.png]]![[Pasted image 20251208160538.png]]![[Pasted image 20251208160538.png]]![[Pasted image 20251208160539.png]]![[Pasted image 20251208160539.png]]


---
---
Tengo un proyecto de Fine-Tuning de un Tutor Inteligente de Algoritmos, el cual tiene como objetivo desarrollar y entrenar un modelo de lenguaje especializado en la enseñanza de algoritmos, utilizando técnicas de fine-tuning. La intención es crear un Tutor Inteligente de Algoritmos capaz de explicar conceptos, resolver ejercicios, generar ejemplos, evaluar soluciones propuestas y acompañar a los estudiantes durante el aprendizaje de estructuras de datos y diseño algorítmico.

Este tutor será adaptado a necesidades reales mediante un conjunto curado de datos provenientes de explicaciones, ejercicios, pseudocódigo, problemas clásicos de algoritmia y diálogos pedagógicos. El modelo resultante ofrecerá respuestas claras, progresivas y alineadas con buenas prácticas educativas.

Ayúdame a desarrollar el proyecto, teniendo además en cuenta:

Objetivo General

Entrenar y evaluar un modelo de lenguaje mediante fine-tuning para que opere como un tutor especializado en enseñanza de algoritmos, capaz de brindar explicaciones comprensibles, detalladas y adaptadas a distintos niveles de dominio.  
Objetivos Específicos

code Code

downloadcontent_copy

expand_less

`Diseñar un dataset educativo compuesto por explicaciones paso a paso, ejercicios resueltos y conversaciones tutor-estudiante. Realizar el preprocesamiento, limpieza y segmentación del dataset. Entrenar un modelo base de lenguaje mediante fine-tuning supervisado. Evaluar el desempeño del tutor en ejercicios de complejidad y explicación. Ajustar parámetros del modelo según métricas como claridad, precisión y coherencia pedagógica. Generar versiones iterativas del tutor para distintos niveles (básico, intermedio, avanzado).`
  

Planteamiento del Problema

A muchos estudiantes les resulta difícil comprender algoritmos debido a:

code Code

downloadcontent_copy

expand_less

`Falta de explicaciones detalladas o contextualizadas. Escasez de ejemplos paso a paso. Dificultad para visualizar el funcionamiento interno. Ausencia de retroalimentación inmediata.`
  

Un sistema de tutoría inteligente puede resolver estas limitaciones mediante explicaciones personalizadas, ejercicios graduados y retroalimentación guiada.  
Metodología

El proyecto se divide en las siguientes puntos:

code Code

downloadcontent_copy

expand_less

`Definir el alcance exacto del tutor y los temas principales. Seleccionar el modelo base para entrenamiento. Crear un repositorio inicial de problemas de algoritmos. Diseñar un conjunto de explicaciones pedagógicas claras. Redactar ejemplos de interacción tutor-estudiante. Normalizar y limpiar el corpus. Dividir datos en entrenamiento, validación y prueba. Formatear datos en estructura de instrucciones. Implementar el pipeline de fine-tuning. Ajustar hiperparámetros de entrenamiento. Probar explicaciones generadas en ejercicios básicos. Evaluar la coherencia del modelo en problemas recursivos. Medir la calidad de razonamiento en grafos. Revisar las respuestas para detectar errores. Ampliar el dataset según necesidades encontradas. Entrenar nuevamente el modelo con datos corregidos. Evaluar desempeño comparando con un baseline. Integrar el tutor en una interfaz simple. Preparar una guía de uso para estudiantes. Generar ejemplos de preguntas recomendadas. Crear una sección de ejercicios automáticos. Documentar todo el proyecto para evaluación final.`
  

Resultados Esperados

code Code

downloadcontent_copy

expand_less

`Un tutor especializado capaz de explicar algoritmos. Un modelo entrenado con datos cuidadosamente curados. Una herramienta útil para estudiantes de computación. Un sistema adaptable para incluir nuevos temas.`
  

teniendo en cuenta que mi hardware es una laptop thinkpad t14 gen2 con core i7 1185g7 48 GB de RAM e intel iris xe graphics

---
---

me parece perfecta la hoja de ruta, primero comencemos con el desarrollo del dataset, existe algun dataset ya creado con ejemplos? o como puedo escribir un prompt para chatgpt que me genere el dataset

---
---
