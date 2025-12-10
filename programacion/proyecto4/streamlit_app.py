import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(
    page_title="Tutor de Algoritmos",
    page_icon="🎓",
    layout="wide"
)

# --- FUNCIONES AUXILIARES ---

def get_ollama_models():
    """Obtiene la lista de modelos disponibles en tu Ollama local."""
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            data = response.json()
            # Extrae solo los nombres de los modelos
            return [model['name'] for model in data['models']]
        else:
            st.error("Error al obtener modelos de Ollama.")
            return []
    except Exception as e:
        st.error(f"No se pudo conectar con Ollama. Asegúrate de que esté corriendo. Error: {e}")
        return []

def generate_response(model_name, conversation_history):
    """Genera una respuesta usando el modelo seleccionado en modo streaming."""
    url = "http://localhost:11434/api/chat"
    
    payload = {
        "model": model_name,
        "messages": conversation_history,
        "stream": True  # Activamos streaming para ver la respuesta mientras se genera
    }
    
    try:
        with requests.post(url, json=payload, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        body = json.loads(line.decode('utf-8'))
                        if 'message' in body and 'content' in body['message']:
                            yield body['message']['content']
            else:
                yield f"Error: {response.text}"
    except Exception as e:
        yield f"Error de conexión: {e}"

# --- INTERFAZ GRÁFICA ---

st.title("🎓 Tutor Inteligente de Algoritmos")
st.markdown("---")

# BARRA LATERAL (SIDEBAR) - Configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # 1. Obtener y seleccionar modelo
    available_models = get_ollama_models()
    
    if available_models:
        # Buscamos si tu modelo final está en la lista para ponerlo por defecto
        default_index = 0
        target_model = "tutor_algoritmos_final:latest" # Ajusta este nombre según como lo guardaste
        
        if target_model in available_models:
            default_index = available_models.index(target_model)
            
        selected_model = st.selectbox(
            "Selecciona el Tutor (Modelo):", 
            available_models, 
            index=default_index
        )
        st.success(f"Modelo activo: **{selected_model}**")
    else:
        st.warning("No se detectaron modelos. Revisa tu conexión a Ollama.")
        selected_model = None

    st.markdown("---")
    if st.button("🗑️ Borrar Historial"):
        st.session_state.messages = []
        st.rerun()

# --- LÓGICA DEL CHAT ---

# Inicializar historial en session_state si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar input del usuario
if prompt := st.chat_input("Escribe tu duda sobre algoritmos..."):
    
    # Agregar mensaje del usuario al historial visual y de contexto
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta del asistente
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Llamamos a la función generadora (Streaming)
        if selected_model:
            # Preparamos el contexto para Ollama (le enviamos el historial)
            # Esto permite que el tutor recuerde lo que dijiste antes
            history_for_ollama = [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages
            ]
            
            for chunk in generate_response(selected_model, history_for_ollama):
                full_response += chunk
                # Actualizamos el contenedor de texto en tiempo real
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        else:
            st.error("Por favor selecciona un modelo válido.")

    # Guardar respuesta del asistente en el historial
    st.session_state.messages.append({"role": "assistant", "content": full_response})
