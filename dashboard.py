import streamlit as st
import requests
import time
from pathlib import Path

st.set_page_config(
    page_title="AI Guide Generator",
    page_icon="📚",
    layout="wide"
)

# API Base URL
API_URL = "http://localhost:8000"

st.title("🤖 AI-Powered Documentation Generator")
st.markdown("Transform research into polished getting-started guides")

# Sidebar for inputs
with st.sidebar:
    st.header("📥 Input Sources")
    
    youtube_links = st.text_area(
        "YouTube Links",
        placeholder="https://youtube.com/watch?v=...",
        help="Enter YouTube video or channel URLs (comma-separated)"
    )
    
    webpage_links = st.text_area(
        "Web Pages",
        placeholder="https://example.com/article",
        help="Enter article or documentation URLs"
    )
    
    research_paper_links = st.text_area(
        "Research Papers",
        placeholder="https://arxiv.org/abs/...",
        help="Enter arXiv paper URLs"
    )
    
    document_paths = st.text_area(
        "Document Paths",
        placeholder="path/to/document.pdf",
        help="Enter local file paths"
    )
    
    generate_btn = st.button("🚀 Generate Guide", type="primary", use_container_width=True)

# Main content
tab1, tab2 = st.tabs(["📊 Generation", "📜 History"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Generation Status")
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        message_placeholder = st.empty()
    
    with col2:
        st.subheader("Metrics")
        metric_sources = st.metric("Sources", "0")
        metric_status = st.metric("Status", "Idle")

with tab2:
    st.subheader("Recent Generations")
    
    try:
        response = requests.get(f"{API_URL}/api/v1/history")
        if response.status_code == 200:
            history = response.json()
            if history:
                st.dataframe(
                    history,
                    use_container_width=True,
                    column_config={
                        "id": "Generation ID",
                        "created_at": "Created",
                        "status": "Status",
                        "word_count": "Words",
                        "execution_time": "Time (s)",
                        "sources_count": "Sources"
                    }
                )
            else:
                st.info("No generation history yet")
        else:
            st.warning("Could not fetch history. Is the API running?")
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        st.info("💡 Start the API with: `uvicorn src.guide_generator_pro.api.app:app --reload`")

# Generation logic
if generate_btn:
    # Count sources
    sources_count = sum(1 for s in [youtube_links, webpage_links, research_paper_links, document_paths] if s.strip())
    
    if sources_count == 0:
        st.error("⚠️ Please provide at least one source!")
    else:
        try:
            # Call API
            response = requests.post(
                f"{API_URL}/api/v1/generate",
                json={
                    "youtube_links": youtube_links,
                    "webpage_links": webpage_links,
                    "research_paper_links": research_paper_links,
                    "document_paths": document_paths
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                generation_id = data["generation_id"]
                
                status_placeholder.info(f"Generation ID: `{generation_id}`")
                
                # Poll for status
                while True:
                    status_resp = requests.get(f"{API_URL}/api/v1/status/{generation_id}")
                    
                    if status_resp.status_code == 200:
                        status_data = status_resp.json()
                        
                        # Update progress
                        progress = status_data.get("progress", 0)
                        progress_bar.progress(progress / 100)
                        
                        status = status_data.get("status", "unknown")
                        message = status_data.get("message", "Processing...")
                        
                        message_placeholder.info(f"Status: {status} - {message}")
                        
                        if status == "completed":
                            st.success("✅ Guide generated successfully!")
                            
                            # Download button
                            download_url = f"{API_URL}/api/v1/download/{generation_id}"
                            st.markdown(f"[📥 Download Guide]({download_url})")
                            
                            # Show metrics
                            word_count = status_data.get("word_count", 0)
                            st.metric("Word Count", word_count)
                            break
                        
                        elif status == "failed":
                            error = status_data.get("error", "Unknown error")
                            st.error(f"❌ Generation failed: {error}")
                            break
                    
                    time.sleep(2)
            else:
                st.error(f"API Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to API")
            st.info("💡 Start the API with: `uvicorn src.guide_generator_pro.api.app:app --reload`")
        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("Built with CrewAI, FastAPI, and Streamlit")