"""
MPAgent Extraction Modules

This module provides specialized GPT-based extractors for Marine Protected Area Management Plans in Spanish.
It includes:
1. Zonation and Regulations Extractor
2. Conservation Objectives Extractor 
3. Literature Citation Extractor

This is part of Phase 2 (AI Extraction Modules) of the MPAgent project.
"""

import os
import json
import openai
from typing import Dict, List, Any, Optional, Union
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import PromptValue
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables (OpenAI API key)
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
default_model = os.getenv("DEFAULT_MODEL", "gpt-4")

class ZonationExtractor:
    """Extracts zonation details and regulations from MPA management plan text."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the zonation extractor.
        
        Args:
            model_name: OpenAI model name to use (defaults to environment setting or gpt-4)
        """
        self.model_name = model_name or default_model
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        
        # Define the prompt template for zonation extraction
        self.zonation_template = """
        A continuación tienes un texto extraído de un Plan de Manejo de un Área Marina Protegida. 
        Extrae claramente la información sobre las zonas del área protegida, incluyendo límites y regulaciones específicas asociadas a cada zona. 
        
        Instrucciones específicas:
        1. Identifica todas las zonas mencionadas en el texto (pueden llamarse "zonas", "sectores", "áreas", etc.)
        2. Para cada zona, extrae sus límites geográficos (pueden ser coordenadas, descripciones de límites, etc.)
        3. Para cada zona, identifica las regulaciones, restricciones o usos permitidos
        4. Si no existe información sobre alguno de estos elementos para una zona, indica "No especificado"
        5. Utiliza exactamente la estructura JSON solicitada
        
        Presenta la respuesta ÚNICAMENTE en formato JSON con la siguiente estructura:
        {{
          "zonas": [
            {{
              "nombre_zona": "...",
              "limites": "...",
              "regulaciones": ["...", "..."]
            }},
            ...
          ]
        }}
        
        Si no hay información sobre zonificación, devuelve:
        {{
          "zonas": []
        }}
        
        Texto del Plan de Manejo:
        {text}
        
        JSON:
        """
        
        self.prompt = PromptTemplate(
            template=self.zonation_template,
            input_variables=["text"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, output_key="json_result")
    
    def extract(self, text: str) -> Dict:
        """
        Extract zonation and regulations from text.
        
        Args:
            text: Spanish text from MPA management plan
            
        Returns:
            Dictionary containing the extracted zones and regulations
        """
        try:
            json_str = self.chain.run(text=text)
            # Parse JSON and handle potential errors
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            # Handle error if output isn't valid JSON
            return {"zonas": [], "error": "Error al procesar la respuesta JSON"}
        except Exception as e:
            return {"zonas": [], "error": f"Error durante la extracción: {str(e)}"}


class ObjectivesExtractor:
    """Extracts conservation objectives from MPA management plan text."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the objectives extractor.
        
        Args:
            model_name: OpenAI model name to use (defaults to environment setting or gpt-4)
        """
        self.model_name = model_name or default_model
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        
        # Define the prompt template for conservation objectives extraction
        self.objectives_template = """
        Extrae del siguiente texto los objetivos de conservación definidos explícitamente en el Plan de Manejo de un Área Marina Protegida.
        
        Instrucciones específicas:
        1. Identifica los objetivos de conservación o manejo principales
        2. Busca secciones tituladas "Objetivos", "Objetivos de conservación", "Objetivos del área", etc.
        3. Incluye tanto objetivos generales como específicos si están presentes
        4. Mantén la redacción original de los objetivos
        5. Si hay objetivos numerados o con viñetas, mantén esa estructura en el listado
        6. No incluyas metas operativas, indicadores o actividades (solo objetivos)
        7. Utiliza exactamente la estructura JSON solicitada
        
        Presenta cada objetivo claramente en formato JSON:
        {{
          "objetivos_conservacion": [
            "objetivo 1",
            "objetivo 2",
            ...
          ]
        }}
        
        Si no se encuentran objetivos explícitos, devuelve:
        {{
          "objetivos_conservacion": []
        }}
        
        Texto:
        {text}
        
        JSON:
        """
        
        self.prompt = PromptTemplate(
            template=self.objectives_template,
            input_variables=["text"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, output_key="json_result")
    
    def extract(self, text: str) -> Dict:
        """
        Extract conservation objectives from text.
        
        Args:
            text: Spanish text from MPA management plan
            
        Returns:
            Dictionary containing the extracted conservation objectives
        """
        try:
            json_str = self.chain.run(text=text)
            # Parse JSON and handle potential errors
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            # Handle error if output isn't valid JSON
            return {"objetivos_conservacion": [], "error": "Error al procesar la respuesta JSON"}
        except Exception as e:
            return {"objetivos_conservacion": [], "error": f"Error durante la extracción: {str(e)}"}


class LiteratureExtractor:
    """Extracts cited literature from MPA management plan text."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the literature extractor.
        
        Args:
            model_name: OpenAI model name to use (defaults to environment setting or gpt-4)
        """
        self.model_name = model_name or default_model
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        
        # Define the prompt template for literature extraction
        self.literature_template = """
        Del texto proporcionado, extrae todas las referencias bibliográficas citadas en un Plan de Manejo de un Área Marina Protegida.
        
        Instrucciones específicas:
        1. Busca secciones tituladas "Referencias", "Bibliografía", "Literatura citada", etc.
        2. Incluye cada referencia bibliográfica completa
        3. Separa los componentes de cada referencia según se solicita en la estructura JSON
        4. Si algún componente no está disponible, indica "No especificado"
        5. Mantén los acentos y caracteres especiales del español correctamente
        6. Utiliza exactamente la estructura JSON solicitada
        
        Estructura los datos claramente en formato JSON:
        {{
          "referencias_bibliograficas": [
            {{
              "autores": "...",
              "titulo": "...",
              "revista_o_fuente": "...",
              "ano_publicacion": "..."
            }},
            ...
          ]
        }}
        
        Si no hay referencias bibliográficas, devuelve:
        {{
          "referencias_bibliograficas": []
        }}
        
        Texto:
        {text}
        
        JSON:
        """
        
        self.prompt = PromptTemplate(
            template=self.literature_template,
            input_variables=["text"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, output_key="json_result")
    
    def extract(self, text: str) -> Dict:
        """
        Extract cited literature from text.
        
        Args:
            text: Spanish text from MPA management plan
            
        Returns:
            Dictionary containing the extracted literature references
        """
        try:
            json_str = self.chain.run(text=text)
            # Parse JSON and handle potential errors
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            # Handle error if output isn't valid JSON
            return {"referencias_bibliograficas": [], "error": "Error al procesar la respuesta JSON"}
        except Exception as e:
            return {"referencias_bibliograficas": [], "error": f"Error durante la extracción: {str(e)}"}


def process_large_text(text: str, max_chunk_size: int = 8000) -> List[str]:
    """
    Split large texts into manageable chunks for API processing.
    
    Args:
        text: Full text to process
        max_chunk_size: Maximum characters per chunk (default 8000)
        
    Returns:
        List of text chunks
    """
    # Simple chunking by character count
    chunks = []
    for i in range(0, len(text), max_chunk_size):
        chunks.append(text[i:i + max_chunk_size])
    return chunks


def extract_all(text: str, model_name: str = None) -> Dict:
    """
    Extract all information types from the text.
    
    Args:
        text: Spanish text from MPA management plan
        model_name: OpenAI model name to use
        
    Returns:
        Dictionary containing all extracted information
    """
    zonation_extractor = ZonationExtractor(model_name)
    objectives_extractor = ObjectivesExtractor(model_name)
    literature_extractor = LiteratureExtractor(model_name)
    
    # For large documents, we might need to process different sections
    # For now, process the whole text for each extractor
    zonation_result = zonation_extractor.extract(text)
    objectives_result = objectives_extractor.extract(text)
    literature_result = literature_extractor.extract(text)
    
    # Combine results
    return {
        "zonation": zonation_result,
        "objectives": objectives_result,
        "literature": literature_result
    }
