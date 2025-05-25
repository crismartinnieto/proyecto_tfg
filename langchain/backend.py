import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

from consultas import get_response_from_neo4j, get_response_from_wikidata, get_response_from_dbpedia, get_response_from_llm

# Esperar a que Neo4j esté listo
print("Esperando a que Neo4j esté listo...")
time.sleep(20)


def process_question(pregunta, usar_wikidata=True, usar_dbpedia=True):
    # 1. Intentar con Neo4j
    respuesta_neo4j = get_response_from_neo4j(pregunta)
    if respuesta_neo4j:
        return respuesta_neo4j

    # 2. Intentar con Wikidata si está permitido
    if usar_wikidata:
        logger.info("🔁 Intentando con Wikidata...")
        respuesta_wikidata = get_response_from_wikidata(pregunta)
        if respuesta_wikidata:
            return respuesta_wikidata

    # 3. Intentar con DBpedia si está permitido
    if usar_dbpedia:
        logger.info("🔁 Intentando con DBpedia...")
        respuesta_dbpedia = get_response_from_dbpedia(pregunta)
        if respuesta_dbpedia:
            return respuesta_dbpedia

    # LLM como último recurso
    return get_response_from_llm(pregunta)

