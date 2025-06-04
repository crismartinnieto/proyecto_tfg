import json
from neo4j import GraphDatabase
import re

# Configuración de la conexión a Neo4j
NEO4J_URI = "bolt://neo4j:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

# Ruta del archivo JSON
JSON_FILE_PATH = "/app/records.json"


def sanitize_label(label):
    # Reemplaza cualquier carácter que no sea letra, número o guion bajo por guion bajo
    label = re.sub(r'[^a-zA-Z0-9_]', '_', label)
    return label


def create_node(tx, label, properties):
    safe_label = sanitize_label(label)  # <--- esto lo arregla

    query = f"""
    MERGE (n:{safe_label} {{nombre: $nombre}})
    SET n += $props
    """
    tx.run(query, nombre=properties.get("nombre"), props=properties)


def create_relationship(tx, start_label, start_nombre, rel_type, end_label, end_nombre):
    safe_start_label = sanitize_label(start_label)
    safe_end_label = sanitize_label(end_label)
    safe_rel_type = sanitize_label(rel_type)  

    query = f"""
    MATCH (a:{safe_start_label} {{nombre: $start_nombre}})
    MATCH (b:{safe_end_label} {{nombre: $end_nombre}})
    MERGE (a)-[r:{safe_rel_type}]->(b)
    """
    try:
        tx.run(query, start_nombre=start_nombre, end_nombre=end_nombre)
    except Exception as e:
        print(f"Error running query:\n{query}\nWith params: start_nombre={start_nombre}, end_nombre={end_nombre}")
        print("Exception:", e)
        raise


def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with open(JSON_FILE_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    with driver.session() as session:
        for item in data:
            n = item.get("n")
            m = item.get("m")
            r = item.get("r")

            # Saltar si falta 'n' o sus propiedades
            if not n or "properties" not in n:
                print("❌ Nodo 'n' inválido:", item)
                continue

            # Completar 'nombre' desde 'id' si falta
            n["properties"]["nombre"] = n["properties"].get("nombre", n["properties"].get("id"))

            # Validar que 'nombre' exista después de fallback
            if not n["properties"].get("nombre"):
                print("❌ Nodo sin 'nombre':", item)
                continue

            # Crear nodo n
            session.execute_write(create_node, n["labels"][0], n["properties"])

            if m and "properties" in m:
                # Fallback para m también
                m["properties"]["nombre"] = m["properties"].get("nombre", m["properties"].get("id"))

                if not m["properties"].get("nombre"):
                    print("❌ Nodo 'm' sin 'nombre':", item)
                    continue

                # Crear nodo m
                session.execute_write(create_node, m["labels"][0], m["properties"])

                # Crear relación solo si hay relación definida
                if r:
                    session.execute_write(
                        create_relationship,
                        n["labels"][0],
                        n["properties"]["nombre"],
                        r["type"],
                        m["labels"][0],
                        m["properties"]["nombre"]
                    )


    print("✅ Carga de datos desde JSON completada correctamente.")
    driver.close()


if __name__ == "__main__":
    main()
