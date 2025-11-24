import requests
import os
import time
import cv2 as cv
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ============================================================================
# CONFIGURACIÓN DE APIs - Obtener keys gratuitas en:
# - Unsplash: https://unsplash.com/developers (50 req/hora)
# - Pexels: https://www.pexels.com/api/ (200 req/hora)
# - Pixabay: https://pixabay.com/api/docs/ (100 req/min)
# ============================================================================
UNSPLASH_ACCESS_KEY = 'komiVlwErqS32kH8jVDaH7AsgwICy_3HKsnJljqZav4'
PEXELS_API_KEY = 'YgyqiDEJD4jkRSShDNHTcVw3CSSAnI4A70bwNFij5Qt1NrkVpTo3nDu7'
PIXABAY_API_KEY = '52990197-9b8095d9ac5e09307b24c7bcb'

# Configuración general
OUTPUT_DIR = './.training_images/emotions'
TEMP_DIR = './.training_images/temp_downloads'
FACE_SIZE = (100, 100)
IMAGES_PER_EMOTION = 3000  # 3000 por emoción
MAX_WORKERS = 10  # Descargas paralelas

# Emociones y términos de búsqueda
EMOTIONS = {
    'happy': ['happy', 'smile', 'joy', 'cheerful', 'laughing'],
    'angry': ['angry', 'mad', 'furious', 'rage', 'upset'],
    'sad': ['sad', 'crying', 'depressed', 'tears', 'sorrow']
}

# Thread-safe counter
class Counter:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = 0
    
    def increment(self):
        with self.lock:
            self.value += 1
            return self.value

downloaded_counter = Counter()
faces_counter = Counter()

def create_directories():
    os.makedirs(TEMP_DIR, exist_ok=True)
    for emotion in EMOTIONS.keys():
        os.makedirs(os.path.join(OUTPUT_DIR, emotion), exist_ok=True)

def detect_and_crop_face(image_path):
    try:
        img = cv.imread(image_path)
        if img is None:
            return None
        
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) == 0:
            return None
        
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        margin = int(0.2 * min(w, h))
        x, y = max(0, x - margin), max(0, y - margin)
        w = min(img.shape[1] - x, w + 2 * margin)
        h = min(img.shape[0] - y, h + 2 * margin)

        face_img = img[y:y+h, x:x+w]
        return cv.resize(face_img, FACE_SIZE, interpolation=cv.INTER_AREA)
    except:
        return None

def download_and_process(url, emotion, face_number):
    """Descargar y procesar una imagen (paralelizable)"""
    temp_path = os.path.join(TEMP_DIR, f"temp_{threading.get_ident()}_{time.time()}.jpg")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False
        
        with open(temp_path, 'wb') as f:
            f.write(response.content)
        
        downloaded_counter.increment()
        
        face_img = detect_and_crop_face(temp_path)
        
        if face_img is not None:
            emotion_dir = os.path.join(OUTPUT_DIR, emotion)
            filename = f"{emotion}_{face_number:04d}.jpg"
            cv.imwrite(os.path.join(emotion_dir, filename), face_img)
            faces_counter.increment()
            os.remove(temp_path)
            return True
        
        os.remove(temp_path)
        return False
    except Exception as e:
        try:
            os.remove(temp_path)
        except:
            pass
        return False

def search_pixabay(query, page=1):
    if PIXABAY_API_KEY == 'TU_PIXABAY_KEY':
        return []
    
    url = 'https://pixabay.com/api/'
    params = {
        'key': PIXABAY_API_KEY,
        'q': f'{query} face person',
        'image_type': 'photo',
        'page': page,
        'per_page': 200,
        'safesearch': 'true'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [photo['largeImageURL'] for photo in data.get('hits', [])]
    except:
        pass
    return []

def search_pexels(query, page=1):
    if PEXELS_API_KEY == 'TU_PEXELS_KEY':
        return []
    
    url = 'https://api.pexels.com/v1/search'
    headers = {'Authorization': PEXELS_API_KEY}
    params = {
        'query': f'{query} face portrait person',
        'page': page,
        'per_page': 80,
        'orientation': 'portrait'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [photo['src']['large'] for photo in data.get('photos', [])]
    except:
        pass
    return []

def search_unsplash(query, page=1):
    if UNSPLASH_ACCESS_KEY == 'TU_UNSPLASH_KEY':
        return []
    
    url = 'https://api.unsplash.com/search/photos'
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    params = {
        'query': f'{query} face portrait',
        'page': page,
        'per_page': 30,
        'orientation': 'portrait'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [photo['urls']['regular'] for photo in data.get('results', [])]
    except:
        pass
    return []

def download_emotion_images(emotion, queries, target_count):
    print(f"\n{'='*70}")
    print(f"📥 EMOCIÓN: {emotion.upper()} - Meta: {target_count} caras")
    print(f"{'='*70}")
    
    emotion_dir = os.path.join(OUTPUT_DIR, emotion)
    saved_count = len([f for f in os.listdir(emotion_dir) if f.endswith('.jpg')])
    
    if saved_count >= target_count:
        print(f"✓ Ya tienes {saved_count} caras. Saltando...")
        return saved_count
    
    print(f"Actual: {saved_count} | Faltan: {target_count - saved_count}")
    
    # APIs con prioridad (de más generosa a menos)
    apis = [
        ('Pixabay', search_pixabay, 10),
        #('Pexels', search_pexels, 5),
        #('Unsplash', search_unsplash, 3)
    ]
    
    start_time = time.time()
    last_count = saved_count
    
    for query in queries:
        if saved_count >= target_count:
            break
        
        print(f"\n🔍 '{query}':")
        
        for api_name, api_func, max_pages in apis:
            if saved_count >= target_count:
                break
            
            print(f"  {api_name}: ", end='', flush=True)
            
            for page in range(1, max_pages + 1):
                if saved_count >= target_count:
                    break
                
                urls = api_func(query, page)
                if not urls:
                    print("❌", end='', flush=True)
                    break
                
                # Descargar en paralelo
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    futures = []
                    for url in urls:
                        if saved_count >= target_count:
                            break
                        saved_count += 1
                        future = executor.submit(download_and_process, url, emotion, saved_count)
                        futures.append(future)
                    
                    # Esperar resultados
                    for future in as_completed(futures):
                        pass
                
                current_faces = len([f for f in os.listdir(emotion_dir) if f.endswith('.jpg')])
                new_faces = current_faces - last_count
                last_count = current_faces
                
                detection_rate = (faces_counter.value / downloaded_counter.value * 100) if downloaded_counter.value > 0 else 0
                
                print(f" p{page}[+{new_faces}]", end='', flush=True)
                
                if current_faces >= target_count:
                    saved_count = current_faces
                    break
                
                time.sleep(0.5)
            
            saved_count = len([f for f in os.listdir(emotion_dir) if f.endswith('.jpg')])
            elapsed = time.time() - start_time
            rate = saved_count / elapsed if elapsed > 0 else 0
            
            print(f" → {saved_count}/{target_count} ({rate:.1f}/s, {detection_rate:.1f}% det)")
            
            if saved_count >= target_count:
                break
            
            time.sleep(1)
    
    return saved_count

def main():
    print("="*70)
    print("DESCARGADOR RÁPIDO DE EMOCIONES (PARALELO)")
    print("="*70)
    
    # Verificar APIs
    apis_ok = []
    if PIXABAY_API_KEY != 'TU_PIXABAY_KEY':
        apis_ok.append('Pixabay ✓')
    if PEXELS_API_KEY != 'TU_PEXELS_KEY':
        apis_ok.append('Pexels ✓')
    if UNSPLASH_ACCESS_KEY != 'TU_UNSPLASH_KEY':
        apis_ok.append('Unsplash ✓')
    
    if not apis_ok:
        print("\n⚠️  ERROR: Configura al menos una API")
        print("\n📋 Obtener keys gratis:")
        print("   • Pixabay (RECOMENDADO): https://pixabay.com/api/docs/")
        print("   • Pexels: https://www.pexels.com/api/")
        print("   • Unsplash: https://unsplash.com/developers")
        return
    
    print(f"\n✓ APIs: {', '.join(apis_ok)}")
    print(f"✓ Descargas paralelas: {MAX_WORKERS}")
    print(f"✓ Meta: {IMAGES_PER_EMOTION} caras/emoción")
    
    create_directories()
    
    overall_start = time.time()
    
    for emotion, queries in EMOTIONS.items():
        download_emotion_images(emotion, queries, IMAGES_PER_EMOTION)
    
    # Limpiar
    try:
        for file in os.listdir(TEMP_DIR):
            os.remove(os.path.join(TEMP_DIR, file))
        os.rmdir(TEMP_DIR)
    except:
        pass
    
    # Resumen
    total_time = time.time() - overall_start
    print(f"\n{'='*70}")
    print("RESUMEN FINAL")
    print(f"{'='*70}")
    
    total = 0
    for emotion in EMOTIONS.keys():
        count = len([f for f in os.listdir(os.path.join(OUTPUT_DIR, emotion)) if f.endswith('.jpg')])
        total += count
        progress = (count / IMAGES_PER_EMOTION * 100)
        bar = '█' * int(progress / 5) + '░' * (20 - int(progress / 5))
        print(f"  {emotion.capitalize():8s}: {count:4d} [{bar}] {progress:.1f}%")
    
    detection_rate = (faces_counter.value / downloaded_counter.value * 100) if downloaded_counter.value > 0 else 0
    
    print(f"\n  Total caras: {total}")
    print(f"  Tiempo: {total_time/60:.1f} min")
    print(f"  Velocidad: {total/total_time:.1f} caras/seg")
    print(f"  Descargadas: {downloaded_counter.value}")
    print(f"  Detección: {detection_rate:.1f}%")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
