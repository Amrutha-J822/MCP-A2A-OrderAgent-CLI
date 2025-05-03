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

**🧠 AI Customer Order Agent** is a part of it where we can anything about your customers' orders in natural language—by voice or text—and instantly get the latest status, totals, dates, or any other field you need. Features are:
- 🔄**Voice & Text Input**  
  Leverage the Web Speech API for seamless "click-to-talk" queries, or type any question in the browser.
- 🗂️**Multi-LLM Extraction**  
  First tries your custom MCP–A2A bridge (Perplexity/Vapi.ai agent under the hood), then falls back to Mistral if needed.
- 🔍**Dynamic Field Lookup**  
    Your query can ask for **any** column—status, total, rating, items, address, etc.—and the agent will map your phrasing to the correct database field.
- 📊**AWS RDS Integration**  
  Safely fetches your customer_orders from a managed PostgreSQL instance.
- ☁️**Cloud-native Deployment**  
    Two Render web services—one for the **MCP–A2A bridge**, one for the **FastAPI app**—guarantee zero-downtime, public HTTPS endpoints, and automatic rebuilds on git push.
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
---

## 🧩 Components

### 1. AWS EC2 Manager  
Create/terminate EC2 instances via natural language.

**Tools:**  
- `initiate_ec2_instance`  
- `terminate_ec2_instance`  

### 2. Order Status Manager  
Query and update customer order status in AWS RDS.

**Tools:**  
- `get_order_status`  
- `list_all_orders`  
- `update_order_status`  

### 3. JIRA Ticket Assistant  
Simulate ticket creation, comments, and status updates.

**Tools:**  
- `create_jira_ticket`  
- `update_jira_ticket`  

### 4. AWS Advisor via Perplexity  
Get cloud advice via LLMs with fallback (Perplexity → Mistral).

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+  
- AWS account with EC2 permissions  
- PostgreSQL instance (RDS)  
- Perplexity API Key  
- Vapi.ai API Key  

### Environment Setup

1. Clone the repo:
```bash
git clone https://github.com/Amrutha-J822/MCP-A2A-OrderAgent-CLI.git
cd MCP-A2A-OrderAgent-CLI
