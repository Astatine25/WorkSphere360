# 🤖 AI-Powered Employee Leave Management System (RPGLE + AI)

An enterprise-grade **Employee Leave Management System** built on  
**IBM i (AS/400)** using **RPG IV (ILE RPG)** and **DB2**, enhanced with a
**multi-agent AI decision support layer** for intelligent leave planning,
conflict detection, and workload optimization.

This project modernizes a legacy HR system by **overlaying AI intelligence**
without replacing existing IBM i infrastructure.

---

## 📌 Key Features

### 👩‍💼 Employee
- Apply leave & comp-off
- View leave balance and status
- Get AI-recommended best leave dates

### 👨‍💼 Manager
- Approve / reject leave
- View team availability
- AI-based risk score & workload impact
- Suggested alternative leave dates

### 🛠 Admin
- Employee & role management
- Holiday calendar maintenance
- System configuration

### 🤖 AI Capabilities
- Leave conflict detection
- Team availability calculation
- Approval probability prediction
- Workload & burnout risk analysis
- Explainable recommendations

---

## 🧠 System Architecture

The system follows a **hybrid architecture**:

- **Core System:** IBM i (RPGLE + DB2)
- **AI Layer:** External AI Agent (Python / ML / LLM)
- **Integration:** REST-based AI Bridge

---

## 🏗 High-Level Architecture Diagram

```mermaid
flowchart LR
    EmployeeUI --> RPGApp
    ManagerUI --> RPGApp
    AdminUI --> RPGApp

    RPGApp --> DB2[(DB2 Physical Files)]
    RPGApp --> AIBridge

    AIBridge --> AIEngine
    AIEngine --> AIBridge

    DB2 --> AIEngine
