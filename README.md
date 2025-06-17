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
---

## Check database is full

1. Open your web browser and go to the following address: [http://localhost:7474](http://localhost:7474)

2. Log in with the configured credentials. 

Username: neo4j

Password: password

3. Once inside, you will use the Neo4j Browser interface to run Cypher queries and explore the database.
  ```bash
  MATCH (n)
  OPTIONAL MATCH (n)-[r]->(m)
  RETURN n, r, m
  ```

## Project Structure

```
proyecto/
├── data/                              
├── import/            
│   ├── records_train.csv          
├── logs/                 
├── plugins/              
├── scripts/              
│   ├── main.py   
│   ├── requirements.txt   
│   ├── Dockerfile              
├── docker-compose.yml    
└── README.md             
```

---

## File Explications

### `import/`

* **records_train.csv**: CSV con las descripciones de las universidades a procesar

### `scripts/`

* **main.py**: Script en Python que se encarga de transformar los documentos a un grafo. 
* **Dockerfile** y **requirements.txt**: Configuración del entorno para ejecutar el script de carga de datos en un contenedor Docker con las dependencias necesarias.
