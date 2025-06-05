"""
MPAgent Analytical Assessment Modules

This module provides specialized GPT-based analytical assessments for Marine Protected Area Management Plans:
1. MPA Guide Framework Evaluation
2. SMART Criteria & Feasibility Analysis
3. Literature-Objective Congruence Analysis

This is part of Phase 3 (Analytical Modules) of the MPAgent project.
"""

import os
import json
from typing import Dict, List, Any, Optional, Union
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables (OpenAI API key)
load_dotenv()

# Get default model from environment or use GPT-4
default_model = os.getenv("DEFAULT_MODEL", "gpt-4")


class MPAGuideEvaluator:
    """
    Evaluates the protection quality of MPA zones using the MPA Guide framework.
    
    Categories:
    - Fully Protected
    - Highly Protected
    - Lightly Protected
    - Minimally Protected
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the MPA Guide evaluator.
        
        Args:
            model_name: OpenAI model name to use (defaults to environment setting or gpt-4)
        """
        self.model_name = model_name or default_model
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        
        # Define the prompt template for MPA Guide evaluation
        self.mpa_guide_template = """
        Evalúa las regulaciones extraídas para cada zona utilizando el marco del MPA Guide.

        El marco del MPA Guide establece cuatro categorías de protección:

        1. Totalmente Protegida:
           - No se permite ninguna actividad extractiva o destructiva
           - Se prohíbe la pesca, la minería, el dragado
           - No se permite modificación del hábitat

        2. Altamente Protegida:
           - Se permiten actividades extractivas muy limitadas (subsistencia o ceremonial)
           - Impacto mínimo y localizado
           - Mantiene ecosistemas naturales

        3. Poco Protegida:
           - Se permite pesca comercial o recreativa con algunas restricciones
           - Actividades extractivas moderadas permitidas
           - Se regulan algunas actividades con impacto

        4. Mínimamente Protegida:
           - Muchas actividades extractivas permitidas
           - Pocas restricciones específicas
           - Enfoque en manejo pesquero más que en conservación completa

        Instrucciones:
        1. Para cada zona, evalúa detenidamente sus regulaciones
        2. Asigna la categoría MPA Guide más apropiada
        3. Proporciona una justificación clara basada en las regulaciones específicas
        4. Si hay información insuficiente para evaluar una zona, indica "No determinado"
        5. Utiliza exactamente la estructura JSON solicitada

        Proporciona la respuesta en JSON indicando claramente la categoría asignada y una breve justificación:
        {{
          "evaluacion_zonas": [
            {{
              "nombre_zona": "...",
              "categoria_MPA_guide": "...",
              "justificacion": "..."
            }},
            ...
          ]
        }}

        Si no hay información suficiente para realizar la evaluación, devuelve:
        {{
          "evaluacion_zonas": [],
          "mensaje": "Información insuficiente para realizar la evaluación MPA Guide"
        }}

        Zonas y regulaciones:
        {zonation_data}
        
        JSON:
        """
        
        self.prompt = PromptTemplate(
            template=self.mpa_guide_template,
            input_variables=["zonation_data"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, output_key="json_result")
    
    def evaluate(self, zonation_data: Dict) -> Dict:
        """
        Evaluate zonation using the MPA Guide framework.
        
        Args:
            zonation_data: Dictionary containing zonation information
            
        Returns:
            Dictionary containing the MPA Guide evaluation results
        """
        try:
            # Convert dictionary to string for the prompt
            zonation_str = json.dumps(zonation_data, ensure_ascii=False, indent=2)
            
            # Get evaluation
            json_str = self.chain.run(zonation_data=zonation_str)
            
            # Parse JSON and handle potential errors
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            # Handle error if output isn't valid JSON
            return {"evaluacion_zonas": [], "error": "Error al procesar la respuesta JSON"}
        except Exception as e:
            return {"evaluacion_zonas": [], "error": f"Error durante la evaluación: {str(e)}"}


class SMARTCriteriaEvaluator:
    """
    Evaluates conservation objectives using SMART criteria and performs feasibility analysis.
    
    SMART:
    - Specific (Específico)
    - Measurable (Medible)
    - Achievable (Alcanzable)
    - Relevant (Relevante)
    - Time-bound (Con Plazo definido)
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the SMART criteria evaluator.
        
        Args:
            model_name: OpenAI model name to use (defaults to environment setting or gpt-4)
        """
        self.model_name = model_name or default_model
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        
        # Define the prompt template for SMART criteria evaluation
        self.smart_template = """
        Evalúa cada objetivo de conservación extraído según los criterios SMART e indica su viabilidad práctica.

        Los criterios SMART son:
        - Específico: El objetivo describe claramente y concretamente lo que se quiere lograr.
        - Medible: Es posible cuantificar o medir el progreso hacia el cumplimiento del objetivo.
        - Alcanzable: El objetivo es realista y posible de lograr con los recursos disponibles.
        - Relevante: El objetivo está alineado con las necesidades de conservación del área marina protegida.
        - Con plazo: El objetivo establece un marco temporal claro para su cumplimiento.

        Instrucciones:
        1. Evalúa cada objetivo según cada criterio SMART con "true" o "false"
        2. Proporciona una breve evaluación sobre la viabilidad práctica del objetivo
        3. Considera aspectos como recursos necesarios, capacidades técnicas, contexto socioeconómico
        4. Si hay información insuficiente para evaluar algún aspecto, explicalo en la sección de viabilidad
        5. Utiliza exactamente la estructura JSON solicitada

        Presenta la respuesta estructurada en formato JSON:
        {{
          "evaluacion_objetivos": [
            {{
              "objetivo": "...",
              "SMART": {{
                "Especifico": true/false,
                "Medible": true/false,
                "Alcanzable": true/false,
                "Relevante": true/false,
                "Con_plazo": true/false
              }},
              "puntuacion_SMART": 0-5,
              "viabilidad": "breve evaluación sobre su implementación práctica"
            }},
            ...
          ]
        }}
        
        Si no hay objetivos para evaluar, devuelve:
        {{
          "evaluacion_objetivos": [],
          "mensaje": "No se encontraron objetivos para evaluar"
        }}

        Objetivos:
        {objectives_data}
        
        JSON:
        """
        
        self.prompt = PromptTemplate(
            template=self.smart_template,
            input_variables=["objectives_data"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, output_key="json_result")
    
    def evaluate(self, objectives_data: Dict) -> Dict:
        """
        Evaluate conservation objectives using SMART criteria.
        
        Args:
            objectives_data: Dictionary containing conservation objectives
            
        Returns:
            Dictionary containing the SMART evaluation results
        """
        try:
            # Convert dictionary to string for the prompt
            objectives_str = json.dumps(objectives_data, ensure_ascii=False, indent=2)
            
            # Get evaluation
            json_str = self.chain.run(objectives_data=objectives_str)
            
            # Parse JSON and handle potential errors
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            # Handle error if output isn't valid JSON
            return {"evaluacion_objetivos": [], "error": "Error al procesar la respuesta JSON"}
        except Exception as e:
            return {"evaluacion_objetivos": [], "error": f"Error durante la evaluación: {str(e)}"}


class LiteratureCongruenceAnalyzer:
    """
    Analyzes thematic congruence between conservation objectives and cited literature.
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the literature congruence analyzer.
        
        Args:
            model_name: OpenAI model name to use (defaults to environment setting or gpt-4)
        """
        self.model_name = model_name or default_model
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        
        # Define the prompt template for literature congruence analysis
        self.congruence_template = """
        Compara los objetivos de conservación con los temas principales identificados en las referencias bibliográficas extraídas.

        Instrucciones:
        1. Identifica los temas principales abordados en cada referencia bibliográfica
        2. Determina si cada objetivo de conservación está respaldado por literatura pertinente
        3. Indica claramente los objetivos que carecen de respaldo en la literatura proporcionada
        4. Identifica posibles brechas temáticas en la literatura citada
        5. Para cada objetivo, lista las referencias bibliográficas relacionadas (si las hay)
        6. Proporciona un breve comentario explicando la congruencia o las carencias para cada objetivo
        7. Utiliza exactamente la estructura JSON solicitada

        Presenta la respuesta en formato JSON:
        {{
          "congruencia_tematica": [
            {{
              "objetivo": "...",
              "respaldado_por_literatura": true/false,
              "temas_relacionados_literatura": ["...", "..."],
              "referencias_relacionadas": ["referencia 1", "referencia 2"],
              "comentarios": "breve explicación sobre congruencia o carencias identificadas"
            }},
            ...
          ],
          "brechas_tematicas_generales": [
            "tema 1 faltante en la literatura",
            "tema 2 faltante en la literatura"
          ]
        }}

        Si no hay suficiente información para realizar el análisis, devuelve:
        {{
          "congruencia_tematica": [],
          "mensaje": "Información insuficiente para realizar el análisis de congruencia"
        }}

        Objetivos y Literatura:
        {combined_data}
        
        JSON:
        """
        
        self.prompt = PromptTemplate(
            template=self.congruence_template,
            input_variables=["combined_data"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, output_key="json_result")
    
    def analyze(self, objectives_data: Dict, literature_data: Dict) -> Dict:
        """
        Analyze congruence between conservation objectives and literature.
        
        Args:
            objectives_data: Dictionary containing conservation objectives
            literature_data: Dictionary containing literature citations
            
        Returns:
            Dictionary containing the congruence analysis results
        """
        try:
            # Combine the data
            combined_data = {
                "objetivos": objectives_data,
                "literatura": literature_data
            }
            
            # Convert combined dictionary to string for the prompt
            combined_str = json.dumps(combined_data, ensure_ascii=False, indent=2)
            
            # Get analysis
            json_str = self.chain.run(combined_data=combined_str)
            
            # Parse JSON and handle potential errors
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            # Handle error if output isn't valid JSON
            return {"congruencia_tematica": [], "error": "Error al procesar la respuesta JSON"}
        except Exception as e:
            return {"congruencia_tematica": [], "error": f"Error durante el análisis: {str(e)}"}


def analyze_all(zonation_data: Dict, objectives_data: Dict, literature_data: Dict, model_name: str = None) -> Dict:
    """
    Run all analytical assessments.
    
    Args:
        zonation_data: Dictionary containing zonation information
        objectives_data: Dictionary containing conservation objectives
        literature_data: Dictionary containing literature citations
        model_name: OpenAI model name to use
        
    Returns:
        Dictionary containing all analytical results
    """
    mpa_evaluator = MPAGuideEvaluator(model_name)
    smart_evaluator = SMARTCriteriaEvaluator(model_name)
    congruence_analyzer = LiteratureCongruenceAnalyzer(model_name)
    
    # Run all analyses
    mpa_results = mpa_evaluator.evaluate(zonation_data)
    smart_results = smart_evaluator.evaluate(objectives_data)
    congruence_results = congruence_analyzer.analyze(objectives_data, literature_data)
    
    # Combine results
    return {
        "mpa_guide_evaluation": mpa_results,
        "smart_criteria_evaluation": smart_results,
        "literature_congruence_analysis": congruence_results
    }
