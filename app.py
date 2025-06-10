"""
MPAgent - Marine Protected Area Management Plan Analysis Tool

This module provides a Streamlit web interface for analyzing MPA management plans,
integrating document processing, AI extraction, and analytical modules with a focus
on Spanish language support and robust error handling.
"""

import os
import sys
import json
import time
import streamlit as st
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Import project modules
from extraction_modules import ZonationExtractor, ObjectivesExtractor, LiteratureExtractor, extract_all
from analytical_modules import analyze_all, MPAGuideEvaluator, SMARTCriteriaEvaluator, LiteratureCongruenceAnalyzer

# Configure page
st.set_page_config(
    page_title="MPAgent - Análisis de Planes de Manejo de AMPs",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize session state
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #1f77b4; margin-bottom: 1rem;}
    .section-header {color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 0.3rem; margin-top: 1.5rem;}
    .success-box {background-color: #e8f5e9; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
    .warning-box {background-color: #fff8e1; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
    .error-box {background-color: #ffebee; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
    .metric-card {background-color: #f5f5f5; padding: 1rem; border-radius: 0.5rem; text-align: center;}
    </style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file) -> tuple[bool, str]:
    """Extract text from PDF using PyMuPDF with progress tracking."""
    try:
        # Read the file content first
        file_bytes = pdf_file.getvalue()
        
        # Open the PDF from bytes
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        total_pages = len(doc)
        
        if total_pages == 0:
            return False, "El archivo PDF está vacío."
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, page in enumerate(doc):
            progress = (i + 1) / total_pages
            progress_bar.progress(progress)
            status_text.text(f"Procesando página {i+1} de {total_pages}...")
            full_text += page.get_text("text") + "\n\n"
        
        doc.close()
        progress_bar.empty()
        status_text.empty()
        
        if not full_text.strip():
            return False, "El PDF no contiene texto extraíble."
        
        return True, full_text.strip()
    
    except fitz.FileDataError as e:
        if 'password' in str(e).lower():
            return False, "El PDF está protegido con contraseña."
        return False, "El archivo no es un PDF válido o está dañado."
    except fitz.EmptyFileError:
        return False, "El archivo PDF está vacío."
    except Exception as e:
        return False, f"Error al procesar el PDF: {str(e)}"

def split_text_into_chunks(text, chunk_size=1000):
    """Split text into chunks of approximately chunk_size tokens."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        if current_size + len(word) + 1 > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_size = len(word)
        else:
            current_chunk.append(word)
            current_size += len(word) + 1
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def save_uploaded_file(uploaded_file) -> Optional[Path]:
    """Save uploaded file to temporary location."""
    try:
        temp_dir = Path("./temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        file_path = temp_dir / uploaded_file.name
        file_path.write_bytes(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error al guardar el archivo: {str(e)}")
        return None

def display_zonation_results(data: Dict[str, Any]) -> None:
    """Display zonation and regulations results."""
    if not data or "zonas" not in data or not data["zonas"]:
        st.warning("No se encontró información de zonificación en el documento.")
        return
    
    st.markdown("### 🗺️ Zonificación y Regulaciones")
    for i, zona in enumerate(data["zonas"], 1):
        with st.expander(f"Zona {i}: {zona.get('nombre_zona', 'Sin nombre')}"):
            cols = st.columns(2)
            with cols[0]:
                st.markdown("**Límites:**")
                st.write(zona.get("limites", "No especificado"))
            with cols[1]:
                st.markdown("**Regulaciones:**")
                if "regulaciones" in zona and zona["regulaciones"]:
                    for reg in zona["regulaciones"]:
                        st.write(f"- {reg}")
                else:
                    st.write("No se especificaron regulaciones.")

def display_objectives_results(objectives_data: Dict[str, Any], smart_results: Dict[str, Any]) -> None:
    """Display conservation objectives and SMART analysis."""
    if not objectives_data or "objetivos_conservacion" not in objectives_data or not objectives_data["objetivos_conservacion"]:
        st.warning("No se encontraron objetivos de conservación en el documento.")
        return
    
    st.markdown("### 🎯 Objetivos de Conservación")
    smart_evaluations = {}
    if smart_results and "evaluacion_objetivos" in smart_results:
        smart_evaluations = {obj["objetivo"]: obj for obj in smart_results["evaluacion_objetivos"]}
    
    for i, objetivo in enumerate(objectives_data["objetivos_conservacion"], 1):
        with st.expander(f"Objetivo {i}"):
            st.markdown(f"**{objetivo}**")
            
            if objetivo in smart_evaluations:
                smart = smart_evaluations[objetivo]["SMART"]
                score = smart_evaluations[objetivo]["puntuacion_SMART"]
                
                # Display SMART score with color coding
                score_color = "green" if score >= 4 else "orange" if score >= 2 else "red"
                st.markdown(f"**Puntuación SMART:** :{score_color}[{score}/5]")
                
                # Display SMART criteria
                cols = st.columns(5)
                criteria = ["Específico", "Medible", "Alcanzable", "Relevante", "Con Plazo"]
                for i, crit in enumerate(criteria):
                    value = smart.get(crit.lower().replace(" ", "_"), False)
                    cols[i].metric(crit, "✅" if value else "❌")
                
                # Display viability assessment
                st.markdown("**Evaluación de viabilidad:**")
                st.info(smart_evaluations[objetivo]["viabilidad"])

def display_literature_results(literature_data: Dict[str, Any], congruence_results: Dict[str, Any]) -> None:
    """Display literature citations and congruence analysis."""
    if not literature_data or "referencias" not in literature_data or not literature_data["referencias"]:
        st.warning("No se encontraron referencias bibliográficas en el documento.")
        return
    
    st.markdown("### 📚 Referencias Bibliográficas")
    
    # Display literature references
    with st.expander("Ver todas las referencias"):
        for i, ref in enumerate(literature_data["referencias"], 1):
            st.markdown(f"{i}. {ref}")
    
    # Display congruence analysis if available
    if congruence_results and "congruencia_tematica" in congruence_results:
        st.markdown("#### 🔍 Análisis de Congruencia Temática")
        for item in congruence_results["congruencia_tematica"]:
            with st.expander(f"Análisis: {item['objetivo'][:50]}..."):
                st.markdown(f"**Objetivo:** {item['objetivo']}")
                st.markdown(f"**Respaldado por literatura:** {'✅ Sí' if item['respaldado_por_literatura'] else '❌ No'}")
                
                if item["referencias_relacionadas"]:
                    st.markdown("**Referencias relacionadas:**")
                    for ref in item["referencias_relacionadas"]:
                        st.write(f"- {ref}")
                
                if "comentarios" in item:
                    st.markdown("**Comentarios:**")
                    st.info(item["comentarios"])
        
        if "brechas_tematicas_generales" in congruence_results and congruence_results["brechas_tematicas_generales"]:
            st.markdown("#### ⚠️ Brechas Temáticas Identificadas")
            for brecha in congruence_results["brechas_tematicas_generales"]:
                st.warning(f"- {brecha}")

def display_mpa_guide_results(mpa_results: Dict[str, Any]) -> None:
    """Display MPA Guide evaluation results."""
    if not mpa_results or "evaluacion_zonas" not in mpa_results or not mpa_results["evaluacion_zonas"]:
        st.warning("No se pudo realizar la evaluación MPA Guide.")
        return
    
    st.markdown("### 📊 Evaluación MPA Guide")
    
    # Display overall assessment
    zonas_evaluadas = len(mpa_results["evaluacion_zonas"])
    categorias = [z["categoria_MPA_guide"] for z in mpa_results["evaluacion_zonas"] if "categoria_MPA_guide" in z]
    if categorias:
        st.metric("Categoría de protección predominante", max(set(categorias), key=categorias.count))
    
    # Display evaluation per zone
    for zona in mpa_results["evaluacion_zonas"]:
        with st.expander(f"Evaluación: {zona.get('nombre_zona', 'Zona sin nombre')}"):
            st.markdown(f"**Categoría MPA Guide:** **{zona.get('categoria_MPA_guide', 'No determinado')}**")
            if "justificacion" in zona:
                st.markdown("**Justificación:**")
                st.info(zona["justificacion"])

def main():
    """Main application function."""
    # Sidebar with app info and controls
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=MPAgent", width=150)
        st.title("MPAgent")
        st.markdown("""
        Herramienta de análisis de Planes de Manejo de Áreas Marinas Protegidas.
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Estado del Análisis")
        if st.session_state.extracted_data:
            st.success("✅ Datos extraídos")
        else:
            st.warning("⏳ Esperando datos")
            
        if st.session_state.analysis_results:
            st.success("✅ Análisis completado")
        else:
            st.warning("⏳ Análisis pendiente")
        
        # Sidebar for configuration
        st.markdown("---")
        st.markdown("### ⚙️ Configuración")
        model_name = st.selectbox(
            "Modelo de IA",
            ["gpt-3.5-turbo", "gpt-4"],
            index=0,
            help="Selecciona el modelo de IA a utilizar. GPT-4 es más preciso pero más lento y costoso."
        )
        chunk_size = st.slider(
            "Tamaño de fragmentos de texto",
            min_value=500,
            max_value=2000,
            value=1000,
            step=100,
            help="Tamaño de los fragmentos de texto para procesar (en tokens)"
        )
        
        if st.button("🔄 Reiniciar Análisis"):
            st.session_state.extracted_data = None
            st.session_state.analysis_results = None
            st.experimental_rerun()
            
        st.markdown("---")
        st.markdown("### 📝 Acerca de")
        st.markdown("""
        **MPAgent** es una herramienta para analizar Planes de Manejo de Áreas Marinas Protegidas.
        """)
        st.markdown("Versión: 1.0.0")

    # Main content area
    st.markdown('<h1 class="main-header">🌊 MPAgent - Análisis de Planes de Manejo</h1>', unsafe_allow_html=True)
    
    # File upload section
    st.markdown("## 1️⃣ Cargar Documento")
    uploaded_file = st.file_uploader(
        "Sube el Plan de Manejo en formato PDF",
        type=["pdf"],
        help="Selecciona un archivo PDF para analizar."
    )
    
    # Process uploaded file
    if uploaded_file and st.button("🔍 Iniciar Análisis", type="primary"):
        with st.spinner("Procesando documento..."):
            # Save the uploaded file
            file_path = save_uploaded_file(uploaded_file)
            if not file_path:
                st.error("Error al guardar el archivo.")
                return
            
            # Extract text from PDF
            success, text = extract_text_from_pdf(uploaded_file)
            if not success:
                st.error(f"Error al extraer texto: {text}")
                return
            
            # Split the text into chunks
            text_chunks = split_text_into_chunks(text, chunk_size=chunk_size)
            st.session_state.text_chunks = text_chunks
            st.session_state.current_chunk = 0
            st.session_state.extracted_text = ""
            st.session_state.processing_complete = False
            st.success(f"Texto extraído exitosamente! Dividido en {len(text_chunks)} fragmentos.")
            
            # Process text chunks one by one
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Initialize extracted data
                st.session_state.extracted_data = {"text": text}
                
                # Initialize extraction results
                extraction_results = {
                    "zonation": {"zonas": []},
                    "objectives": {"objetivos_conservacion": []},
                    "literature": {"referencias_bibliograficas": []}
                }
                
                # Process each chunk
                for i, chunk in enumerate(text_chunks):
                    status_text.text(f"Procesando fragmento {i+1} de {len(text_chunks)}...")
                    
                    try:
                        # Process the current chunk
                        chunk_results = extract_all(chunk, model_name=model_name)
                        
                        # Merge results, avoiding duplicates
                        if "zonation" in chunk_results and "zonas" in chunk_results["zonation"]:
                            extraction_results["zonation"]["zonas"].extend(
                                zone for zone in chunk_results["zonation"]["zonas"] 
                                if zone not in extraction_results["zonation"]["zonas"]
                            )
                            
                        if "objectives" in chunk_results and "objetivos_conservacion" in chunk_results["objectives"]:
                            extraction_results["objectives"]["objetivos_conservacion"].extend(
                                obj for obj in chunk_results["objectives"]["objetivos_conservacion"]
                                if obj not in extraction_results["objectives"]["objetivos_conservacion"]
                            )
                            
                        if "literature" in chunk_results and "referencias_bibliograficas" in chunk_results["literature"]:
                            extraction_results["literature"]["referencias_bibliograficas"].extend(
                                ref for ref in chunk_results["literature"]["referencias_bibliograficas"]
                                if ref not in extraction_results["literature"]["referencias_bibliograficas"]
                            )
                            
                    except Exception as e:
                        st.warning(f"Advertencia en el fragmento {i+1}: {str(e)}")
                        continue
                    
                    # Update progress
                    progress = (i + 1) / len(text_chunks)
                    progress_bar.progress(progress)
                
                # Store the combined results
                st.session_state.extracted_data.update(extraction_results)
                
                st.success("✅ Extracción de información completada")
                
            except Exception as e:
                st.error(f"Error durante la extracción: {str(e)}")
                st.stop()
            
            # Run analysis modules
            with st.spinner("Analizando datos..."):
                try:
                    analysis_results = analyze_all(
                        extraction_results.get("zonation", {}),
                        extraction_results.get("objectives", {}),
                        extraction_results.get("literature", {}),
                        model_name=model_name
                    )
                    st.session_state.analysis_results = analysis_results
                    st.success("✅ Análisis completado")
                except Exception as e:
                    st.error(f"Error durante el análisis: {str(e)}")
                    st.stop()
            
            st.balloons()
            st.experimental_rerun()
    
    # Display results if available
    if st.session_state.extracted_data:
        st.markdown("## 📋 Resultados del Análisis")
        
        # Display extracted text preview
        with st.expander("📄 Ver texto extraído"):
            st.text_area("Texto extraído (vista previa)", 
                        value=st.session_state.extracted_data["text"][:2000] + "...", 
                        height=300)
        
        # Display analysis results
        if st.session_state.analysis_results:
            tab1, tab2, tab3, tab4 = st.tabs([
                "🗺️ Zonificación", 
                "🎯 Objetivos", 
                "📚 Literatura", 
                "📊 MPA Guide"
            ])
            
            with tab1:
                display_zonation_results(st.session_state.extracted_data.get("zonation", {}))
                
            with tab2:
                display_objectives_results(
                    st.session_state.extracted_data.get("objectives", {}),
                    st.session_state.analysis_results.get("smart_analysis", {})
                )
                
            with tab3:
                display_literature_results(
                    st.session_state.extracted_data.get("literature", {}),
                    st.session_state.analysis_results.get("congruence_analysis", {})
                )
                
            with tab4:
                display_mpa_guide_results(
                    st.session_state.analysis_results.get("mpa_guide_evaluation", {})
                )
            
            # Add download button for full report
            st.download_button(
                label="📥 Descargar Informe Completo",
                data=json.dumps({
                    "extracted_data": st.session_state.extracted_data,
                    "analysis_results": st.session_state.analysis_results
                }, indent=2, ensure_ascii=False),
                file_name="informe_analisis_mpa.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
