import logging
import pandas as pd
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain.chat_models import ChatOpenAI

# Configurar logging
logging.basicConfig(
    level=logging.INFO,  # Cambia a DEBUG si quieres más detalle
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("Leyendo el CSV de universidades...")
try:
    df = pd.read_csv("/app/import/train_descriptions.csv", delimiter=',')
except FileNotFoundError:
    logger.error("Archivo CSV no encontrado en /app/import/universidades_europa.csv")
    raise

descriptions = df['descripcion_ingles'].dropna().tolist()
logger.info(f"Total de descripciones encontradas: {len(descriptions)}")

logger.info("Inicializando el modelo LLM y el transformador de grafo...")
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0, max_tokens=None, timeout=None, max_retries=2, base_url="https://openrouter.ai/api/v1",  api_key="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")
llm_transformer = LLMGraphTransformer(llm=llm)

logger.info("Creando documentos a partir de las descripciones...")
documents = [Document(page_content=text) for text in descriptions]
logger.debug(f"Ejemplo de documento: {documents[0].page_content[:200]}...")

logger.info("Transformando documentos en documentos de grafo...")
graph_documents = llm_transformer.convert_to_graph_documents(documents)
logger.info(f"Documentos de grafo generados: {len(graph_documents)}")

logger.debug("Ejemplo de documento de grafo:")
logger.debug(graph_documents[0])

logger.info("Conectando con Neo4j...")
graph = Neo4jGraph(
    url="bolt://neo4j:7687",
    username="neo4j",
    password="password"
)

logger.info("Cargando documentos en el grafo...")
graph.add_graph_documents(graph_documents)
logger.info("Datos cargados en Neo4j correctamente.")
