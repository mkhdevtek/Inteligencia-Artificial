import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud

# Configuración para mostrar múltiples ventanas
plt.ion()  # Modo interactivo

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
def cargar_corpus(ruta_csv, encoding='utf-8'):
    """Carga el dataset CSV"""
    df = pd.read_csv(ruta_csv, encoding=encoding)
    print(f"📊 Dataset cargado: {len(df)} documentos")
    print(f"📋 Columnas disponibles: {list(df.columns)}")
    return df

def exploracion_basica(df, columnas_texto):
    """Análisis exploratorio básico del corpus para múltiples columnas"""
    print("\n" + "="*60)
    print("EXPLORACIÓN BÁSICA DEL CORPUS")
    print("="*60)
    
    for columna in columnas_texto:
        if columna not in df.columns:
            print(f"⚠️  Columna '{columna}' no encontrada")
            continue
            
        df[f'{columna}_longitud'] = df[columna].astype(str).str.len()
        df[f'{columna}_num_palabras'] = df[columna].astype(str).str.split().str.len()
        
        print(f"\n📝 Análisis de columna: '{columna}'")
        print(f"   Total de documentos: {len(df)}")
        print(f"   📊 Caracteres por documento:")
        print(f"      - Promedio: {df[f'{columna}_longitud'].mean():.0f}")
        print(f"      - Mínimo: {df[f'{columna}_longitud'].min()}")
        print(f"      - Máximo: {df[f'{columna}_longitud'].max()}")
        print(f"   💬 Palabras por documento:")
        print(f"      - Promedio: {df[f'{columna}_num_palabras'].mean():.1f}")
        print(f"      - Mínimo: {df[f'{columna}_num_palabras'].min()}")
        print(f"      - Máximo: {df[f'{columna}_num_palabras'].max()}")
    
    return df

# 2. LIMPIEZA Y PREPROCESAMIENTO
def limpiar_texto(texto):
    """Limpia y normaliza el texto"""
    texto = str(texto).lower()
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto)
    texto = re.sub(r'@\w+|#\w+', '', texto)
    texto = re.sub(r'[^a-záéíóúñü\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def preprocesar_corpus(df, columnas_texto):
    """Preprocesa todas las columnas de texto"""
    print("\n🔧 Preprocesando textos...")
    for columna in columnas_texto:
        if columna in df.columns:
            df[f'{columna}_limpio'] = df[columna].apply(limpiar_texto)
            print(f"   ✓ Columna '{columna}' procesada")
    return df

# 3. ANÁLISIS DE FRECUENCIA DE PALABRAS
def analizar_frecuencias(df, columna_texto, top_n=20, stopwords_es=None):
    """Analiza frecuencia de palabras"""
    
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
    
    texto_completo = ' '.join(df[columna_texto].astype(str))
    palabras = texto_completo.split()
    palabras_filtradas = [p for p in palabras if p not in stopwords_es and len(p) > 2]
    frecuencias = Counter(palabras_filtradas)
    palabras_comunes = frecuencias.most_common(top_n)
    
    return frecuencias, palabras_comunes

# 4. VISUALIZACIONES CONSOLIDADAS
def crear_visualizaciones_todas_columnas(df, columnas_texto, resultados_frecuencias):
    """Crea todas las visualizaciones para todas las columnas en ventanas separadas"""
    
    num_columnas = len(columnas_texto)
    colores = ['steelblue', 'coral', 'mediumseagreen', 'mediumpurple', 'gold', 'crimson']
    
    # FIGURA 1: Gráficos de barras de frecuencias
    fig1 = plt.figure(figsize=(16, 6 * num_columnas), num="Frecuencias de Palabras")
    
    for idx, columna in enumerate(columnas_texto, 1):
        if columna not in resultados_frecuencias:
            continue
        
        palabras_comunes = resultados_frecuencias[columna]['palabras_comunes']
        palabras, frecuencias = zip(*palabras_comunes[:20])
        
        ax = fig1.add_subplot(num_columnas, 1, idx)
        ax.barh(range(len(palabras)), frecuencias, color=colores[idx % len(colores)])
        ax.set_yticks(range(len(palabras)))
        ax.set_yticklabels(palabras)
        ax.set_xlabel('Frecuencia', fontsize=11)
        ax.set_ylabel('Palabras', fontsize=11)
        ax.set_title(f'Top 20 Palabras - {columna}', fontsize=13, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # FIGURA 2: Nubes de palabras
    fig2 = plt.figure(figsize=(18, 6 * ((num_columnas + 1) // 2)), num="Nubes de Palabras")
    
    for idx, columna in enumerate(columnas_texto, 1):
        if columna not in resultados_frecuencias:
            continue
        
        frecuencias = resultados_frecuencias[columna]['frecuencias']
        
        ax = fig2.add_subplot((num_columnas + 1) // 2, 2, idx)
        
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate_from_frequencies(frecuencias)
        
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(f'Nube de Palabras - {columna}', fontsize=13, fontweight='bold', pad=10)
    
    plt.tight_layout()
    
    # FIGURA 3: Distribución de longitudes
    fig3 = plt.figure(figsize=(18, 5 * num_columnas), num="Distribución de Longitudes")
    
    for idx, columna in enumerate(columnas_texto, 1):
        col_longitud = f'{columna}_longitud'
        col_palabras = f'{columna}_num_palabras'
        
        if col_longitud not in df.columns or col_palabras not in df.columns:
            continue
        
        # Caracteres
        ax1 = fig3.add_subplot(num_columnas, 2, idx * 2 - 1)
        ax1.hist(df[col_longitud], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Caracteres', fontsize=10)
        ax1.set_ylabel('Frecuencia', fontsize=10)
        ax1.set_title(f'{columna} - Distribución (caracteres)', fontsize=11, fontweight='bold')
        ax1.grid(alpha=0.3)
        
        # Palabras
        ax2 = fig3.add_subplot(num_columnas, 2, idx * 2)
        ax2.hist(df[col_palabras], bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Palabras', fontsize=10)
        ax2.set_ylabel('Frecuencia', fontsize=10)
        ax2.set_title(f'{columna} - Distribución (palabras)', fontsize=11, fontweight='bold')
        ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    
    # FIGURA 4: Comparación entre columnas
    if num_columnas > 1:
        fig4 = plt.figure(figsize=(16, 8), num="Comparación entre Columnas")
        
        # Subplot 1: Promedio de palabras
        ax1 = fig4.add_subplot(2, 2, 1)
        promedios_palabras = [df[f'{col}_num_palabras'].mean() for col in columnas_texto 
                             if f'{col}_num_palabras' in df.columns]
        ax1.bar(columnas_texto, promedios_palabras, color=colores[:num_columnas])
        ax1.set_ylabel('Promedio de palabras', fontsize=11)
        ax1.set_title('Promedio de Palabras por Columna', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # Subplot 2: Promedio de caracteres
        ax2 = fig4.add_subplot(2, 2, 2)
        promedios_caracteres = [df[f'{col}_longitud'].mean() for col in columnas_texto 
                               if f'{col}_longitud' in df.columns]
        ax2.bar(columnas_texto, promedios_caracteres, color=colores[:num_columnas])
        ax2.set_ylabel('Promedio de caracteres', fontsize=11)
        ax2.set_title('Promedio de Caracteres por Columna', fontsize=12, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        
        # Subplot 3: Vocabulario único
        ax3 = fig4.add_subplot(2, 2, 3)
        vocab_unico = [len(resultados_frecuencias[col]['frecuencias']) for col in columnas_texto
                      if col in resultados_frecuencias]
        ax3.bar(columnas_texto, vocab_unico, color=colores[:num_columnas])
        ax3.set_ylabel('Palabras únicas', fontsize=11)
        ax3.set_title('Vocabulario Único por Columna', fontsize=12, fontweight='bold')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(axis='y', alpha=0.3)
        
        # Subplot 4: Total de palabras
        ax4 = fig4.add_subplot(2, 2, 4)
        total_palabras = [sum(resultados_frecuencias[col]['frecuencias'].values()) 
                         for col in columnas_texto if col in resultados_frecuencias]
        ax4.bar(columnas_texto, total_palabras, color=colores[:num_columnas])
        ax4.set_ylabel('Total de palabras', fontsize=11)
        ax4.set_title('Total de Palabras por Columna', fontsize=12, fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
    
    # Mostrar todas las figuras
    plt.show(block=False)
    print("\n✅ Todas las visualizaciones generadas y mostradas")
    print("💡 Puedes interactuar con todas las ventanas simultáneamente")

# 5. ANÁLISIS POR CATEGORÍAS
def analisis_por_categoria(df, columnas_texto, columna_categoria):
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
        
        for columna in columnas_texto:
            col_palabras = f'{columna}_num_palabras'
            if col_palabras in df.columns:
                print(f"   Promedio palabras ({columna}): {subset[col_palabras].mean():.1f}")

def analizar_corpus_completo(ruta_csv, columnas_texto, columna_categoria=None):
    if isinstance(columnas_texto, str):
        columnas_texto = [columnas_texto]
    
    print(f"\n🚀 Iniciando análisis de {len(columnas_texto)} columna(s) de texto...")
    
    df = cargar_corpus(ruta_csv)
    
    df = exploracion_basica(df, columnas_texto)
    
    df = preprocesar_corpus(df, columnas_texto)
    
    resultados_frecuencias = {}
    
    for columna in columnas_texto:
        columna_limpia = f'{columna}_limpio'
        if columna_limpia in df.columns:
            print(f"\n🔍 Analizando frecuencias para '{columna}'...")
            frecuencias, palabras_comunes = analizar_frecuencias(df, columna_limpia, top_n=20)
            
            resultados_frecuencias[columna] = {
                'frecuencias': frecuencias,
                'palabras_comunes': palabras_comunes
            }
            
            print(f"\n🔤 TOP 20 PALABRAS - {columna}")
            print("-" * 50)
            for palabra, freq in palabras_comunes:
                print(f"{palabra:20s} : {freq:5d} veces")
    
    print("\n📊 Generando todas las visualizaciones...")
    crear_visualizaciones_todas_columnas(df, columnas_texto, resultados_frecuencias)

    if columna_categoria:
        analisis_por_categoria(df, columnas_texto, columna_categoria)
    
    return df, resultados_frecuencias

if __name__ == "__main__":
    ruta_csv = './datasetTexto.csv'
    
    columnas_texto = [
        'Titulo',
        'Medio',
        'Resumen',
        'Comentario_Reaccion'
    ]

    columna_categoria = 'Categoria'  # o None si no tienes
    
    df_analizado, resultados = analizar_corpus_completo(
        ruta_csv, 
        columnas_texto,
        columna_categoria
    )
    
#    df_analizado.to_csv('./corpus_analizado.csv', index=False)
