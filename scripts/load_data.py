from neo4j import GraphDatabase

# Configuración de la conexión a Neo4j
NEO4J_URI = "bolt://neo4j_container:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# Ruta del archivo CQL
CQL_FILE_PATH = "/app/load_data.cql"

def execute_cql_script(session, file_path):
    """Carga y ejecuta un archivo CQL en la base de datos Neo4j."""
    with open(file_path, "r", encoding="utf-8") as file:
        cql_script = file.read()
    
    queries = cql_script.split(";")  # Dividir el script en consultas individuales
    for query in queries:
        query = query.strip()
        if query:
            session.run(query)
    print("Carga de datos completada correctamente.")

def main():
    """Función principal para ejecutar el script de carga de datos."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        execute_cql_script(session, CQL_FILE_PATH)
    print("Carga de datos completada correctamente. 100%")
    driver.close()

if __name__ == "__main__":
    main()
