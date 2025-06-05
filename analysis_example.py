"""
MPAgent Analysis Example

This script demonstrates how to use the extraction and analytical modules for
Marine Protected Area Management Plans analysis.

This integrates components from Phase 2 (AI Extraction Modules) and 
Phase 3 (Analytical Modules) of the MPAgent project.
"""

import os
import json
import streamlit as st
from extraction_modules import ZonationExtractor, ObjectivesExtractor, LiteratureExtractor
from analytical_modules import MPAGuideEvaluator, SMARTCriteriaEvaluator, LiteratureCongruenceAnalyzer
from dotenv import load_dotenv

# Load environment variables (OpenAI API key)
load_dotenv()

# Sample function to demonstrate the workflow
def analyze_mpa_document(text):
    """
    Process and analyze MPA management plan text.
    
    Args:
        text: The extracted text from the MPA management plan PDF
        
    Returns:
        Dictionary containing extraction and analysis results
    """
    st.header("Proceso de Análisis")
    
    # Step 1: Extract data
    with st.spinner("Extrayendo información del plan de manejo..."):
        st.subheader("1. Extracción de Datos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.spinner("Extrayendo zonas y regulaciones..."):
                zonation_extractor = ZonationExtractor()
                zonation_data = zonation_extractor.extract(text)
                st.success("✅ Zonas y regulaciones extraídas")
        
        with col2:
            with st.spinner("Extrayendo objetivos de conservación..."):
                objectives_extractor = ObjectivesExtractor()
                objectives_data = objectives_extractor.extract(text)
                st.success("✅ Objetivos de conservación extraídos")
        
        with col3:
            with st.spinner("Extrayendo referencias bibliográficas..."):
                literature_extractor = LiteratureExtractor()
                literature_data = literature_extractor.extract(text)
                st.success("✅ Referencias bibliográficas extraídas")
    
    # Step 2: Analyze the extracted data
    with st.spinner("Realizando análisis avanzado..."):
        st.subheader("2. Análisis Avanzado")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.spinner("Evaluando marco MPA Guide..."):
                mpa_evaluator = MPAGuideEvaluator()
                mpa_results = mpa_evaluator.evaluate(zonation_data)
                st.success("✅ Evaluación MPA Guide completada")
            
            with st.spinner("Evaluando criterios SMART..."):
                smart_evaluator = SMARTCriteriaEvaluator()
                smart_results = smart_evaluator.evaluate(objectives_data)
                st.success("✅ Evaluación SMART completada")
        
        with col2:
            with st.spinner("Analizando congruencia con literatura..."):
                congruence_analyzer = LiteratureCongruenceAnalyzer()
                congruence_results = congruence_analyzer.analyze(objectives_data, literature_data)
                st.success("✅ Análisis de congruencia completado")
    
    # Combine all results
    all_results = {
        "extraction": {
            "zonation": zonation_data,
            "objectives": objectives_data,
            "literature": literature_data
        },
        "analysis": {
            "mpa_guide": mpa_results,
            "smart": smart_results,
            "congruence": congruence_results
        }
    }
    
    # Display results
    st.header("3. Resultados del Análisis")
    
    # MPA Guide results
    st.subheader("Evaluación MPA Guide")
    if "evaluacion_zonas" in mpa_results and mpa_results["evaluacion_zonas"]:
        for zone in mpa_results["evaluacion_zonas"]:
            st.write(f"**Zona:** {zone['nombre_zona']}")
            st.write(f"**Categoría:** {zone['categoria_MPA_guide']}")
            st.write(f"**Justificación:** {zone['justificacion']}")
            st.write("---")
    else:
        st.write("No se pudo realizar la evaluación MPA Guide.")
    
    # SMART Criteria results
    st.subheader("Evaluación SMART")
    if "evaluacion_objetivos" in smart_results and smart_results["evaluacion_objetivos"]:
        for obj in smart_results["evaluacion_objetivos"]:
            st.write(f"**Objetivo:** {obj['objetivo']}")
            
            # Display SMART criteria as colored indicators
            cols = st.columns(5)
            criteria = obj["SMART"]
            with cols[0]:
                st.write("Específico: " + ("✅" if criteria["Especifico"] else "❌"))
            with cols[1]:
                st.write("Medible: " + ("✅" if criteria["Medible"] else "❌"))
            with cols[2]:
                st.write("Alcanzable: " + ("✅" if criteria["Alcanzable"] else "❌"))
            with cols[3]:
                st.write("Relevante: " + ("✅" if criteria["Relevante"] else "❌"))
            with cols[4]:
                st.write("Con Plazo: " + ("✅" if criteria["Con_plazo"] else "❌"))
            
            # Puntuación y viabilidad
            if "puntuacion_SMART" in obj:
                st.write(f"**Puntuación SMART:** {obj['puntuacion_SMART']}/5")
            st.write(f"**Viabilidad:** {obj['viabilidad']}")
            st.write("---")
    else:
        st.write("No se pudo realizar la evaluación SMART.")
    
    # Literature Congruence results
    st.subheader("Análisis de Congruencia con Literatura")
    if "congruencia_tematica" in congruence_results and congruence_results["congruencia_tematica"]:
        for item in congruence_results["congruencia_tematica"]:
            st.write(f"**Objetivo:** {item['objetivo']}")
            st.write(f"**Respaldado por literatura:** " + ("✅ Sí" if item['respaldado_por_literatura'] else "❌ No"))
            
            if item['temas_relacionados_literatura']:
                st.write("**Temas relacionados:**")
                for tema in item['temas_relacionados_literatura']:
                    st.write(f"- {tema}")
            
            if "referencias_relacionadas" in item and item['referencias_relacionadas']:
                st.write("**Referencias relacionadas:**")
                for ref in item['referencias_relacionadas']:
                    st.write(f"- {ref}")
            
            st.write(f"**Comentarios:** {item['comentarios']}")
            st.write("---")
        
        if "brechas_tematicas_generales" in congruence_results and congruence_results["brechas_tematicas_generales"]:
            st.subheader("Brechas Temáticas Generales")
            for brecha in congruence_results["brechas_tematicas_generales"]:
                st.write(f"- {brecha}")
    else:
        st.write("No se pudo realizar el análisis de congruencia con literatura.")
    
    # Provide download options for results
    st.header("4. Descargar Resultados")
    json_results = json.dumps(all_results, ensure_ascii=False, indent=2)
    st.download_button(
        label="Descargar Análisis Completo (JSON)",
        data=json_results.encode("utf-8"),
        file_name="analisis_completo.json",
        mime="application/json"
    )
    
    return all_results


# Example of how to use in a Streamlit app
def main():
    st.title("Ejemplo de Análisis de Plan de Manejo de AMP")
    
    # This would normally come from the PDF extraction step
    sample_text = """
    Este es un ejemplo de texto extraído de un Plan de Manejo de un Área Marina Protegida.
    
    ZONIFICACIÓN:
    
    Zona Núcleo:
    Límites: Desde la coordenada 18°32'14"N, 95°03'45"W hasta la coordenada 18°30'22"N, 95°02'11"W.
    Regulaciones:
    - Prohibida toda actividad extractiva
    - Prohibido el acceso sin permiso científico
    - No se permite el tránsito de embarcaciones motorizadas
    
    Zona de Amortiguamiento:
    Límites: Radio de 5km alrededor de la Zona Núcleo.
    Regulaciones:
    - Se permite pesca artesanal con artes específicas
    - Prohibida la pesca industrial
    - Se permite turismo regulado de bajo impacto
    
    OBJETIVOS DE CONSERVACIÓN:
    
    1. Proteger el 100% de los arrecifes de coral dentro del área para 2030
    2. Aumentar la biomasa de especies comerciales en un 30% en 5 años
    3. Mantener la calidad del agua dentro de los estándares internacionales
    4. Implementar un programa de educación ambiental para comunidades locales
    5. Desarrollar investigación científica continua sobre biodiversidad marina
    
    REFERENCIAS BIBLIOGRÁFICAS:
    
    García, M. y Rodríguez, J. (2020). Estado de conservación de arrecifes coralinos en la región sur del Pacífico mexicano. Revista de Biología Marina, 32(2), 45-58.
    
    López, A. (2019). Efectividad de las áreas marinas protegidas: un análisis comparativo. Editorial Océano, Ciudad de México.
    
    Smith, J., Brown, T., & García, M. (2018). Conservation strategies for coral reef ecosystems. Marine Conservation, 12(3), 211-225.
    
    Pérez, R., González, S. y Martínez, B. (2021). Impacto socioeconómico de las restricciones pesqueras en comunidades costeras. Estudios Económicos Pesqueros, 8(1), 78-92.
    """
    
    # Option to use the sample text or enter new text
    use_sample = st.checkbox("Usar texto de ejemplo", value=True)
    
    if use_sample:
        input_text = sample_text
    else:
        input_text = st.text_area("Introducir texto del Plan de Manejo:", height=300)
    
    if st.button("Iniciar Análisis") and input_text:
        # Run the analysis
        analyze_mpa_document(input_text)


if __name__ == "__main__":
    main()
