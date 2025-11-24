from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar los datos de texto
textos = ["Este es un ejemplo de texto 1.", "Este es otro ejemplo de texto 2."]

# Convertir cada texto en un vector de características mediante TF-IDF
vectorizador = TfidfVectorizer()
matriz_de_textos = vectorizador.fit_transform(textos)

# Calcular la similitud de cúspide entre los dos vectores
similitud_coseno = cosine_similarity(matriz_de_textos[0].toarray(), matriz_de_textos[1].toarray())

print("Similitud de cúspide:", similitud_coseno)

