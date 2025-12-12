import json
import re
from collections import Counter

def limpiar_dataset(archivo_entrada, archivo_salida):
    """
    Limpia un dataset JSONL eliminando duplicados, validando estructura,
    y asegurando calidad de datos.
    """
    
    # Listas para almacenar datos
    datos_originales = []
    datos_limpios = []
    
    # Contadores y estadísticas
    stats = {
        'total_original': 0,
        'duplicados_exactos': 0,
        'prompts_similares': 0,
        'formato_invalido': 0,
        'campos_vacios': 0,
        'respuestas_muy_cortas': 0,
        'caracteres_invalidos': 0,
        'final_limpio': 0
    }
    
    # 1. LEER ARCHIVO
    print("📖 Leyendo archivo...")
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            for linea_num, linea in enumerate(f, 1):
                stats['total_original'] += 1
                try:
                    dato = json.loads(linea.strip())
                    datos_originales.append(dato)
                except json.JSONDecodeError as e:
                    print(f"⚠️  Línea {linea_num}: JSON inválido - {e}")
                    stats['formato_invalido'] += 1
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo_entrada}'")
        return
    
    print(f"✅ Leídos {len(datos_originales)} registros")
    
    # 2. VALIDAR ESTRUCTURA
    print("\n🔍 Validando estructura...")
    datos_validos = []
    
    for i, dato in enumerate(datos_originales):
        # Verificar que tenga los campos necesarios
        if not isinstance(dato, dict):
            stats['formato_invalido'] += 1
            continue
            
        # Detectar el tipo de dataset y normalizar campos
        if 'instruction' in dato and 'output' in dato:
            prompt = dato.get('instruction', '').strip()
            response = dato.get('output', '').strip()
        elif 'prompt' in dato and 'response' in dato:
            prompt = dato.get('prompt', '').strip()
            response = dato.get('response', '').strip()
        else:
            print(f"⚠️  Registro {i+1}: Campos no reconocidos - {list(dato.keys())}")
            stats['formato_invalido'] += 1
            continue
        
        # Validar que no estén vacíos
        if not prompt or not response:
            stats['campos_vacios'] += 1
            continue
        
        # Validar longitud mínima de respuesta
        if len(response) < 50:
            stats['respuestas_muy_cortas'] += 1
            continue
        
        # Normalizar el formato de salida
        datos_validos.append({
            'prompt': prompt,
            'response': response
        })
    
    print(f"✅ {len(datos_validos)} registros con estructura válida")
    
    # 3. ELIMINAR DUPLICADOS EXACTOS
    print("\n🔄 Eliminando duplicados exactos...")
    vistos = set()
    datos_sin_duplicados = []
    
    for dato in datos_validos:
        # Crear un hash del prompt
        dato_hash = hash(dato['prompt'].lower())
        
        if dato_hash not in vistos:
            vistos.add(dato_hash)
            datos_sin_duplicados.append(dato)
        else:
            stats['duplicados_exactos'] += 1
    
    print(f"✅ Eliminados {stats['duplicados_exactos']} duplicados exactos")
    
    # 4. DETECTAR PROMPTS MUY SIMILARES
    print("\n🔍 Detectando prompts similares...")
    
    def similitud_simple(texto1, texto2):
        """Calcula similitud básica entre dos textos"""
        palabras1 = set(texto1.lower().split())
        palabras2 = set(texto2.lower().split())
        
        if not palabras1 or not palabras2:
            return 0
        
        interseccion = palabras1.intersection(palabras2)
        union = palabras1.union(palabras2)
        
        return len(interseccion) / len(union)
    
    datos_unicos = []
    
    for i, dato_actual in enumerate(datos_sin_duplicados):
        es_similar = False
        
        for dato_guardado in datos_unicos:
            similitud = similitud_simple(dato_actual['prompt'], dato_guardado['prompt'])
            
            # Si la similitud es mayor al 80%, considerarlo duplicado
            if similitud > 0.8:
                es_similar = True
                stats['prompts_similares'] += 1
                break
        
        if not es_similar:
            datos_unicos.append(dato_actual)
    
    print(f"✅ Eliminados {stats['prompts_similares']} prompts similares")
    
    # 5. LIMPIAR CARACTERES PROBLEMÁTICOS
    print("\n🧹 Limpiando caracteres problemáticos...")
    
    def limpiar_texto(texto):
        """Elimina caracteres problemáticos y normaliza espacios"""
        # Eliminar caracteres de control excepto saltos de línea y tabs
        texto = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', texto)
        
        # Normalizar múltiples espacios
        texto = re.sub(r' +', ' ', texto)
        
        # Normalizar múltiples saltos de línea
        texto = re.sub(r'\n\n+', '\n\n', texto)
        
        return texto.strip()
    
    for dato in datos_unicos:
        dato_original = str(dato)
        dato['prompt'] = limpiar_texto(dato['prompt'])
        dato['response'] = limpiar_texto(dato['response'])
        
        if str(dato) != dato_original:
            stats['caracteres_invalidos'] += 1
    
    print(f"✅ Limpiados {stats['caracteres_invalidos']} registros con caracteres problemáticos")
    
    # 6. ANÁLISIS DE CALIDAD
    print("\n📊 Análisis de calidad del dataset:")
    
    longitudes_prompts = [len(d['prompt']) for d in datos_unicos]
    longitudes_responses = [len(d['response']) for d in datos_unicos]
    
    print(f"   • Prompts - Min: {min(longitudes_prompts)}, Max: {max(longitudes_prompts)}, Promedio: {sum(longitudes_prompts)//len(longitudes_prompts)}")
    print(f"   • Responses - Min: {min(longitudes_responses)}, Max: {max(longitudes_responses)}, Promedio: {sum(longitudes_responses)//len(longitudes_responses)}")
    
    # Detectar palabras clave más comunes
    todas_palabras = []
    for dato in datos_unicos:
        palabras = re.findall(r'\b\w+\b', dato['prompt'].lower())
        todas_palabras.extend(palabras)
    
    palabras_comunes = Counter(todas_palabras).most_common(10)
    print(f"\n   📝 Palabras más frecuentes en prompts:")
    for palabra, freq in palabras_comunes:
        if len(palabra) > 3:  # Ignorar palabras muy cortas
            print(f"      - {palabra}: {freq} veces")
    
    # 7. GUARDAR DATASET LIMPIO
    datos_limpios = datos_unicos
    stats['final_limpio'] = len(datos_limpios)
    
    print(f"\n💾 Guardando dataset limpio...")
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for dato in datos_limpios:
            json.dump(dato, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"✅ Dataset guardado en '{archivo_salida}'")
    
    # 8. REPORTE FINAL
    print("\n" + "="*60)
    print("📋 REPORTE DE LIMPIEZA")
    print("="*60)
    print(f"Registros originales:        {stats['total_original']}")
    print(f"Formato inválido:            -{stats['formato_invalido']}")
    print(f"Campos vacíos:               -{stats['campos_vacios']}")
    print(f"Respuestas muy cortas:       -{stats['respuestas_muy_cortas']}")
    print(f"Duplicados exactos:          -{stats['duplicados_exactos']}")
    print(f"Prompts similares:           -{stats['prompts_similares']}")
    print(f"Con caracteres problemáticos: {stats['caracteres_invalidos']}")
    print("-"*60)
    print(f"REGISTROS FINALES:           {stats['final_limpio']}")
    print(f"Porcentaje retenido:         {(stats['final_limpio']/stats['total_original']*100):.1f}%")
    print("="*60)
    
    # 9. CREAR ARCHIVO DE ESTADÍSTICAS
    with open('estadisticas_limpieza.txt', 'w', encoding='utf-8') as f:
        f.write("ESTADÍSTICAS DE LIMPIEZA DEL DATASET\n")
        f.write("="*60 + "\n\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
    
    print("\n💡 Estadísticas guardadas en 'estadisticas_limpieza.txt'")


# FUNCIÓN ADICIONAL: VALIDAR DATASET
def validar_dataset(archivo):
    """Valida un dataset sin modificarlo"""
    print(f"\n🔍 Validando dataset: {archivo}")
    
    errores = []
    
    with open(archivo, 'r', encoding='utf-8') as f:
        for i, linea in enumerate(f, 1):
            try:
                dato = json.loads(linea.strip())
                
                # Verificar campos
                if 'prompt' not in dato or 'response' not in dato:
                    if 'instruction' not in dato or 'output' not in dato:
                        errores.append(f"Línea {i}: Campos incorrectos")
                
                # Verificar que no estén vacíos
                prompt = dato.get('prompt', dato.get('instruction', ''))
                response = dato.get('response', dato.get('output', ''))
                
                if not prompt.strip():
                    errores.append(f"Línea {i}: Prompt vacío")
                if not response.strip():
                    errores.append(f"Línea {i}: Response vacío")
                    
            except json.JSONDecodeError:
                errores.append(f"Línea {i}: JSON inválido")
    
    if errores:
        print(f"❌ Se encontraron {len(errores)} errores:")
        for error in errores[:10]:  # Mostrar solo los primeros 10
            print(f"   • {error}")
        if len(errores) > 10:
            print(f"   ... y {len(errores) - 10} errores más")
    else:
        print("✅ Dataset válido - Sin errores encontrados")


# USO DEL SCRIPT
if __name__ == "__main__":
    print("🧹 LIMPIADOR DE DATASETS JSONL")
    print("="*60)
    
    # Archivos
    archivo_entrada = "./dataset.jsonl"
    archivo_salida = "./dataset_limpio.jsonl"
    
    # Limpiar dataset
    limpiar_dataset(archivo_entrada, archivo_salida)
    
    # Validar resultado
    print("\n" + "="*60)
    validar_dataset(archivo_salida)
