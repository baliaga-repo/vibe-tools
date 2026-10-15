# 🧰 Vibe Tools: Portable Vibe Coding & Agentic MCP Ecosystem

<p align="center">
  <b>A zero-friction, token-efficient developer toolkit for Antigravity IDE and modern AI Agentic workflows.</b>
</p>

<p align="center">
  <a href="README.md">🇮🇩 Baca dalam Bahasa Indonesia</a> •
  <a href="README_EN.md">🇬🇧 Read in English</a>
</p>

---

## 🌟 Overview

**Vibe Tools** is a self-contained, portable suite of automation scripts, Model Context Protocol (MCP) servers, schemas, token-saving guardrails, and agentic skills designed for **Google Antigravity IDE** and modern AI coding environments.

With a single terminal command, Vibe Tools configures a complete, high-performance **Dual-Agent Architecture** in any project without requiring tedious manual setup.

---

## ⚡ 1-Click Quickstart

### Method 1: As a Git Submodule (Recommended)
Add Vibe Tools as a submodule in any project to keep it automatically synchronized:

```bash
# 1. Add the submodule to your project
git submodule add https://github.com/baliaga-repo/vibe-tools.git vibe_tools

# 2. Run the 1-click ecosystem installer
python vibe_tools/setup_vibe_ecosystem.py
```

### Method 2: Standalone / Direct Copy
Simply copy the `vibe_tools/` folder into your project root and run:
```bash
python vibe_tools/setup_vibe_ecosystem.py
```

---

## 🚀 What Happens Automatically in 1 Click?

When you run `setup_vibe_ecosystem.py`, it automatically performs the following:

- [x] **Installs Required Dependencies**: Automatically checks and installs `mcp`, `requests`, `graphifyy`, and Hermes dependencies via `pip`.
- [x] **Configures Antigravity IDE**: Dynamically maps paths in `~/.gemini/config/mcp_config.json` without hardcoded usernames.
- [x] **Installs OpenRouter MCP**: Installs the `openrouter` MCP server (`tanya_openrouter`, `daftar_model_rekomendasi`, `cek_koneksi_openrouter`) supporting Claude Sonnet 4.5, DeepSeek-R1, and custom models.
- [x] **Installs Hermes Agent MCP**: Configures autonomous multi-step subagent delegation (`delegasikan_ke_hermes`).
- [x] **Deploys MCP Schemas**: Installs validated JSON schemas into `~/.gemini/antigravity-ide/mcp/`.
- [x] **Deploys Global Skills**: Deploys the `/graphify` skill to `~/.gemini/config/skills/graphify/SKILL.md`.
- [x] **Synchronizes API Keys**: Auto-detects and synchronizes your `OPENROUTER_API_KEY` across all IDE config files.
- [x] **Predictive Budgeting & Interactive Model Selector**: Deploys `cost_estimator.py` with automatic `ask_question` popups and cost forecasting.
- [x] **Bilingual Token Optimization (English Bridge)**: Translates contexts to dense technical English under the hood to save 30%–50% token cost on BPE tokenizers, presenting results in Indonesian for free.
- [x] **Scaffolds Guardrails & Architecture**: Generates token-efficient rules in `.agents/AGENTS.md`, model confirmation guards, modular skills, workflows, and AST file maps (`.agents/MAP.md`).

---

## 🧠 Dual-Agent Architecture & Bilingual Optimization

Vibe Tools establishes a collaborative dual-agent paradigm:

```mermaid
graph TD
    User([User / Developer]) -->|Indonesian Chat| IDE[Antigravity IDE / Gemini Primary Model]
    IDE -->|Local Heuristic Cost & Token Estimator| CE[cost_estimator.py / ask_question Modal]
    IDE -->|Context Heavy Lifting: Code Review, AST Maps, Precision Edits| Repo[Project Codebase]
    IDE -->|Dense Technical English Bridge - 40% Token Savings| OR[OpenRouter MCP: Claude Sonnet 4.5 / DeepSeek-R1]
    IDE -->|Autonomous Multi-step Problem Solving| Hermes[Hermes Agent MCP]
    OR -->|Concise English Diff / Solution| IDE
    Hermes -->|Subagent Execution Report| IDE
    IDE -->|Free Indonesian Translation & Synthesis| User
```

1. **Primary Model (Gemini / IDE Agent)**: Handles large context lifting, AST tree inspections, CLI executions, log digestion, and precision code editing for FREE.
2. **Deep Reasoning Offload**: Autonomously offloads pure algorithmic problems, root-cause investigations, and architectural decisions to **OpenRouter** (Claude Sonnet 4.5 / DeepSeek-R1) or **Hermes Agent**.
3. **Interactive Budget Guard**: Prompts an interactive modal selector (`ask_question`) with live token & USD cost estimates when no model is explicitly designated.
4. **Bilingual Bridge**: Translates Indonesian prompts into concise technical English before dispatching to external reasoning models, saving 30%–50% in token volume on Byte-Pair Encoding tokenizers.

---

## 📁 Repository Contents

### 🐍 Automation Scripts & MCP Servers
| File | Description |
| :--- | :--- |
| **`setup_vibe_ecosystem.py`** | Master 1-click installer for the entire ecosystem. |
| **`openrouter_mcp.py`** | Dynamic OpenRouter MCP server with smart alias resolution (`r1`, `claude`, `deepseek`, `free`). |
| **`hermes_mcp.py`** | Native bridge server connecting Hermes Agent to Antigravity IDE. |
| **`graphify_sync.py`** | AST code mapping generator and Knowledge Graph synchronization (`--map-only`, `--graph-only`). |
| **`push_to_github.py`** | Safe Git staging, commit, and push utility with file size detection (>50MB/100MB warning). |
| **`install_openrouter_mcp.py`** | Standalone installer for the OpenRouter MCP server. |
| **`install_hermes_antigravity.py`**| Standalone installer for Hermes Agent and bridge tools. |
| **`cost_estimator.py`** | Heuristic token & cost calculator with interactive model selection for Antigravity IDE. |
| **`docstring_translator.py`** | AST-based automated Python docstring translator to bilingual format `[ID]` & `[EN]` (GitHub Actions ready). |
| **`mcp_schemas/`** | Pre-built offline schema files for Antigravity IDE MCP integration. |

### 📚 Documentation & Prompting Guides
| File | Description |
| :--- | :--- |
| **`PANDUAN_SETUP_VIBE_CODING_BARU.md`** | Step-by-step instructions and ready-to-paste prompts for new projects. |
| **`Prompt_AI.md`** | Curated catalog of token-saving prompting patterns (*Progressive Disclosure*, *Targeted Context Tagging*, *Facade Pattern*). |
| **`OPENROUTER_MCP_GUIDE.md`** | Detailed setup guide for OpenRouter models, daily budget limits, and alias mapping. |
| **`PANDUAN_HERMES_ANTIGRAVITY.md`** | Architectural deep-dive on Hermes Agent integration with Antigravity. |
| **`TUTORIAL_TESTING_ASK_QUESTION.md`** | Practical hands-on tutorial and prompt examples for testing the `ask_question` interactive model picker. |

---

## 🔄 Cross-Project Synchronization & Updates

Because `vibe_tools` is managed as a **Git Submodule**, you can edit, push, and sync changes directly from any project you are working on:

### 1. Edit & Push Updates from Any Project
If you improve a prompt, modify an MCP server, or add new scripts inside `vibe_tools/`:
```bash
# Enter the submodule directory
cd vibe_tools

# Push directly to the vibe-tools repository (interactive script or raw git)
python push_to_github.py
# Or manually: git add . && git commit -m "feat: new feature" && git push origin main

# Return to parent project root and update the version pointer
cd ..
git add vibe_tools
git commit -m "chore: update vibe_tools to latest version"
git push
```

### 2. Pull Updates in Another Project (Same PC or Another Machine)
Open a terminal in the root of any other project using `vibe_tools` and run:
```bash
git submodule update --remote --merge
```
*Git will instantly pull the latest commits from the `vibe-tools` repository and merge them into the submodule directory.*

### 3. Clone Projects on a New Computer / Machine
When setting up an existing project on a new computer:
```bash
# Clone the repository along with all submodules automatically
git clone --recurse-submodules <YOUR_PROJECT_REPO_URL>

# If already cloned without --recurse-submodules:
git submodule update --init --recursive
```

### 4. Re-running the Installer (When New Tools / MCPs Are Added)
Whenever an update includes new MCP servers, dependencies, or schemas:
```bash
python vibe_tools/setup_vibe_ecosystem.py
```

---

## 🤝 Contributing

Contributions are very welcome! Whether it's adding new MCP servers, improving prompt templates, optimizing token usage, or refining setup scripts:

1. **Fork** the repository: [github.com/baliaga-repo/vibe-tools](https://github.com/baliaga-repo/vibe-tools)
2. Create a feature branch: `git checkout -b feature/amazing-tool`
3. Commit your changes: `git commit -m "feat: add amazing tool"`
4. Push to your branch: `git push origin feature/amazing-tool`
5. Open a **Pull Request**.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - feel free to use, modify, and distribute it in your own personal and commercial projects.
