from langchain_ollama import ChatOllama
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun
from langchain_ollama import ChatOllama
from langchain_community.graphs.rdf_graph import RdfGraph
from langchain_community.chains.graph_qa.sparql import GraphSparqlQAChain
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# Configura la API de Ollama
llm = ChatOllama(model="llama3", base_url="http://ollama.gsi.upm.es")
llm_dbpedia = ChatOllama(model="mistral", base_url="https://ollama.gsi.upm.es/")

# Conexión a Neo4j a través de LangChain
graph = Neo4jGraph(
    url="bolt://neo4j:7687",
    username="neo4j",
    password="password"
)

graph_dbpedia = RdfGraph(
    query_endpoint="https://dbpedia.org/sparql",
    standard="rdf"
)


def get_response_from_neo4j(pregunta):
    try:
        qa_chain = GraphCypherQAChain.from_llm(
            llm=llm,
            graph=graph,
            verbose=True,
            return_intermediate_steps=True,
            allow_dangerous_requests=True
        )

        respuesta = qa_chain.invoke({"query": pregunta})
        
        logger.info("🔍 Respuesta completa de Neo4j QA Chain:")
        logger.info(respuesta)

        # Verificamos si el contexto está vacío
        intermediate_steps = respuesta.get("intermediate_steps", [])
        if intermediate_steps and isinstance(intermediate_steps[1].get("context", None), list):
            if len(intermediate_steps[1]["context"]) == 0:
                logger.info("⚠️ No se encontraron resultados en Neo4j.")
                return None

        return respuesta["result"]

    except Exception as e:
        print(f"❌ Error al consultar Neo4j: {e}")
        return None



def get_response_from_wikidata(pregunta):
    # Obtener la entidad de Wikidata
    messages = [
        SystemMessage(content="""Eres un asistente que ayuda a identificar entidades específicas para ser consultadas en Wikidata. 
        Dada una pregunta del usuario, devuelve el nombre COMPLETO Y EXACTO de la entidad principal a buscar en Wikidata.
        No devuelvas nada ambiguo. No expliques nada. Solo responde con el nombre más apropiado para Wikidata."""),
        HumanMessage(content=pregunta)
    ]

    entidad = llm.invoke(messages).content
    logger.info("Entidad de Wikidata: %s", entidad)

    # Usar Wikidata API para obtener información relevante
    wikidata = WikidataQueryRun(api_wrapper=WikidataAPIWrapper(lang="es"))
    respuesta_raw = wikidata.run(entidad)
    logger.info("Contexto Wikidata: %s", respuesta_raw)

    # Verifica si la respuesta es "No good Wikidata Search Result was found"
    if "No good Wikidata Search Result was found" in respuesta_raw:
        logger.warning("⚠️ No se encontró un buen resultado en Wikidata para la entidad: %s", entidad)
        return None  # Aquí no se retorna respuesta de Wikidata y podemos continuar con DBpedia o Neo4j

    # Usar el LLM para responder de forma natural con el contexto obtenido
    messages_final = [
        SystemMessage(content="""Eres un asistente que responde preguntas de los usuarios utilizando información estructurada de Wikidata. 
        A continuación recibirás una pregunta y un contexto que contiene datos relevantes de Wikidata. 
        Responde de forma natural, clara y directa, utilizando solo la información del contexto. 
        Si no encuentras la respuesta, indícalo."""), 
        HumanMessage(content=f"Pregunta: {pregunta}\n\nContexto:\n{respuesta_raw}")
    ]

    respuesta_final = llm.invoke(messages_final).content

    return respuesta_final

def get_response_from_dbpedia(pregunta):
    logger.info("🌐 [DBpedia] Consultando DBpedia con la pregunta: %s", pregunta)

    # Configurar el grafo RDF y el LLM
    chain = GraphSparqlQAChain.from_llm(
        llm=llm_dbpedia,  # reutiliza el ChatOllama ya instanciado globalmente
        graph=graph_dbpedia,
        allow_dangerous_requests=True,
        return_sparql_query=True,
    )

    # Bloque de namespaces para ayudar al modelo
    query = """
        Associated namespaces:
        dbr:  <http://dbpedia.org/resource/>
        dbo:  <http://dbpedia.org/ontology/>
        rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    """

    # Pregunta del usuario (solo texto, sin necesidad de tocar el código)
    user_question = pregunta

    # Concatenar la ayuda (namespaces) + pregunta del usuario
    full_prompt = f"{query}\n\n{user_question}"

    try:
        result = chain.invoke({"query": full_prompt}, return_only_outputs=False)
        logger.info("Contexto DBpedia: %s", result)
        respuesta = result["result"]
        if not respuesta:
            logger.warning("⚠️ DBpedia no devolvió respuesta útil.")
            return None
        return respuesta

    except ValueError as e:
        logger.error("❌ Error al ejecutar la consulta SPARQL: %s", e)
        return None
        
    except Exception as e:
        logger.exception("❌ Error inesperado al consultar DBpedia")
        return None



def get_response_from_llm(pregunta):
    logger.info("💬 [LLM] Generando respuesta con modelo local como último recurso...")    
    respuesta = llm.invoke(pregunta).content
    advertencia = "⚠️ *Esta respuesta ha sido generada por IA sin apoyo en fuentes verificadas. Considera contrastarla con fuentes oficiales.*\n\n"
    return advertencia + respuesta
