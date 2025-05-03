<p align="center">
  <img src="docs/logo.png" alt="Nexus Agent" width="200"/>
</p>

# 🚀 Nexus Agent  
### *Multi-Agent Orchestration via MCP & A2A*  
**Top 6 of 57** @ **MCP & A2A Hackathon – AWS Edition** • Creators Corner @ AWS GenAI Loft, SF  

[![Hackathon Finalists!](https://img.shields.io/badge/Top%206-in%2057-orange.svg)](https://lnkd.in/gMKTiyKu)  
[![FastAPI](https://img.shields.io/badge/FastAPI-%5E0.95-green.svg)](https://fastapi.tiangolo.com/)  
[![AWS](https://img.shields.io/badge/AWS-EC2-blue.svg)](https://aws.amazon.com/ec2/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Project Overview

**Nexus Agent** is a cloud-ops automation platform where multiple AI agents collaborate—like a human team—to manage EC2 instances, create JIRA tickets, query RDS order data, and more, all via natural language.

- 🔄 **Agent-to-Agent Workflow** via Model Context Protocol (MCP) & Agent-to-Agent (A2A) bridge  
- ☁️ **AWS Automation**: spin up/down EC2, snapshot backups  
- 🗂️ **Ticketing Integration**: automated JIRA workflows  
- 📊 **Data Queries**: fetch, filter & analyze RDS records  
- 🔍 **IDE-like Observability**: real-time tracing & debugging of agent decisions  

---

## 🏆 Hackathon Highlights

- **Event**: MCP & A2A Hackathon – AWS Edition  
- **Hosts**: Creators Corner @ AWS GenAI Loft  
- **Team Nexus Agent**  
  - **Amrutha Junnuri**
  - Chandini Saisri Uppuganti   
  - Kiran  

> “Nexus Agent pushed the boundaries of multi-agent orchestration—automating cloud operations, ticketing, and data retrieval in a single, conversational UX.”  

📄 Devpost: [bit.ly/devpost-m2](https://lnkd.in/gMKTiyKu)  
▶️ Demo: [youtu.be/g2bduyiW](https://lnkd.in/g2bduyiW)  

---

## 📐 Architecture & Workflow

```mermaid
flowchart LR
  U[User<br/>(Voice / Text)] -->|“Create EC2 t2.micro”| API[FastAPI “/ask”]
  subgraph API Service
    API --> A2AClient[MCP–A2A Client]
    A2AClient -->|POST /a2a_send_task| Bridge[MCP–A2A Bridge]
    Bridge -->|LLM Orchestration| LLM[(Perplexity → Vapi → Mistral)]
    LLM -->|result JSON| Bridge
    Bridge -->|POST /a2a_get_task| A2AClient
    A2AClient -->|Executes Tool Calls| Tools{AWS | JIRA | RDS}
    Tools -->|Responses| API
    API -->|JSON / Audio| UI[Browser UI & Speech]
  end
