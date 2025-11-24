from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# Crear un vectorizador TF-IDF
vectorizer = TfidfVectorizer()

texts = '''
@paezvarela @alvaro_delgado @ARBedolla Esta noche en #LosPeriodistas, @paezvarela le pregunta a @ARBedolla quién considera que podría estar buscando politizar el caso de Carlos Manzo. 🎙️⚖️

Mira su respuesta completa y el análisis a fondo en una conversación clave para entender este tema.

🕕 Únete a la conversación https://t.co/tEAMUEdFiH
'''
# Transformar los textos en vectores
X = vectorizer.fit_transform(texts)

# Aplicar K-Means con 3 centroides
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

# Obtener los cluster de cada texto
clusters = kmeans.predict(X)

