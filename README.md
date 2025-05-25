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

## File Responsibilities

### `langchain/`

* **backend.py**: Orquesta el flujo de consulta intentando obtener respuestas primero desde Neo4j, luego desde Wikidata, luego DBpedia, y finalmente desde un modelo LLM local si todo lo anterior falla.
* **consultas.py**:  Implementa funciones para consultar Neo4j, Wikidata, DBpedia y el modelo LLM local, encargándose de obtener y procesar respuestas según la fuente.
* **langchain_api.py**: Expone una API REST con Flask que recibe preguntas vía POST, llama a backend.py y devuelve la respuesta en formato JSON.
* **Dockerfile** y **requirements.txt**: Define la imagen de Docker que instala las dependencias y lanza el servicio Flask al arrancar el contenedor.

### `scripts/`

* **load\_data.py**: Lee y procesa datos para insertarlos en el grafo.
* **load\_data.cql**: Contiene las sentencias Cypher para poblar la base de datos.
* **Dockerfile** y **requirements.txt**: Entorno de carga de datos.

### `streamlit/`

* **streamlit\_app.py**: Aplicación principal de visualización e interacción.
* **streamlit\_estilos.py**: Define estilos y configuraciones visuales.
* **Dockerfile** y **requirements.txt**: Entorno de frontend.
