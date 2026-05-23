# YouTube Thumbnail Designer Agent

An end-to-end AI agent system built using LangGraph that autonomously generates and improves YouTube thumbnails using the Reflection Pattern.

The agent:
- searches the web for thumbnail inspiration
- writes optimized thumbnail prompts
- generates thumbnails using OpenAI image generation
- critiques thumbnails using GPT-4o Vision
- iteratively improves thumbnails until a target rating is achieved

---

# Architecture

The workflow is built entirely using LangGraph.

```text
START
  ↓
web_search
  ↓
prompt_writer
  ↓
generator
  ↓
critic
  ↓
should_continue
 ↙            ↘
prompt_writer   saver
                  ↓
                 END
```

---

# Features

- LangGraph StateGraph workflow
- Reflection-based AI agent loop
- Tavily web search integration
- AI image generation
- Vision-based thumbnail critique
- Structured output with Pydantic
- Conditional graph edges
- Reducer-based state history
- Automatic report generation
- Graph visualization

---

# Tech Stack

- Python 3.11+
- LangGraph
- LangChain
- OpenAI API
- GPT-4o-mini
- OpenAI Image Generation
- Tavily Search API
- Pydantic

---

# Project Structure

```text
youtube-thumbnail-agent/
│
├── app/
│   ├── graph.py
│   ├── nodes.py
│   ├── prompts.py
│   ├── state.py
│   └── tools.py
│
├── outputs/
│
├── main.py
├── make_diagram.py
├── graph.png
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your_repo_url>
cd youtube-thumbnail-agent
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Add Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

# Running The Project

Run the agent:

```bash
python main.py
```

---

# Generate Graph Diagram

```bash
python make_diagram.py
```

This generates:

```text
graph.png
```

---

# Outputs

Generated outputs are stored inside:

```text
outputs/<timestamp>_<topic>/
```

Each run contains:

- iter_1.png
- iter_2.png
- final.png
- report.md

---

# Reflection Loop

The system uses a reflection-based improvement loop.

The critic evaluates:
- readability
- contrast
- emotional impact
- clickability
- composition

If the rating is below the target score:
- the critique is fed back into the prompt writer
- a new thumbnail is generated
- the loop continues

Termination Conditions:
- rating >= target_rating
OR
- iteration >= max_iterations

---

# Example Flow

Iteration 1:
- rating: 7
- critique generated

Iteration 2:
- improved prompt
- new thumbnail generated
- rating: 8

System saves:
- final.png
- report.md

---

# Future Improvements

- Better thumbnail aesthetic tuning
- Multi-style thumbnail generation
- YouTube trend analysis
- Multi-agent collaboration
- Automatic title generation
- Streamlit frontend

---

