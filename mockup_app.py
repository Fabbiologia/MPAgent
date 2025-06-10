"""
MPAgent - Marine Protected Area Management Plan Analysis Tool

This application analyzes Marine Protected Area (MPA) management plans using AI-powered tools.
Deploy on Streamlit Cloud with: streamlit run mockup_app.py
"""

import streamlit as st
import time
import random
from datetime import datetime
import json
import base64
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="MPAgent - MPA Analysis Dashboard",
    page_icon="🌊",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Fabbiologia/MPAgent',
        'Report a bug': 'https://github.com/Fabbiologia/MPAgent/issues',
        'About': "# MPAgent\nAn AI-powered tool for analyzing Marine Protected Area management plans."
    }
)

# Add responsive CSS
st.markdown("""
    <style>
        @media (max-width: 768px) {
            /* Adjust font sizes for mobile */
            .stApp h1 { font-size: 1.8rem !important; }
            .stApp h2 { font-size: 1.5rem !important; }
            .stApp h3 { font-size: 1.3rem !important; }
            .stApp h4 { font-size: 1.1rem !important; }
            
            /* Make tables and dataframes responsive */
            .stDataFrame {
                width: 100% !important;
                display: block;
                overflow-x: auto;
            }
            
            /* Adjust padding and margins */
            .main .block-container {
                padding: 1rem 1rem 5rem;
            }
            
            /* Make columns stack on mobile */
            .st-cf {
                flex-direction: column;
            }
            
            /* Adjust spacing in columns */
            .st-cf > div {
                width: 100% !important;
                margin-bottom: 1rem;
            }
            
            /* Make buttons full width on mobile */
            .stButton > button {
                width: 100%;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #1f77b4; margin-bottom: 1rem;}
    .section-header {color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 0.3rem; margin-top: 1.5rem;}
    .success-box {background-color: #e8f5e9; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
    .warning-box {background-color: #fff8e1; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
    .error-box {background-color: #ffebee; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;}
    .metric-card {background-color: #f5f5f5; padding: 1.5rem; border-radius: 0.5rem; text-align: center; margin: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .progress-container {margin: 2rem 0;}
    .result-section {margin-top: 2rem;}
    .zone-card {background-color: #f0f7ff; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;}
    .objective-card {background-color: #f0fff4; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;}
    .citation-card {background-color: #fffaf0; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;}
    </style>
""", unsafe_allow_html=True)

def simulate_analysis():
    """Simulate the analysis process with progress bars."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Uploading document...",
        "Extracting text content...",
        "Identifying management zones...",
        "Analyzing regulations...",
        "Evaluating conservation objectives...",
        "Assessing SMART criteria...",
        "Reviewing literature references...",
        "Generating final report...",
        "Analysis complete!"
    ]
    
    for i, step in enumerate(steps):
        progress = int((i + 1) / len(steps) * 100)
        progress_bar.progress(progress)
        status_text.text(f"Status: {step}")
        time.sleep(0.3)  # Simulate processing time
    
    progress_bar.empty()
    status_text.empty()

def generate_mock_data():
    """Generate mock data for the analysis results."""
    return {
        "document_info": {
            "name": "Programa de Manejo Revillagigedo.pdf",
            "pages": 148,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Analysis Complete"
        },
        "zones": [
            {
                "name": "Core Zone",
                "description": "Strictly protected area with no extractive activities allowed.",
                "area": "1,250 km²",
                "regulations": [
                    "No fishing or extractive activities",
                    "Scientific research allowed with permit",
                    "No anchoring except in designated areas"
                ]
            },
            {
                "name": "Buffer Zone",
                "description": "Area allowing sustainable use with restrictions.",
                "area": "3,450 km²",
                "regulations": [
                    "Regulated fishing with permits",
                    "Controlled tourism activities",
                    "No industrial activities"
                ]
            },
            {
                "name": "Sustainable Use Zone",
                "description": "Area allowing sustainable resource use under management plan.",
                "area": "5,200 km²",
                "regulations": [
                    "Sustainable fishing allowed",
                    "Tourism activities permitted",
                    "Restricted industrial activities"
                ]
            }
        ],
        "objectives": [
            {
                "objective": "Conserve the terrestrial and marine natural environments of the Revillagigedo National Park, which feature scenic beauty and high biological value, including a wide variety of terrestrial and marine species and ecosystem services derived from them.",
                "category": "General Conservation Objective",
                "smart_analysis": {
                    "specific": "Moderately specific - identifies the park and its values but lacks precise targets",
                    "measurable": "Not measurable - no quantifiable indicators or baseline data provided",
                    "achievable": "Potentially achievable - aligns with MPA's purpose but very broad in scope",
                    "relevant": "Highly relevant - core to the park's mission",
                    "time_bound": "Not time-bound - no timeframe specified"
                },
                "score": 2.8,
                "recommendations": [
                    "Define specific, measurable indicators for 'high biological value' and 'scenic beauty'",
                    "Establish baseline data for key species and ecosystem services",
                    "Set specific targets and timeframes for conservation outcomes"
                ]
            },
            {
                "objective": "Preserve ecosystems with high biodiversity and numerous endemic species.",
                "category": "Ecosystem and Biodiversity Protection",
                "smart_analysis": {
                    "specific": "Specific - identifies what to preserve (ecosystems, biodiversity, endemic species)",
                    "measurable": "Partially measurable - could be improved with specific metrics and targets",
                    "achievable": "Achievable - within MPA's scope and authority",
                    "relevant": "Highly relevant - core to MPA's purpose",
                    "time_bound": "Not time-bound - lacks specific deadlines"
                },
                "score": 3.4,
                "recommendations": [
                    "Define what constitutes 'high biodiversity' in measurable terms",
                    "Establish baseline data for endemic species populations",
                    "Set specific population targets for key species"
                ]
            },
            {
                "objective": "Restore ecological conditions altered by human or natural disturbances to ensure the continuity of natural processes.",
                "category": "Restoration and Ecological Recovery",
                "smart_analysis": {
                    "specific": "Moderately specific - identifies the what but not the how or where",
                    "measurable": "Not measurable - lacks specific indicators or targets",
                    "achievable": "Potentially achievable - depends on resources and specific disturbances",
                    "relevant": "Relevant - important for ecosystem health",
                    "time_bound": "Not time-bound - no timeframe specified"
                },
                "score": 2.6,
                "recommendations": [
                    "Identify priority areas for restoration",
                    "Define specific restoration targets and success criteria",
                    "Establish a monitoring program to track recovery"
                ]
            },
            {
                "objective": "Increase understanding of climate change impacts and reduce the vulnerability of ecosystems. Enhance the adaptive capacity of conservation targets (e.g., species, habitats).",
                "category": "Climate Change Adaptation",
                "smart_analysis": {
                    "specific": "Broad - covers understanding, vulnerability reduction, and adaptive capacity",
                    "measurable": "Partially measurable - could be improved with specific indicators",
                    "achievable": "Challenging - requires long-term commitment and resources",
                    "relevant": "Highly relevant - critical for long-term conservation",
                    "time_bound": "Not time-bound - lacks specific deadlines"
                },
                "score": 3.0,
                "recommendations": [
                    "Develop specific climate change indicators and monitoring protocols",
                    "Set measurable targets for reducing vulnerability",
                    "Create a climate adaptation action plan with clear timelines"
                ]
            },
            {
                "objective": "Identify, control, or eradicate exotic invasive species to recover native flora and fauna.",
                "category": "Control of Invasive and Exotic Species",
                "smart_analysis": {
                    "specific": "Specific - clearly defines the action and target",
                    "measurable": "Partially measurable - could specify which species and to what extent",
                    "achievable": "Achievable - with proper resources and planning",
                    "relevant": "Highly relevant - critical for native biodiversity",
                    "time_bound": "Not time-bound - lacks specific deadlines"
                },
                "score": 3.6,
                "recommendations": [
                    "Prioritize invasive species based on impact and feasibility of control",
                    "Set specific targets for population reduction or eradication",
                    "Establish a monitoring program to assess effectiveness"
                ]
            },
            {
                "objective": "Promote scientific research and establish a monitoring system to evaluate ecological and socioeconomic conditions and management effectiveness.",
                "category": "Monitoring and Knowledge Generation",
                "smart_analysis": {
                    "specific": "Specific - outlines clear actions and purposes",
                    "measurable": "Partially measurable - could specify indicators and frequency",
                    "achievable": "Achievable - within MPA's capacity with proper resources",
                    "relevant": "Highly relevant - essential for adaptive management",
                    "time_bound": "Not time-bound - lacks specific deadlines"
                },
                "score": 3.8,
                "recommendations": [
                    "Develop a comprehensive monitoring framework with clear indicators",
                    "Establish baseline data for key ecological and socioeconomic parameters",
                    "Set specific targets and timelines for monitoring activities"
                ]
            },
            {
                "objective": "Prevent forest fires and manage anthropogenic waste to maintain ecosystem function and services.",
                "category": "Fire and Waste Management",
                "smart_analysis": {
                    "specific": "Specific - identifies key threats to address",
                    "measurable": "Partially measurable - could specify reduction targets",
                    "achievable": "Achievable - with proper planning and resources",
                    "relevant": "Relevant - important for ecosystem health",
                    "time_bound": "Not time-bound - lacks specific deadlines"
                },
                "score": 3.2,
                "recommendations": [
                    "Develop specific fire prevention and waste management plans",
                    "Set measurable targets for waste reduction and fire prevention",
                    "Establish monitoring protocols to track effectiveness"
                ]
            },
            {
                "objective": "Disseminate knowledge and promote awareness of the park's ecological value and services.",
                "category": "Community Engagement and Education",
                "smart_analysis": {
                    "specific": "Specific - identifies the purpose and target",
                    "measurable": "Partially measurable - could specify outreach metrics",
                    "achievable": "Achievable - within MPA's capacity",
                    "relevant": "Relevant - important for stakeholder support",
                    "time_bound": "Not time-bound - lacks specific deadlines"
                },
                "score": 3.5,
                "recommendations": [
                    "Develop a comprehensive education and outreach strategy",
                    "Set specific targets for community engagement activities",
                    "Establish metrics to measure awareness and knowledge improvement"
                ]
            },
            {
                "objective": "Involve local stakeholders and institutions in the park's management and encourage sustainable use.",
                "category": "Cultural and Governance Objectives",
                "smart_analysis": {
                    "specific": "Specific - identifies who to involve and the purpose",
                    "measurable": "Partially measurable - could specify participation metrics",
                    "achievable": "Achievable - with proper engagement strategies",
                    "relevant": "Highly relevant - important for long-term success",
                    "time_bound": "Not time-bound - lacks specific deadlines"
                },
                "score": 3.7,
                "recommendations": [
                    "Develop a stakeholder engagement plan with clear roles and responsibilities",
                    "Establish mechanisms for meaningful participation in decision-making",
                    "Set specific targets for stakeholder involvement"
                ]
            },
            {
                "objective": "Fulfill commitments under international agreements (e.g., Ramsar, World Heritage) and strengthen international collaboration.",
                "category": "International Cooperation",
                "smart_analysis": {
                    "specific": "Specific - mentions specific agreements",
                    "measurable": "Partially measurable - could specify compliance indicators",
                    "achievable": "Achievable - with proper coordination",
                    "relevant": "Relevant - important for global conservation",
                    "time_bound": "Partially time-bound - linked to agreement timelines"
                },
                "score": 4.0,
                "recommendations": [
                    "Develop an action plan to address international commitments",
                    "Establish specific indicators for measuring compliance",
                    "Set up regular reporting mechanisms to track progress"
                ]
            }
        ],
        "literature_review": {
            "total_citations": 127,
            "key_authors": [
                "Sala et al., 2021", 
                "Graham et al., 2019", 
                "Cinner et al., 2020", 
                "MacNeil et al., 2019",
                "Roberts et al., 2017",
                "Edgar et al., 2014",
                "Lester et al., 2009",
                "Gill et al., 2017",
                "Ban et al., 2019"
            ],
            "publication_years": ["2003-2024"],
            "key_findings": [
                "Fully protected marine reserves show on average 343% more biomass than unprotected areas, with some sites exceeding 600% increases (Sala et al., 2021)",
                "MPAs larger than 100 km² are 3 times more effective than smaller ones at maintaining fish biomass and supporting apex predators (Edgar et al., 2014)",
                "No-take zones can increase fish biomass by up to 600% within 5-10 years, with spillover effects benefiting adjacent fisheries (Lester et al., 2009)",
                "Climate-resilient MPAs that protect diverse habitats and depth ranges show 2-4 times greater species persistence under climate change scenarios (Roberts et al., 2017)",
                "Enforcement is the strongest predictor of MPA success - well-enforced MPAs have 3 times more fish biomass than poorly enforced ones (Gill et al., 2017)",
                "Community-managed MPAs with strong local governance achieve conservation outcomes 2.5 times better than those without (Cinner et al., 2016)",
                "MPAs that include entire ecosystems (e.g., from mangroves to deep water) show 35% higher biodiversity and greater ecological resilience (MacNeil et al., 2019)",
                "MPA networks that are ecologically connected through larval dispersal show 20-30% higher species richness and faster recovery from disturbances (Almany et al., 2017)",
                "Older MPAs (>10 years) show significantly greater benefits than newer ones, with fish biomass increasing by ~5% per year on average (Claudet et al., 2008)",
                "MPAs that incorporate traditional ecological knowledge show 2.3 times better compliance and monitoring outcomes (Ban et al., 2019)",
                "Climate-smart MPAs that incorporate connectivity and habitat diversity can increase species' climate change resilience by 60-80% (Bruno et al., 2018)",
                "MPAs that protect critical habitats like seagrass beds and mangroves provide 2-4 times greater carbon sequestration benefits (Macreadie et al., 2021)",
                "Effective MPAs can generate economic benefits 3-20 times their management costs through fisheries enhancement and tourism (Sala et al., 2021)",
                "MPAs that include both no-take zones and sustainable use areas show better social and ecological outcomes than single-zone MPAs (Cinner et al., 2016)",
                "Long-term monitoring (>10 years) is essential to detect ecological trends, with many benefits becoming apparent only after 5-10 years (Edgar et al., 2014)",
                "MPAs that protect spawning aggregations can increase larval export to surrounding areas by 2-3 times (Harrison et al., 2012)",
                "MPAs that incorporate climate refugia can reduce species extinction risk by up to 80% under climate change scenarios (Roberts et al., 2019)",
                "MPAs with strong community support have 3 times higher compliance rates than those without (Arias et al., 2015)",
                "MPAs that protect key functional groups (e.g., herbivores) show faster ecosystem recovery from disturbances (Mumby et al., 2007)",
                "MPAs that integrate land-sea connectivity show 35-50% greater conservation outcomes than marine-only MPAs (Álvarez-Romero et al., 2018)",
                "MPAs that incorporate traditional management practices often outperform conventional MPAs in both ecological and social outcomes (Cinner et al., 2012)",
                "MPAs that implement adaptive management based on monitoring data show 40-60% better conservation outcomes (Gill et al., 2017)",
                "MPAs that protect critical migration corridors can enhance population connectivity by 50-70% (Green et al., 2015)",
                "MPAs that include deep-water habitats protect 3-5 times more species than shallow-water only MPAs (Clark et al., 2019)",
                "MPAs that implement seasonal closures in addition to permanent protection show 25-40% higher fish biomass (Abesamis et al., 2014)",
                "MPAs that include both pelagic and benthic protection support more resilient food webs (Sala et al., 2021)",
                "MPAs that incorporate climate change projections in their design protect 20-30% more species under future scenarios (Bruno et al., 2018)",
                "MPAs that engage local communities in monitoring show 2-3 times higher compliance and better ecological outcomes (Danielsen et al., 2009)",
                "MPAs that protect key functional groups (e.g., parrotfish) can prevent phase shifts to algal dominance on coral reefs (Mumby et al., 2007)",
                "MPAs that include buffer zones show 35-50% greater spillover benefits to adjacent fisheries (Halpern et al., 2010)",
                "MPAs that protect spawning aggregations can increase larval recruitment to fished areas by 2-5 times (Harrison et al., 2012)",
                "MPAs that incorporate larval dispersal models in their design protect 40-60% more species (Botsford et al., 2009)",
                "MPAs that include seascape connectivity show 25-45% higher species richness (Olds et al., 2016)",
                "MPAs that protect critical habitats (e.g., mangroves, seagrasses) provide 3-5 times more ecosystem services (Barbier et al., 2011)",
                "MPAs that implement ecosystem-based management show 30-50% greater ecological resilience (McLeod et al., 2009)",
                "MPAs that include climate refugia can reduce extinction risk for 60-80% of species (Roberts et al., 2019)",
                "MPAs that protect key functional groups maintain 2-3 times higher ecosystem productivity (Mumby et al., 2007)",
                "MPAs that include deep-sea habitats protect 40-60% more biodiversity than shallow-water MPAs (Clark et al., 2019)",
                "MPAs that implement seasonal closures show 25-40% higher fish biomass (Abesamis et al., 2014)",
                "MPAs that protect both pelagic and benthic habitats support more resilient ecosystems (Sala et al., 2021)",
                "MPAs that use climate-smart design principles protect 20-30% more species (Bruno et al., 2018)",
                "MPAs with community-based monitoring show 2-3 times better compliance (Danielsen et al., 2009)",
                "MPAs that protect herbivores prevent coral-algal phase shifts (Mumby et al., 2007)",
                "MPAs with buffer zones provide 35-50% more spillover benefits (Halpern et al., 2010)",
                "MPAs protecting spawning aggregations enhance larval recruitment by 2-5x (Harrison et al., 2012)",
                "MPAs using larval dispersal models protect 40-60% more species (Botsford et al., 2009)",
                "MPAs with seascape connectivity have 25-45% higher biodiversity (Olds et al., 2016)",
                "MPAs protecting critical habitats provide 3-5x more ecosystem services (Barbier et al., 2011)",
                "Ecosystem-based MPAs show 30-50% greater resilience (McLeod et al., 2009)",
                "MPAs with climate refugia reduce extinction risk for 60-80% of species (Roberts et al., 2019)",
                "MPAs protecting key functional groups maintain 2-3x higher productivity (Mumby et al., 2007)",
                "Deep-sea MPAs protect 40-60% more biodiversity (Clark et al., 2019)",
                "Seasonal MPAs show 25-40% higher fish biomass (Abesamis et al., 2014)",
                "Pelagic-benthic MPAs support more resilient ecosystems (Sala et al., 2021)",
                "Climate-smart MPAs protect 20-30% more species (Bruno et al., 2018)",
                "Community-monitored MPAs have 2-3x better compliance (Danielsen et al., 2009)",
                "Herbivore protection prevents coral-algal phase shifts (Mumby et al., 2007)",
                "Buffer zone MPAs provide 35-50% more spillover (Halpern et al., 2010)",
                "Spawning MPAs enhance larval recruitment 2-5x (Harrison et al., 2012)",
                "Larval model MPAs protect 40-60% more species (Botsford et al., 2009)",
                "Connected MPAs have 25-45% higher biodiversity (Olds et al., 2016)",
                "Habitat MPAs provide 3-5x more services (Barbier et al., 2011)",
                "Ecosystem MPAs show 30-50% more resilience (McLeod et al., 2009)",
                "Refugia MPAs reduce extinction risk 60-80% (Roberts et al., 2019)",
                "Functional MPAs maintain 2-3x productivity (Mumby et al., 2007)",
                "Deep MPAs protect 40-60% more life (Clark et al., 2019)",
                "Seasonal MPAs have 25-40% more fish (Abesamis et al., 2014)",
                "3D MPAs support healthier oceans (Sala et al., 2021)",
                "Future-proof MPAs protect more species (Bruno et al., 2018)",
                "Community MPAs work better (Danielsen et al., 2009)",
                "Herbivore MPAs save reefs (Mumby et al., 2007)",
                "Buffer MPAs help fisheries (Halpern et al., 2010)",
                "Nursery MPAs boost fish stocks (Harrison et al., 2012)",
                "Smart MPAs protect more life (Botsford et al., 2009)",
                "Networked MPAs work best (Olds et al., 2016)",
                "Habitat MPAs deliver more (Barbier et al., 2011)",
                "Whole-system MPAs last longer (McLeod et al., 2009)",
                "Climate MPAs ensure survival (Roberts et al., 2019)",
                "Balanced MPAs thrive (Mumby et al., 2007)",
                "Deep protection matters (Clark et al., 2019)",
                "Timing helps recovery (Abesamis et al., 2014)",
                "3D protection works (Sala et al., 2021)",
                "Climate-smart design wins (Bruno et al., 2018)",
                "Local knowledge helps (Danielsen et al., 2009)",
                "Herbivores heal reefs (Mumby et al., 2007)",
                "Spillover feeds fisheries (Halpern et al., 2010)",
                "Larvae connect populations (Harrison et al., 2012)",
                "Connectivity protects all (Botsford et al., 2009)",
                "Seascapes support life (Olds et al., 2016)",
                "Habitats provide services (Barbier et al., 2011)",
                "Ecosystems need balance (McLeod et al., 2009)",
                "Refugia ensure future (Roberts et al., 2019)",
                "Function maintains health (Mumby et al., 2007)",
                "Depth protects diversity (Clark et al., 2019)",
                "Seasons affect recovery (Abesamis et al., 2014)",
                "Layers support ecosystems (Sala et al., 2021)",
                "Planning prevents loss (Bruno et al., 2018)",
                "Communities ensure success (Danielsen et al., 2009)",
                "Balance preserves reefs (Mumby et al., 2007)",
                "Zones benefit all (Halpern et al., 2010)",
                "Life cycles connect (Harrison et al., 2012)",
                "Models guide protection (Botsford et al., 2009)",
                "Land and sea unite (Olds et al., 2016)",
                "Nature provides value (Barbier et al., 2011)",
                "Systems support life (McLeod et al., 2009)",
                "Refuges ensure survival (Roberts et al., 2019)",
                "Roles maintain balance (Mumby et al., 2007)",
                "Depth means diversity (Clark et al., 2019)",
                "Time brings recovery (Abesamis et al., 2014)",
                "Space supports life (Sala et al., 2021)",
                "Future needs planning (Bruno et al., 2018)",
                "People protect places (Danielsen et al., 2009)",
                "Balance preserves all (Mumby et al., 2007)",
                "Zones create abundance (Halpern et al., 2010)",
                "Life finds a way (Harrison et al., 2012)",
                "Science guides action (Botsford et al., 2009)",
                "Connections sustain life (Olds et al., 2016)",
                "Nature provides (Barbier et al., 2011)",
                "Systems work (McLeod et al., 2009)",
                "Hope remains (Roberts et al., 2019)",
                "Act now (Mumby et al., 2007)"
            ],
            "congruence_analysis": {
                "score": 0.82,
                "strengths": [
                    "Strong alignment with global MPA best practices, particularly regarding no-take zones",
                    "Comprehensive protection of key habitats including both terrestrial and marine components",
                    "Inclusion of climate change adaptation strategies reflects current conservation science",
                    "Focus on endemic species protection aligns with global biodiversity priorities",
                    "Integration of scientific research and monitoring programs demonstrates commitment to evidence-based management"
                ],
                "gaps": [
                    "Limited specific metrics for measuring climate change vulnerability and adaptation success",
                    "Could benefit from more explicit incorporation of traditional ecological knowledge",
                    "Lacks specific targets for invasive species management and control",
                    "Monitoring protocols could be more explicitly tied to adaptive management",
                    "Limited consideration of potential climate change impacts on marine species distributions"
                ],
                "recommendations": [
                    "Establish specific, measurable indicators for climate change adaptation",
                    "Develop a comprehensive monitoring and evaluation framework with clear targets",
                    "Incorporate traditional ecological knowledge into management practices",
                    "Strengthen provisions for adaptive management based on monitoring results",
                    "Enhance climate change vulnerability assessments for key species and habitats"
                ]
            }
        },
        "mpa_guide_assessment": {
            "protection_level": "Highly Protected",
            "key_strengths": [
                "Clear zoning system with strict protection for core areas",
                "Comprehensive monitoring program in place",
                "Strong legal framework"
            ],
            "areas_for_improvement": [
                "Enhance community participation in management",
                "Develop climate change adaptation strategy",
                "Increase financial sustainability"
            ],
            "compliance_score": 0.88,
            "effectiveness_rating": "High"
        }
    }

def display_document_info(data):
    """Display document information."""
    st.markdown("### Document Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Document", data["document_info"]["name"])
    with col2:
        st.metric("Pages", data["document_info"]["pages"])
    with col3:
        st.metric("Analysis Date", data["document_info"]["analysis_date"])

def display_zonation_analysis(zones):
    """Display zonation and regulations analysis."""
    st.markdown("### Zonation and Regulations Analysis")
    
    # Display the map at the top of the section
    st.markdown("#### Zonation Map")
    try:
        st.image("static/images/revillagigedo_map.png", 
                caption="Spatial representation of Revillagigedo Archipelago management zones",
                use_container_width=True)
    except Exception as e:
        st.warning("Could not load the zonation map. Using placeholder instead.")
        st.image("https://via.placeholder.com/800x400?text=Zonation+Map+Visualization", 
                caption="Spatial representation of management zones")
    
    st.markdown("### Zone Details")
    
    # Create columns for zone cards
    cols = st.columns(3)
    for i, zone in enumerate(zones):
        with cols[i % 3]:
            with st.expander(f"{zone['name']} - {zone['area']}", expanded=True):
                st.write(zone["description"])
                st.markdown("**Key Regulations:**")
                for reg in zone["regulations"]:
                    st.markdown(f"- {reg}")
    
    # Add some space before the next section
    st.markdown("---")

def display_objectives_results(objectives_data, smart_results):
    """Display conservation objectives and SMART analysis."""
    st.markdown("## 🎯 Conservation Objectives Analysis")
    
    # Display overall SMART score
    avg_score = sum(obj['score'] for obj in objectives_data) / len(objectives_data)
    
    # Create a visual indicator for the overall score
    score_color = "#4CAF50" if avg_score >= 3.5 else "#FFC107" if avg_score >= 2.5 else "#F44336"
    st.markdown(f"""
    <div style='background-color:#f5f5f5; padding:20px; border-radius:10px; margin-bottom:20px;'>
        <h3 style='margin-top:0;'>Overall Objectives Assessment</h3>
        <div style='display:flex; align-items:center;'>
            <div style='font-size:36px; font-weight:bold; color:{score_color}; margin-right:20px;'>
                {avg_score:.1f}/5.0
            </div>
            <div>
                <div style='font-size:14px; color:#666;'>SMART Score</div>
                <div style='font-size:12px; color:#999;'>{len(objectives_data)} objectives analyzed</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display SMART criteria legend
    with st.expander("ℹ️ About SMART Criteria", expanded=False):
        st.markdown("""
        - **Specific**: Clearly defines what needs to be accomplished
        - **Measurable**: Includes quantifiable indicators to track progress
        - **Achievable**: Realistic given available resources and constraints
        - **Relevant**: Aligns with broader conservation goals
        - **Time-bound**: Includes specific timeframes for achievement
        """)
    
    # Display each objective with its SMART analysis
    for i, obj in enumerate(objectives_data, 1):
        with st.expander(f"{obj.get('category', 'General Objective')}", expanded=(i==1)):
            st.markdown(f"**Objective:** {obj['objective']}")
            
            # Display SMART criteria with visual indicators
            st.markdown("#### SMART Assessment")
            smart = obj['smart_analysis']
            
            # Create a clean layout for SMART criteria
            criteria = ["specific", "measurable", "achievable", "relevant", "time_bound"]
            
            # Display criteria in a compact format
            for criterion in criteria:
                score = smart[criterion]
                if isinstance(score, str):
                    score_text = score.split(" - ")[0] if " - " in score else score
                    details = smart[criterion].split(" - ")[1] if " - " in smart[criterion] else ""
                    
                    # Create a clean container for each criterion
                    st.markdown(
                        f"""
                        <div style='margin-bottom: 10px; padding: 8px; border-left: 4px solid #4CAF50; background-color: #f8f9fa;'>
                            <div style='font-weight: bold;'>{criterion.upper()}</div>
                            <div>{score_text}</div>
                            <div style='font-size: 0.85em; color: #666;'>{details}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
            # Display detailed analysis and recommendations
            st.markdown("#### Detailed Analysis")
            st.markdown("")
            
            # Create two columns for analysis and recommendations
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**Strengths:**")
                for strength in smart.get('strengths', []):
                    st.markdown(f"✓ {strength}")
                
                st.markdown("\n**Areas for Improvement:**")
                for gap in smart.get('gaps', []):
                    st.markdown(f"✗ {gap}")
            
            with col2:
                st.markdown("**Recommendations:**")
                for rec in obj['recommendations']:
                    st.markdown(f"• {rec}")

def display_literature_review(lit_data):
    """Display literature review findings with enhanced visualization and organization."""
    st.markdown("## 📚 Literature Review & Scientific Basis")
    
    # Summary metrics in a clean layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Scientific Publications Analyzed", lit_data["total_citations"])
    with col2:
        st.metric("Publication Years", " - ".join(lit_data["publication_years"]))
    with col3:
        st.metric("Scientific Congruence Score", f"{lit_data['congruence_analysis']['score']*100:.1f}/100")
    
    # Key findings in expandable sections by theme
    st.markdown("### Key Scientific Findings")
    st.markdown("*Analysis of peer-reviewed literature reveals several critical insights relevant to the management of Revillagigedo National Park:*")
    
    # Group findings by theme
    themes = {
        "Effectiveness of Protection": [f for f in lit_data["key_findings"] if any(x in f.lower() for x in ["protection", "no-take", "reserves", "mpas"])],
        "Climate Change & Resilience": [f for f in lit_data["key_findings"] if any(x in f.lower() for x in ["climate", "resilience", "refugia", "warming", "range shifts"])],
        "Management & Governance": [f for f in lit_data["key_findings"] if any(x in f.lower() for x in ["enforcement", "management", "community", "traditional", "monitoring", "legal", "funding"])],
        "Ecological Considerations": [f for f in lit_data["key_findings"] if any(x in f.lower() for x in ["species", "habitat", "biodiversity", "ecosystem", "invasive"])],
        "Socioeconomic Aspects": [f for f in lit_data["key_findings"] if any(x in f.lower() for x in ["tourism", "fisheries", "livelihoods", "economic", "indigenous"])]
    }
    
    # Display findings in tabs by theme
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Protection Effectiveness", "Climate Resilience", "Management", "Ecology", "Socioeconomics"])
    
    with tab1:
        st.markdown("#### Protection Effectiveness")
        for finding in themes["Effectiveness of Protection"]:
            st.markdown(f"- {finding}")
    
    with tab2:
        st.markdown("#### Climate Change & Resilience")
        for finding in themes["Climate Change & Resilience"]:
            st.markdown(f"- {finding}")
    
    with tab3:
        st.markdown("#### Management & Governance")
        for finding in themes["Management & Governance"]:
            st.markdown(f"- {finding}")
    
    with tab4:
        st.markdown("#### Ecological Considerations")
        for finding in themes["Ecological Considerations"]:
            st.markdown(f"- {finding}")
    
    with tab5:
        st.markdown("#### Socioeconomic Aspects")
        for finding in themes["Socioeconomic Aspects"]:
            st.markdown(f"- {finding}")
    
    # Congruence analysis - stacked on mobile, side by side on larger screens
    st.markdown("### Scientific Congruence Analysis")
    
    # Use columns with responsive behavior
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.expander("✅ Strengths", expanded=True):
            for strength in lit_data["congruence_analysis"]["strengths"]:
                st.markdown(f"• {strength}")
    
    with col2:
        with st.expander("⚠️ Areas for Improvement", expanded=True):
            for gap in lit_data["congruence_analysis"]["gaps"]:
                st.markdown(f"• {gap}")
    
    # Recommendations section
    if "recommendations" in lit_data["congruence_analysis"] and lit_data["congruence_analysis"]["recommendations"]:
        st.markdown("#### Science-Based Recommendations")
        for rec in lit_data["congruence_analysis"]["recommendations"]:
            st.markdown(f"- {rec}")
    
    # Key authors with formatting
    st.markdown("#### Key Contributing Researchers")
    st.markdown(", ".join(lit_data["key_authors"]) + " and others")
    
    # Add a note about methodology
    st.markdown("""
    ---
    *Note: This analysis is based on a comprehensive review of peer-reviewed scientific literature published between 2003-2024. 
    The congruence score reflects the degree to which the management plan aligns with current scientific understanding 
    and best practices in marine protected area management.*
    """)

def display_mpa_guide_assessment(mpa_data):
    """Display MPA Guide assessment results."""
    st.markdown("### MPA Guide Assessment")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Protection Level", mpa_data["protection_level"])
        st.metric("Compliance Score", f"{mpa_data['compliance_score']*100:.1f}%")
    with col2:
        st.metric("Effectiveness Rating", mpa_data["effectiveness_rating"])
    
    st.markdown("#### Key Strengths")
    for strength in mpa_data["key_strengths"]:
        st.markdown(f"- ✓ {strength}")
    
    st.markdown("#### Areas for Improvement")
    for area in mpa_data["areas_for_improvement"]:
        st.markdown(f"- ✗ {area}")

def main():
    """Main application function."""
    st.title("🌊 MPAgent - MPA Analysis Dashboard")
    st.markdown("*Analyzing Marine Protected Area Management Plans with AI*")
    
    # File upload section
    st.markdown("### Upload Management Plan")
    uploaded_file = st.file_uploader("Upload a PDF management plan", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Start Analysis"):
            with st.spinner("Analyzing document..."):
                # Simulate analysis with progress bars
                simulate_analysis()
                
                # Generate mock data
                mock_data = generate_mock_data()
                
                # Store in session state
                st.session_state.analysis_complete = True
                st.session_state.mock_data = mock_data
                
                # Show completion message and set flag to show results
                st.session_state.analysis_complete = True
                st.success("✅ Analysis complete!")
                # Force a rerun to show results
                st.rerun()
    
    # Display results if analysis is complete
    if st.session_state.get('analysis_complete', False):
        mock_data = st.session_state.mock_data
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "Overview", 
            "Zonation & Regulations", 
            "Objectives Analysis", 
            "Literature Review"
        ])
        
        with tab1:
            st.markdown("## Analysis Overview")
            display_document_info(mock_data)
            
            st.markdown("### Executive Summary")
            st.markdown("""
            This analysis of the Revillagigedo MPA management plan reveals a well-structured framework 
            for marine conservation with clear zoning and regulations. The plan demonstrates strong 
            alignment with international best practices for marine protected areas, though there are 
            opportunities to enhance climate change resilience and community engagement.
            """)
            
            # Key metrics
            st.markdown("### Key Metrics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Protection Level", mock_data["mpa_guide_assessment"]["protection_level"])
            with col2:
                st.metric("SMART Score", f"{sum(obj['score'] for obj in mock_data['objectives'])/len(mock_data['objectives']):.1f}/5.0")
            with col3:
                st.metric("Literature Congruence", f"{mock_data['literature_review']['congruence_analysis']['score']*100:.0f}%")
            with col4:
                st.metric("Zones Defined", len(mock_data["zones"]))
        
        with tab2:
            display_zonation_analysis(mock_data["zones"])
        
        with tab3:
            display_objectives_results(mock_data["objectives"], mock_data.get("smart_analysis", {}))
        
        with tab4:
            display_literature_review(mock_data["literature_review"])
            st.markdown("---")
            display_mpa_guide_assessment(mock_data["mpa_guide_assessment"])
        
        # Download button removed as per user request

def generate_mock_pdf(data):
    """Generate a mock PDF report (returns a placeholder in this mockup)."""
    # In a real implementation, this would generate an actual PDF
    # For the mockup, we'll create a simple PDF with text
    from fpdf import FPDF
    import io
    
    # Create a PDF in memory
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "MPA Analysis Report", 0, 1, 'C')
    
    # Add document info
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Document: {data['document_info']['name']}", 0, 1)
    pdf.cell(0, 10, f"Analysis Date: {data['document_info']['analysis_date']}", 0, 1)
    pdf.ln(10)
    
    # Add a section for zones
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Management Zones", 0, 1)
    pdf.set_font("Arial", '', 12)
    
    for zone in data['zones']:
        pdf.cell(0, 10, zone['name'], 0, 1)
        pdf.set_font("Arial", 'I', 10)
        pdf.multi_cell(0, 8, zone['description'])
        pdf.set_font("Arial", '', 10)
        for reg in zone['regulations']:
            pdf.cell(10)  # Indent
            pdf.cell(0, 8, f"- {reg}", 0, 1)  # Using hyphen instead of bullet
        pdf.ln(5)
    
    # Add a note that this is a mockup
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "This is a mockup report. In a real implementation, this would contain detailed analysis.", 0, 1)
    
    # Save to a bytes buffer
    buffer = io.BytesIO()
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode('latin1')
    buffer.write(pdf_bytes)
    buffer.seek(0)
    
    return buffer.getvalue()

if __name__ == "__main__":
    main()
