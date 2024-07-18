import os
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

HOSPITAL_QA_MODEL = os.getenv("HOSPITAL_QA_MODEL")
HOSPITAL_CYPHER_MODEL = os.getenv("HOSPITAL_CYPHER_MODEL")

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

graph.refresh_schema()

cypher_generation_template = """
Task:
Generate Cypher query for a Neo4j graph database. 

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
Do not include any explanations or apologizes in your responses. 
Do not respond to any questions that might ask anything other than for you to construct
a Cypher statement. Do not include any text except the generated Cypher statement. Make sure the
direction of the relationship is correct in your queries. Make sure you alias both entities and relationships
properly. Do not run any queries that would add to or delete from the database. Make sure to alias all statements that
follow as with statement (e.g. WITH v as visit, c.billing_amount as billing_amount). If
you need to divide numbers, make sure to filter the denominator to be non zero. 

Examples:
# Who is the oldest patient and how old are they?
MATCH (p:Patient)
RETURN p.name AS oldest_patient,
        duration.between

"""