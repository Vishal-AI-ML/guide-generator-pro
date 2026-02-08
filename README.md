# 🤖 AI-Powered Documentation Generator

> Enterprise-grade multi-agent AI system for automated technical documentation generation from diverse sources

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.86.0-FF6B35?style=for-the-badge)](https://www.crewai.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

[Features](#-key-features) • [Architecture](#️-system-architecture) • [Installation](#-installation) • [Usage](#-usage) • [API Docs](#-api-documentation)

</div>

---

## 📋 **Table of Contents**

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#️-system-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Performance Metrics](#-performance-metrics)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 **Overview**

An intelligent, production-ready documentation generation platform that leverages **multi-agent AI orchestration** to automatically research, synthesize, and generate comprehensive getting-started guides from multiple sources including YouTube videos, web articles, academic papers, and technical documents.

### **Problem Statement**

Manual documentation creation is time-consuming, requiring researchers to:
- ❌ Search across multiple platforms (YouTube, web, academic databases)
- ❌ Read and synthesize lengthy content
- ❌ Transform technical research into beginner-friendly guides
- ❌ Maintain consistency across documentation

### **Solution**

This system automates the entire workflow using:
- ✅ **Multi-agent AI** for parallel source processing
- ✅ **Hierarchical orchestration** for intelligent task delegation
- ✅ **Automated synthesis** of research findings
- ✅ **Production-grade API** with async processing
- ✅ **Real-time monitoring** dashboard

---

## ✨ **Key Features**

### **🤝 Multi-Agent Architecture**
- **Hierarchical Research Crew** with specialized agents (YouTube, Web, ArXiv, Document)
- **Sequential Writing Crew** for content creation and editing
- **Manager-led delegation** for optimal task distribution

### **🚀 Production-Ready API**
- RESTful API built with **FastAPI**
- **Asynchronous background processing** for long-running tasks
- **Swagger/OpenAPI** documentation
- **CORS-enabled** for cross-origin requests

### **📊 Real-Time Monitoring**
- **Streamlit dashboard** with live progress tracking
- Generation history and analytics
- Performance metrics visualization
- One-click guide downloads

### **💾 Data Persistence**
- **SQLAlchemy ORM** for database abstraction
- SQLite/PostgreSQL support
- Complete generation history tracking
- Performance metrics storage

### **📈 Performance Analytics**
- Execution time tracking
- Word count analysis
- Success rate monitoring
- Detailed error logging
- JSON metrics export

### **🔌 Multi-Source Integration**
- YouTube videos and channels
- Web pages and blogs
- ArXiv research papers
- PDF, Text, and Markdown documents

---

## 🏗️ **System Architecture**
```
┌─────────────────────────────────────────────────────────────────┐
│                     Client Layer                                │
│  ┌──────────────────┐              ┌──────────────────┐        │
│  │   Web Browser    │              │   API Client     │        │
│  │  (Dashboard UI)  │              │  (cURL/Postman)  │        │
│  └────────┬─────────┘              └────────┬─────────┘        │
└───────────┼──────────────────────────────────┼──────────────────┘
            │                                  │
            ▼                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Streamlit Dashboard (Port 8501)             │  │
│  │         • Real-time Status      • History View           │  │
│  │         • File Downloads        • Metrics Display        │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                           │
│  ┌──────────────────▼───────────────────────────────────────┐  │
│  │              FastAPI Server (Port 8000)                  │  │
│  │  ┌────────────┐  ┌────────────┐  ┌─────────────────┐    │  │
│  │  │  REST API  │  │ Background │  │  File Manager   │    │  │
│  │  │  Endpoints │  │   Tasks    │  │   (outputs/)    │    │  │
│  │  └────────────┘  └────────────┘  └─────────────────┘    │  │
│  └──────────────────┬───────────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              GuideGeneratorFlow (Orchestrator)           │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Metrics Tracker  │  Logger  │  Error Handler     │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                           │
│  ┌──────────────────▼───────────────────────────────────────┐  │
│  │           Research Crew (Hierarchical Process)           │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │         Research Manager (Coordinator)             │  │  │
│  │  └──────────┬─────────────────────────┬────────────────┘  │  │
│  │      ┌──────┴──────┬──────────┬───────┴──────┐           │  │
│  │      ▼             ▼          ▼              ▼           │  │
│  │  ┌────────┐   ┌────────┐ ┌────────┐   ┌──────────┐     │  │
│  │  │YouTube │   │  Web   │ │ ArXiv  │   │ Document │     │  │
│  │  │Specialist   │Specialist│Specialist  │Specialist│     │  │
│  │  └────────┘   └────────┘ └────────┘   └──────────┘     │  │
│  │  Tools: YT Search, Channel Search, Web Scraping,        │  │
│  │         Selenium, ArXiv API, PDF Reader, File Reader    │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                           │
│  ┌──────────────────▼───────────────────────────────────────┐  │
│  │           Writing Crew (Sequential Process)              │  │
│  │  ┌──────────────────┐        ┌───────────────────┐      │  │
│  │  │ Technical Writer │   ──►  │  Content Editor   │      │  │
│  │  │  (Guide Creator) │        │ (Quality Assurance)│      │  │
│  │  └──────────────────┘        └───────────────────┘      │  │
│  └──────────────────┬───────────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Data Layer                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            SQLAlchemy ORM (Database Abstraction)         │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Models: GuideGeneration, Metrics, Performance    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────┬───────────────────────────────────────┘  │
│                     │                                           │
│  ┌──────────────────▼───────────────────────────────────────┐  │
│  │              SQLite Database (guide_generator.db)        │  │
│  │  Tables: guide_generations, metrics                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### **Workflow Diagram**
```
User Input (Sources)
        │
        ▼
┌──────────────────┐
│  Input Validation │
│   & Generation ID │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Research Crew   │ ──► YouTube Specialist ──► Video transcripts
│  (Parallel)      │ ──► Web Specialist ──────► Web content
│                  │ ──► ArXiv Specialist ────► Research papers
│                  │ ──► Document Specialist ─► PDF/Text files
└────────┬─────────┘
         │
         ▼ (Research Report - 5000+ words)
┌──────────────────┐
│  Writing Crew    │ ──► Technical Writer ────► Draft guide
│  (Sequential)    │ ──► Content Editor ──────► Polished guide
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Output Storage  │ ──► Guide saved (outputs/)
│  & Metrics       │ ──► Metrics saved (JSON)
│                  │ ──► DB updated (SQLite)
└──────────────────┘
```

---

## 🛠️ **Tech Stack**

### **Core Framework**
| Technology | Version | Purpose |
|------------|---------|---------|
| **[Python](https://python.org)** | 3.10+ | Primary programming language |
| **[CrewAI](https://crewai.com)** | 0.86.0 | Multi-agent orchestration framework |
| **[OpenAI API](https://openai.com)** | Latest | LLM inference (GPT-4o-mini/GPT-4o) |

### **Backend & API**
| Technology | Version | Purpose |
|------------|---------|---------|
| **[FastAPI](https://fastapi.tiangolo.com)** | 0.115.6 | High-performance async web framework |
| **[Uvicorn](https://uvicorn.org)** | 0.34.0 | ASGI server for FastAPI |
| **[Pydantic](https://pydantic.dev)** | 2.10.3 | Data validation and settings |

### **Database**
| Technology | Version | Purpose |
|------------|---------|---------|
| **[SQLAlchemy](https://sqlalchemy.org)** | 2.0.36 | SQL toolkit and ORM |
| **SQLite** | Built-in | Embedded relational database |

### **Frontend & UI**
| Technology | Version | Purpose |
|------------|---------|---------|
| **[Streamlit](https://streamlit.io)** | 1.41.1 | Interactive dashboard framework |

### **AI Tools & Integrations**
| Tool | Purpose |
|------|---------|
| **YoutubeVideoSearchTool** | YouTube video content extraction |
| **YoutubeChannelSearchTool** | Channel-wide content analysis |
| **ScrapeWebsiteTool** | Static web page scraping |
| **SeleniumScrapingTool** | Dynamic web content extraction |
| **ArxivPaperTool** | Academic paper downloading & parsing |
| **PDFSearchTool** | PDF document analysis |
| **TXTSearchTool** | Text file processing |
| **MDXSearchTool** | Markdown document parsing |

### **Utilities**
| Technology | Purpose |
|------------|---------|
| **python-dotenv** | Environment variable management |
| **aiofiles** | Async file operations |
| **logging** | Structured application logging |

---

## 📦 **Installation**

### **Prerequisites**
```bash
# System Requirements
- Python 3.10 or higher
- pip (Python package installer)
- 4GB+ RAM (8GB recommended)
- Internet connection

# Required Accounts
- OpenAI API account with active API key
```

### **Step 1: Clone Repository**
```bash
git clone https://github.com/Vishal-AI-ML/guide-generator-pro.git
cd guide-generator-pro
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt
```

### **Step 4: Environment Configuration**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file and add your credentials
```

**Required Environment Variables:**
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
OPENAI_MODEL_NAME=gpt-4o-mini

# Database
DATABASE_URL=sqlite:///./guide_generator.db

# API Server
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

---

## 🚀 **Usage**

### **Method 1: Web Dashboard (Recommended)**
```bash
# Terminal 1: Start API Server
uvicorn src.guide_generator_pro.api.app:app --reload --port 8000

# Terminal 2: Start Dashboard
streamlit run dashboard.py
```

**Access:**
- Dashboard: `http://localhost:8501`
- API Docs: `http://localhost:8000/docs`

### **Method 2: API Only**
```bash
# Start API server
uvicorn src.guide_generator_pro.api.app:app --reload --port 8000

# Access Swagger UI
http://localhost:8000/docs
```

### **Method 3: Command Line**
```bash
# Run from terminal (interactive mode)
python -m src.guide_generator_pro.main
```

---

## 📚 **API Documentation**

### **Base URL**
```
http://localhost:8000
```

### **Endpoints**

#### **1. Health Check**
```http
GET /
```

**Response:**
```json
{
  "message": "AI Guide Generator API",
  "version": "1.0.0",
  "endpoints": {
    "generate": "/api/v1/generate",
    "status": "/api/v1/status/{generation_id}",
    "download": "/api/v1/download/{generation_id}",
    "history": "/api/v1/history"
  }
}
```

#### **2. Generate Guide**
```http
POST /api/v1/generate
```

**Request Body:**
```json
{
  "youtube_links": "https://youtube.com/watch?v=example",
  "webpage_links": "https://blog.example.com/tutorial",
  "research_paper_links": "https://arxiv.org/abs/2310.05421",
  "document_paths": "path/to/document.pdf"
}
```

**Response:**
```json
{
  "generation_id": "a1b2c3d4",
  "status": "processing",
  "message": "Guide generation started"
}
```

#### **3. Check Status**
```http
GET /api/v1/status/{generation_id}
```

**Response:**
```json
{
  "status": "completed",
  "word_count": 3542,
  "created_at": "2026-02-08T10:23:03"
}
```

#### **4. Download Guide**
```http
GET /api/v1/download/{generation_id}
```

**Response:** Markdown file download

#### **5. Generation History**
```http
GET /api/v1/history?limit=10
```

**Response:**
```json
[
  {
    "id": "a1b2c3d4",
    "created_at": "2026-02-08T10:23:03",
    "status": "completed",
    "word_count": 3542,
    "execution_time": 369.54,
    "sources_count": 3
  }
]
```

### **cURL Examples**
```bash
# Generate guide
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_links": "https://youtube.com/watch?v=example",
    "webpage_links": "https://example.com/blog"
  }'

# Check status
curl http://localhost:8000/api/v1/status/a1b2c3d4

# Download guide
curl -O http://localhost:8000/api/v1/download/a1b2c3d4
```

---

## 📁 **Project Structure**
```
guide-generator-pro/
│
├── src/
│   └── guide_generator_pro/
│       ├── __init__.py
│       ├── main.py                    # CLI entry point
│       ├── flow.py                    # Main orchestration flow
│       │
│       ├── api/                       # FastAPI application
│       │   ├── __init__.py
│       │   └── app.py                 # API endpoints & server
│       │
│       ├── crews/                     # Multi-agent crews
│       │   ├── __init__.py
│       │   ├── research_crew/         # Hierarchical research
│       │   │   ├── __init__.py
│       │   │   ├── research_crew.py
│       │   │   └── config/
│       │   │       ├── agents.yaml    # Agent definitions
│       │   │       └── tasks.yaml     # Task definitions
│       │   │
│       │   └── writing_crew/          # Sequential writing
│       │       ├── __init__.py
│       │       ├── writing_crew.py
│       │       └── config/
│       │           ├── agents.yaml
│       │           └── tasks.yaml
│       │
│       ├── database/                  # Data persistence
│       │   ├── __init__.py
│       │   ├── models.py              # SQLAlchemy models
│       │   └── manager.py             # Database operations
│       │
│       └── utils/                     # Utilities
│           ├── __init__.py
│           ├── logger.py              # Logging configuration
│           └── metrics.py             # Performance tracking
│
├── dashboard.py                       # Streamlit dashboard
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore rules
├── README.md                          # This file
│
├── logs/                              # Application logs
│   └── guide_generator_YYYYMMDD.log
│
├── outputs/                           # Generated files
│   ├── getting_started_guide.md       # Output guides
│   └── metrics_*.json                 # Performance metrics
│
└── guide_generator.db                 # SQLite database
```

---

## 📊 **Performance Metrics**

### **System Benchmarks**

| Metric | Value |
|--------|-------|
| **Average Generation Time** | 5-8 minutes |
| **Typical Output Length** | 3000-5000 words |
| **Max Sources per Generation** | Unlimited |
| **Concurrent Requests** | Async (non-blocking) |
| **API Response Time** | < 200ms (status checks) |
| **Database Query Time** | < 50ms |

### **Agent Performance**

| Agent | Avg. Execution Time |
|-------|---------------------|
| Research Manager | 2-3 minutes |
| YouTube Specialist | 1-2 minutes |
| Web Specialist | 1-2 minutes |
| ArXiv Specialist | 1-2 minutes |
| Document Specialist | 1-2 minutes |
| Technical Writer | 2-3 minutes |
| Content Editor | 1-2 minutes |

---

## 🤝 **Contributing**

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create feature branch**
```bash
   git checkout -b feature/AmazingFeature
```
3. **Commit changes**
```bash
   git commit -m 'Add some AmazingFeature'
```
4. **Push to branch**
```bash
   git push origin feature/AmazingFeature
```
5. **Open Pull Request**

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black src/

# Linting
flake8 src/
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 **Author**

**Vishal**

- 🌐 GitHub: [[@Vishal-AI-ML](https://github.com/Vishal-AI-ML)](https://github.com/Vishal-AI-ML/guide-generator-pro)
- 💼 LinkedIn: https://www.linkedin.com/in/vishal-shivhare-562508243/
- 📧 Email: vishalshivhare.ai@gmail.com

---

## 🙏 **Acknowledgments**

- **[CrewAI](https://crewai.com)** - For the powerful multi-agent framework
- **[OpenAI](https://openai.com)** - For GPT models and API
- **[FastAPI](https://fastapi.tiangolo.com)** - For the modern web framework
- **[Streamlit](https://streamlit.io)** - For the intuitive dashboard framework

---

## 📞 **Support**

For questions, issues, or feedback:

- 📝 **Open an Issue**: [GitHub Issues](https://github.com/Vishal-AI-ML/guide-generator-pro/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Vishal-AI-ML/guide-generator-pro/discussions)
- 📧 **Email**: your.email@example.com

---

## 🗺️ **Roadmap**

### **Phase 1: Current** ✅
- [x] Multi-agent system
- [x] REST API
- [x] Web dashboard
- [x] Database persistence
- [x] Performance metrics

### **Phase 2: Planned** 🚧
- [ ] Redis caching layer
- [ ] PostgreSQL support
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Unit & integration tests
- [ ] Webhook notifications

### **Phase 3: Future** 🔮
- [ ] User authentication
- [ ] Multi-tenancy support
- [ ] Advanced analytics dashboard
- [ ] Custom agent creation
- [ ] Cloud deployment (AWS/GCP/Azure)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ using CrewAI, FastAPI, and Streamlit

</div>
