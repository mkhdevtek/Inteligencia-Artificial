import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud

# Si usas nltk para análisis más avanzado
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    NLTK_AVAILABLE = True
except:
    NLTK_AVAILABLE = False

# 1. CARGA Y EXPLORACIÓN INICIAL
def cargar_corpus(ruta_csv, columna_texto, encoding='utf-8'):
    """Carga el dataset CSV"""
    df = pd.read_csv(ruta_csv, encoding=encoding)
    print(f"📊 Dataset cargado: {len(df)} documentos")
    print(f"📋 Columnas disponibles: {list(df.columns)}")
    return df

def exploracion_basica(df, columna_texto):
    """Análisis exploratorio básico del corpus"""
    print("\n" + "="*60)
    print("EXPLORACIÓN BÁSICA DEL CORPUS")
    print("="*60)
    
    # Estadísticas generales
    df['longitud'] = df[columna_texto].astype(str).str.len()
    df['num_palabras'] = df[columna_texto].astype(str).str.split().str.len()
    
    print(f"\n📝 Total de documentos: {len(df)}")
    print(f"📊 Caracteres por documento:")
    print(f"   - Promedio: {df['longitud'].mean():.0f}")
    print(f"   - Mínimo: {df['longitud'].min()}")
    print(f"   - Máximo: {df['longitud'].max()}")
    print(f"\n💬 Palabras por documento:")
    print(f"   - Promedio: {df['num_palabras'].mean():.1f}")
    print(f"   - Mínimo: {df['num_palabras'].min()}")
    print(f"   - Máximo: {df['num_palabras'].max()}")
    
    return df

# 2. LIMPIEZA Y PREPROCESAMIENTO
def limpiar_texto(texto):
    """Limpia y normaliza el texto"""
    texto = str(texto).lower()
    # Eliminar URLs
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto)
    # Eliminar menciones y hashtags (opcional)
    texto = re.sub(r'@\w+|#\w+', '', texto)
    # Eliminar caracteres especiales y números
    texto = re.sub(r'[^a-záéíóúñü\s]', '', texto)
    # Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def preprocesar_corpus(df, columna_texto):
    """Preprocesa todo el corpus"""
    print("\n🔧 Preprocesando textos...")
    df['texto_limpio'] = df[columna_texto].apply(limpiar_texto)
    return df

# 3. ANÁLISIS DE FRECUENCIA DE PALABRAS
def analizar_frecuencias(df, columna_texto, top_n=20, stopwords_es=None):
    """Analiza frecuencia de palabras"""
    
    # Stopwords en español
    if stopwords_es is None:
        stopwords_es = set([
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no',
            'haber', 'por', 'con', 'su', 'para', 'como', 'estar', 'tener',
            'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o', 'poder', 'decir',
            'este', 'ir', 'otro', 'ese', 'la', 'si', 'me', 'ya', 'ver', 'porque',
            'dar', 'cuando', 'él', 'muy', 'sin', 'vez', 'mucho', 'saber', 'qué',
            'sobre', 'mi', 'alguno', 'mismo', 'yo', 'también', 'hasta', 'año',
            'dos', 'querer', 'entre', 'así', 'primero', 'desde', 'grande', 'eso',
            'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella', 'sí', 'día', 'uno',
            'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa', 'tanto', 'hombre',
            'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte', 'después', 'vida',
            'quedar', 'siempre', 'creer', 'hablar', 'llevar', 'dejar', 'nada', 'cada',
            'seguir', 'menos', 'nuevo', 'encontrar', 'algo', 'solo', 'decir', 'llamar'
        ])
    
    # Concatenar todos los textos
    texto_completo = ' '.join(df[columna_texto].astype(str))
    palabras = texto_completo.split()
    
    # Filtrar stopwords y palabras cortas
    palabras_filtradas = [p for p in palabras if p not in stopwords_es and len(p) > 2]
    
    # Contar frecuencias
    frecuencias = Counter(palabras_filtradas)
    palabras_comunes = frecuencias.most_common(top_n)
    
    print("\n" + "="*60)
    print(f"🔤 TOP {top_n} PALABRAS MÁS FRECUENTES")
    print("="*60)
    for palabra, freq in palabras_comunes:
        print(f"{palabra:20s} : {freq:5d} veces")
    
    return frecuencias, palabras_comunes

# 4. VISUALIZACIONES
def crear_wordcloud(frecuencias, titulo="Nube de Palabras"):
    """Crea una nube de palabras"""
    plt.figure(figsize=(12, 6))
    
    wordcloud = WordCloud(
        width=800, 
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate_from_frequencies(frecuencias)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(titulo, fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()

def grafico_barras_frecuencias(palabras_comunes, top_n=20):
    """Gráfico de barras de palabras más comunes"""
    palabras, frecuencias = zip(*palabras_comunes[:top_n])
    
    plt.figure(figsize=(12, 8))
    plt.barh(range(len(palabras)), frecuencias, color='steelblue')
    plt.yticks(range(len(palabras)), palabras)
    plt.xlabel('Frecuencia', fontsize=12)
    plt.ylabel('Palabras', fontsize=12)
    plt.title(f'Top {top_n} Palabras Más Frecuentes', fontsize=14, pad=20)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()

def analisis_longitud(df):
    """Visualiza distribución de longitudes"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histograma de longitud en caracteres
    axes[0].hist(df['longitud'], bins=30, color='skyblue', edgecolor='black')
    axes[0].set_xlabel('Caracteres')
    axes[0].set_ylabel('Frecuencia')
    axes[0].set_title('Distribución de Longitud (caracteres)')
    axes[0].grid(alpha=0.3)
    
    # Histograma de número de palabras
    axes[1].hist(df['num_palabras'], bins=30, color='lightcoral', edgecolor='black')
    axes[1].set_xlabel('Palabras')
    axes[1].set_ylabel('Frecuencia')
    axes[1].set_title('Distribución de Longitud (palabras)')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 5. ANÁLISIS POR CATEGORÍAS (si existen)
def analisis_por_categoria(df, columna_texto, columna_categoria):
    """Analiza el corpus por categorías"""
    if columna_categoria not in df.columns:
        print(f"⚠️  Columna '{columna_categoria}' no encontrada")
        return
    
    print("\n" + "="*60)
    print("📑 ANÁLISIS POR CATEGORÍAS")
    print("="*60)
    
    for categoria in df[columna_categoria].unique():
        subset = df[df[columna_categoria] == categoria]
        print(f"\n🏷️  {categoria}")
        print(f"   Documentos: {len(subset)}")
        print(f"   Promedio palabras: {subset['num_palabras'].mean():.1f}")

# FUNCIÓN PRINCIPAL
def analizar_corpus_completo(ruta_csv, columna_texto, columna_categoria=None):
    """Ejecuta análisis completo del corpus"""
    
    # 1. Cargar datos
    df = cargar_corpus(ruta_csv, columna_texto)
    
    # 2. Exploración básica
    df = exploracion_basica(df, columna_texto)
    
    # 3. Limpiar textos
    df = preprocesar_corpus(df, columna_texto)
    
    # 4. Análisis de frecuencias
    frecuencias, palabras_comunes = analizar_frecuencias(df, 'texto_limpio', top_n=20)
    
    # 5. Visualizaciones
    print("\n📊 Generando visualizaciones...")
    grafico_barras_frecuencias(palabras_comunes, top_n=20)
    crear_wordcloud(frecuencias, "Nube de Palabras del Corpus")
    analisis_longitud(df)
    
    # 6. Análisis por categorías (si existe)
    if columna_categoria:
        analisis_por_categoria(df, columna_texto, columna_categoria)
    
    return df, frecuencias

# EJEMPLO DE USO
if __name__ == "__main__":
    # Reemplaza con tu archivo CSV
    ruta_csv = './datasetTexto.csv'  # Tu archivo
    columnas_texto = [
        'Titulo',
        'Medio',
        'Resumen',
        'Comentario_Reaccion'
    ] # Nombre de la columna con el texto
    columna_categoria = 'Categoria'       # Opcional: columna de categorías
    
    df_analizado = ""

    for columna_texto in columnas_texto:
        # Ejecutar análisis
        df_analizado, frecuencias = analizar_corpus_completo(
            ruta_csv, 
            columna_texto,
            columna_categoria  # Puede ser None si no tienes categorías
        )
    
    # Guardar resultados
    df_analizado.to_csv('corpus_analizado.csv', index=False)
    print("\n✅ Análisis completado y guardado!")
