# 🚀 Loop Engineering Projects

A hands-on collection of **Loop Engineering projects** completed as part of the **Panaversity Loop Engineering Crash Course**.

The goal of these projects is to learn how to build reliable AI-assisted workflows using **loops, verification, retries, automation, and measurable feedback** instead of simply asking an AI agent to complete a task once.

## 📚 About the Course

These projects are based on the **Loop Engineering Crash Course by Panaversity**.

The course focuses on a practical idea:

> **Don't just ask an AI agent to do a task — build a loop that can check, improve, and retry the work until the desired result is achieved.**

## 🛠️ Projects

This repository contains **8 hands-on Loop Engineering projects**, progressing from simple monitoring loops to more advanced autonomous workflows.

| # | Project                     | Main Concept                                     |
| - | --------------------------- | ------------------------------------------------ |
| 1 | Watch Loop                  | Monitoring a long-running task                   |
| 2 | Tests-Pass Loop             | Automated verification and retry                 |
| 3 | Morning Brief               | Repeated task execution and validation           |
| 4 | Maker-Checker Loop          | Separate creation and verification               |
| 5 | Fix-Batch Loop              | Handling multiple fixes efficiently              |
| 6 | Event-Driven PR Review      | GitHub Actions and automated review              |
| 7 | Cost & Silent Failure Audit | Measuring real cost and detecting failures       |
| 8 | Real Work Audit             | Building a complete loop with real audit history |

## 🔁 What I Learned

Through these projects, I practiced:

* 🔄 Designing effective AI loops
* ✅ Verification and validation
* 🧪 Test-driven workflows
* 🔁 Retry and recovery strategies
* 👀 Maker-checker patterns
* ⚙️ Automation with shell scripts
* 🤖 AI-assisted development
* 📊 Measuring cost and performance
* 📝 Maintaining audit history
* 🚦 Handling failures instead of blindly trusting AI output

## 🧠 Core Loop

A typical Loop Engineering workflow can be represented as:

```text
        ┌───────────────┐
        │   Give Task   │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │   AI Acts     │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │    Verify     │
        └───────┬───────┘
                ↓
          ┌─────┴─────┐
          │           │
        PASS         FAIL
          │           │
          ↓           ↓
       Finish       Retry
                      │
                      └──────→ AI Acts
```

The important part is the **verification step**. An AI agent should not automatically be considered successful just because it produced an output.

## 🧰 Technologies & Tools

* **Git & GitHub**
* **Shell / Bash scripting**
* **Python**
* **GitHub Actions**
* **Claude Code**
* **OpenCode**
* AI-assisted development workflows

## 📂 Repository Structure

```text
Loop-Engineering-Projects/
│
├── project-1/
├── project-2/
├── project-3/
├── project-4/
├── project-5/
├── project-6/
├── project-7/
├── project-8/
│
└── README.md
```

## 🎯 Learning Objective

The purpose of this repository is not just to complete coding tasks, but to understand how **AI agents can be placed inside reliable engineering loops**.

The projects demonstrate how to:

**Act → Check → Learn → Retry → Complete**

rather than:

**Ask AI → Trust Output → Done**

---

### 👩‍💻 Author

**Yusra Anum**

Student & AI/Software Development Learner

### 🌐 Learning Journey

This repository is part of my hands-on learning journey through **Panaversity's AI and software engineering programs**.

⭐ If you're learning Loop Engineering too, feel free to explore the projects and experiment with the workflows.
