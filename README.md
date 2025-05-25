# Design and Development of a Knowledge-Graph Based System to Enhance Large Language Models in Retrieval-Augmented Generation Scenarios

This project aims to design and develop an intelligent system that enhances Large Language Models (LLMs) by integrating knowledge graph structures. A key aspect of this approach is the implementation of Retrieval-Augmented Generation (RAG) techniques, leveraging knowledge graphs to provide structured, contextually relevant, and factual information to LLMs.

---

## Installation

1. Download or clone the project from GitHub.
2. Navigate to the project folder:

   ```bash
   cd proyecto
````

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
├── data/                 # Directory for input/output data
├── import/               # Import scripts or data assets
├── langchain/            # Backend and LangChain integration
│   ├── backend.py        # Main controller and request dispatcher
│   ├── consultas.py      # Functions to query the knowledge graph
│   ├── langchain_api.py  # LangChain API interface
│   ├── Dockerfile        # Dockerfile for the backend service
│   └── requirements.txt  # Python dependencies for backend
├── logs/                 # System and app logs
├── plugins/              # Custom plugins or extensions
├── scripts/              # Data loading and transformation logic
│   ├── load_data.py      # Script to insert data into the knowledge graph
│   ├── load_data.cql     # Cypher queries to populate the graph database
│   ├── Dockerfile        # Dockerfile for the loader service
│   └── requirements.txt  # Dependencies for data loader
├── streamlit/            # Frontend components and app
│   ├── streamlit_app.py       # Main Streamlit interface
│   ├── streamlit_estilos.py  # Custom styles and UI configuration
│   ├── Dockerfile             # Dockerfile for the frontend service
│   └── requirements.txt       # Frontend dependencies
├── docker-compose.yml    # Docker configuration for all services
└── README.md             # This file
```

---

## File Responsibilities

### `langchain/`

* **backend.py**: Orquestra el flujo de peticiones desde el frontend y gestiona la lógica de negocio.
* **consultas.py**: Contiene funciones para consultar el grafo de conocimiento con Cypher.
* **langchain\_api.py**: Define la interfaz para conectar LangChain con el sistema.
* **Dockerfile** y **requirements.txt**: Configuración del entorno backend.

### `scripts/`

* **load\_data.py**: Lee y procesa datos para insertarlos en el grafo.
* **load\_data.cql**: Contiene las sentencias Cypher para poblar la base de datos.
* **Dockerfile** y **requirements.txt**: Entorno de carga de datos.

### `streamlit/`

* **streamlit\_app.py**: Aplicación principal de visualización e interacción.
* **streamlit\_estilos.py**: Define estilos y configuraciones visuales.
* **Dockerfile** y **requirements.txt**: Entorno de frontend.
