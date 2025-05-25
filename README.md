# Design and Development of a Knowledge-Graph Based System to Enhance Large Language Models in Retrieval-Augmented Generation Scenarios

This project aims to design and develop an intelligent system that enhances Large Language Models (LLMs) by integrating knowledge graph structures. A key aspect of this approach is the implementation of Retrieval-Augmented Generation (RAG) techniques, leveraging knowledge graphs to provide structured, contextually relevant, and factual information to LLMs.

---

## Installation

1. Download or clone the project from GitHub.
2. Navigate to the project folder:

   ```bash
   cd proyecto
   ```
3. Create the required directories:

   ```bash
   mkdir data logs plugins
   ```
4. Build and start the containers:

   ```bash
   docker compose up --build
   ```
5. Open your browser and go to: [http://localhost:8501](http://localhost:8501)

---

## Project Structure

```
proyecto/
├── data/                 
├── import/               
├── langchain/            
│   ├── backend.py        
│   ├── consultas.py      
│   ├── langchain_api.py  
│   ├── Dockerfile        
│   └── requirements.txt  
├── logs/                 
├── plugins/              
├── scripts/              
│   ├── load_data.py      
│   ├── load_data.cql     
│   ├── Dockerfile        
├── streamlit/            
│   ├── streamlit_app.py       
│   ├── streamlit_estilos.py  
│   ├── Dockerfile             
│   └── requirements.txt       
├── docker-compose.yml    
└── README.md             
```

---

## File Explications

### `langchain/`

* **backend.py**: Orquesta el flujo de consulta intentando obtener respuestas primero desde Neo4j, luego desde Wikidata, luego DBpedia, y finalmente desde un modelo LLM local si todo lo anterior falla.
* **consultas.py**:  Implementa funciones para consultar Neo4j, Wikidata, DBpedia y el modelo LLM local, encargándose de obtener y procesar respuestas según la fuente.
* **langchain_api.py**: Expone una API REST con Flask que recibe preguntas vía POST, llama a backend.py y devuelve la respuesta en formato JSON.
* **Dockerfile** y **requirements.txt**: Define la imagen de Docker que instala las dependencias y lanza el servicio Flask al arrancar el contenedor.

### `scripts/`

* **load_data.py**: Script en Python que carga datos CSV en la base de datos Neo4j usando el lenguaje Cypher.
* **load_data.cql**: Script Cypher que define las instrucciones para crear nodos y relaciones en Neo4j a partir de los datos.
* **Dockerfile** y **requirements.txt**: Configuración del entorno para ejecutar el script de carga de datos en un contenedor Docker con las dependencias necesarias.

### `streamlit/`

* **streamlit_app.py**: Archivo principal de la aplicación que permite al usuario introducir preguntas, seleccionar fuentes de datos (Wikidata, DBpedia) y visualizar las respuestas devueltas por una API.
* **streamlit_estilos.py**: Módulo que personaliza visualmente la interfaz de Streamlit con estilos institucionales y muestra los logos de la UPM y el GSI.
* **Dockerfile** y **requirements.txt**: Define la imagen Docker para desplegar la aplicación de Streamlit, instalando las dependencias necesarias y configurando el puerto de acceso.
