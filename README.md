<p align="center">
  <img src="images/architecture.png" alt="Architecture Diagram" width="600"/>
</p>

# 🚀 Nexus Agent  
### *Multi-Agent Orchestration via MCP & A2A*  
**Top 6 of 57 ** @ **MCP & A2A Hackathon – AWS Edition** • Creators Corner @ AWS GenAI Loft, SF  

[![Hackathon Finalists!](https://img.shields.io/badge/Top%206-in%2057-orange.svg)](https://lnkd.in/gMKTiyKu)  
[![FastAPI](https://img.shields.io/badge/FastAPI-%5E0.95-green.svg)](https://fastapi.tiangolo.com/)  
[![AWS](https://img.shields.io/badge/AWS-EC2-blue.svg)](https://aws.amazon.com/ec2/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Project Overview

**Nexus Agent** is a conversational cloud-ops platform where multiple AI agents collaborate—like a human team—via the Agent-to-Agent (A2A) protocol and Model Context Protocol (MCP). Users can:

- 🔄 **Delegate workflows** through an A2A/MCP bridge  
- ☁️ **Automate AWS**: launch/terminate EC2, snapshot volumes  
- 🗂️ **Manage Tickets**: create and update JIRA issues  
- 📊 **Query Data**: fetch and filter RDS order records  
- 🔍 **Observe & Debug**: trace agent decisions in real time  

---

## 🏆 Hackathon Highlights

- **Event**: MCP & A2A Hackathon – AWS Edition  
- **Host**: Creators Corner @ AWS GenAI Loft  
- **Team Nexus Agent**  
  - **Amrutha Junnuri** (You!)  
  - Chandini Saisri Uppuganti  
  - Kiran  
> “Nexus Agent pushed the boundaries of multi-agent orchestration—automating cloud operations, ticketing, and data retrieval in a single, conversational UX.”  

📄 Devpost: [bit.ly/devpost-m2](https://lnkd.in/gMKTiyKu)  
▶️ Demo: [youtu.be/g2bduyiW](https://lnkd.in/g2bduyiW)  

---

## 🏗️ Architecture & Workflow

1️⃣ **Client** (Browser UI & Speech)  
2️⃣ **FastAPI** `/ask` endpoint  
3️⃣ **A2A Client** (MCP–A2A SDK in Python)  
4️⃣ **Bridge** (Node MCP‐A2A server on Render)  
5️⃣ **LLM Orchestration** (Perplexity → Vapi → Mistral)  
6️⃣ **Tools** (AWS, JIRA, RDS)  
7️⃣ **Response** back to UI via JSON (or audio in voice mode)

<p align="center">
  <img src="images/architecture.png" alt="Architecture Diagram" width="600"/>
</p>

---

## 🛠️ Sample Interaction

Type or speak:  
> “What is the status of Alva Halajian order?”

<p align="center">
  <img src="images/output1.jpg" alt="Sample Output" width="600"/>
</p>

Backend JSON response:
```json
{
  "customer": "Alva Halajian",
  "order_status": "COMPLETE"
}
