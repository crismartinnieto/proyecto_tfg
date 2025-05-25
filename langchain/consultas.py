from langchain_ollama import ChatOllama
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun
from langchain_ollama import ChatOllama
from langchain_community.graphs import RdfGraph
from langchain.chains import GraphSparqlQAChain
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# Configura la API de Ollama
llm = ChatOllama(model="phi4", base_url="http://192.168.1.180:11434")

# Conexión a Neo4j a través de LangChain
graph = Neo4jGraph(
    url="bolt://neo4j:7687",
    username="neo4j",
    password="password"
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
    # Placeholder fake response
    return "Esta es una respuesta ficticia desde DBpedia (placeholder)."


def get_response_from_llm(pregunta):
    logger.info("💬 [LLM] Generando respuesta con modelo local como último recurso...")    
    respuesta = llm.invoke(pregunta).content
    advertencia = "⚠️ *Esta respuesta ha sido generada por IA sin apoyo en fuentes verificadas. Considera contrastarla con fuentes oficiales.*\n\n"
    return advertencia + respuesta
