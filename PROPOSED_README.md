# TorrentScout-qBittorrent-Search-Plugin-Suite

![TorrentScout Logo](https://img.shields.io/badge/TorrentScout-Search%20Plugin%20Suite-blue?style=for-the-badge&logo=qbittorrent&logoColor=white)

[![Build Status](https://github.com/chirag127/TorrentScout-qBittorrent-Search-Plugin-Suite/actions/workflows/ci.yml/badge.svg)](https://github.com/chirag127/TorrentScout-qBittorrent-Search-Plugin-Suite/actions/workflows/ci.yml) [![Code Coverage](https://codecov.io/gh/chirag127/TorrentScout-qBittorrent-Search-Plugin-Suite/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/chirag127/TorrentScout-qBittorrent-Search-Plugin-Suite) [![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![Package Manager](https://img.shields.io/badge/Package%20Manager-uv-blueviolet?style=flat-square&logo=git&logoColor=white)](https://github.com/astral-sh/uv) [![Linter/Formatter](https://img.shields.io/badge/Linter%2FFlatter-Ruff-black?style=flat-square&logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/) [![Tests](https://img.shields.io/badge/Tests-Pytest-success?style=flat-square&logo=pytest&logoColor=white)](https://docs.pytest.org/) [![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey?style=flat-square)](https://creativecommons.org/licenses/by-nc/4.0/) [![GitHub Stars](https://img.shields.io/github/stars/chirag127/TorrentScout-qBittorrent-Search-Plugin-Suite?style=flat-square)](https://github.com/chirag127/TorrentScout-qBittorrent-Search-Plugin-Suite/stargazers)


**Star ⭐ this Repo** to support our mission of advanced torrent discovery!

TorrentScout is a high-performance, Python-based suite of search plugins for qBittorrent, engineered to seamlessly integrate with popular torrent search engines. It significantly enhances your content discovery experience by providing robust, efficient, and automated access to a vast array of torrent sources directly within your qBittorrent client.

## ARCHITECTURE

TorrentScout employs a modular plugin architecture, designed for extensibility and maintainability. Each torrent search engine integration is encapsulated within its own independent module, making it easy to add new sources or update existing ones without impacting the core system.

mermaid
graph TD
    A[qBittorrent Client] --> B(TorrentScout CLI/API)
    B --> C{Plugin Manager}
    C --> D[Search Plugin: Engine A]
    C --> E[Search Plugin: Engine B]
    C --> F[Search Plugin: Engine N]
    D --&gt; G[External Torrent Search Engine A]
    E --&gt; H[External Torrent Search Engine B]
    F --&gt; I[External Torrent Search Engine N]
    G --&gt;|Results| D
    H --&gt;|Results| E
    I --&gt;|Results| F
    D --&gt;|Formatted Results| C
    E --&gt;|Formatted Results| C
    F --&gt;|Formatted Results| C
    C --&gt;|Aggregated Results| B
    B --&gt; J[qBittorrent Search Tab]

    subgraph TorrentScout Core
        B
        C
    end

    subgraph TorrentScout Plugins
        D
        E
        F
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#f9f,stroke:#333,stroke-width:2px


## TABLE OF CONTENTS

*   [ARCHITECTURE](#architecture)
*   [🤖 AI AGENT DIRECTIVES](#-ai-agent-directives)
*   [FEATURES](#features)
*   [INSTALLATION](#installation)
*   [USAGE](#usage)
    *   [CLI Commands](#cli-commands)
    *   [Integrating with qBittorrent](#integrating-with-qbittorrent)
*   [DEVELOPMENT STANDARDS](#development-standards)
    *   [Setup](#setup)
    *   [Scripts](#scripts)
    *   [Principles](#principles)
*   [CONTRIBUTING](#contributing)
*   [LICENSE](#license)
*   [SECURITY](#security)


<details>
<summary><b>🤖 AI AGENT DIRECTIVES: APEX PROTOCOL (DECEMBER 2025 EDITION)</b></summary>

# SYSTEM: APEX TECHNICAL AUTHORITY & ELITE ARCHITECT

## 1. IDENTITY & PRIME DIRECTIVE
**Role:** You are a Senior Principal Software Architect and Master Technical Copywriter with **40+ years of elite industry experience**. You operate with absolute precision, enforcing FAANG-level standards and the wisdom of "Managing the Unmanageable."
**Context:** Current Date is **December 2025**. You are building for the 2026 standard.
**Output Standard:** Deliver **EXECUTION-ONLY** results. No plans, no "reporting"—only executed code, updated docs, and applied fixes.
**Philosophy:** "Zero-Defect, High-Velocity, Future-Proof."

---

## 2. INPUT PROCESSING & COGNITION
*   **SPEECH-TO-TEXT INTERPRETATION PROTOCOL:**
    *   **Context:** User inputs may contain phonetic errors (homophones, typos).
    *   **Semantic Correction:** **STRICTLY FORBIDDEN** from executing literal typos. You must **INFER** technical intent based on the project context.
    *   **Logic Anchor:** Treat the `README.md` as the **Single Source of Truth (SSOT)**.
*   **MANDATORY MCP INSTRUMENTATION:**
    *   **No Guessing:** Do not hallucinate APIs.
    *   **Research First:** Use `linkup`/`brave` to search for **December 2025 Industry Standards**, **Security Threats**, and **2026 UI Trends**.
    *   **Validation:** Use `docfork` to verify *every* external API signature.
    *   **Reasoning:** Engage `clear-thought-two` to architect complex flows *before* writing code.

---

## 3. CONTEXT-AWARE APEX TECH STACKS (LATE 2025 STANDARDS)
**Directives:** Detect the project type (`pyproject.toml` for Python) and apply the corresponding **Apex Toolchain**. This repository, `TorrentScout-qBittorrent-Search-Plugin-Suite`, is a Python-based suite of qBittorrent search plugins.

*   **PRIMARY SCENARIO: DATA / SCRIPTS / AUTOMATION (Python)**
    *   **Stack:** This project leverages **Python 3.10+**. Key tools include **uv** (for package management and dependency resolution), **Ruff** (for ultra-fast linting and formatting), and **Pytest** (for robust unit and integration testing).
    *   **Architecture:** Adheres to a **Modular Plugin Architecture**, where each search engine integration is an independent, discoverable module. The core provides robust plugin management, asynchronous execution, and a standardized interface for qBittorrent integration. Prioritize clear module boundaries, efficient resource usage, and resilient error handling for external API interactions (torrent sites).
    *   **CLI Framework:** Uses `Click` or similar for managing plugins and performing manual searches.

*   **SECONDARY SCENARIO A: WEB / APP / EXTENSION (TypeScript) - *Not applicable for this project's primary function. Reference only for potential future web-based extensions.***
    *   **Stack:** TypeScript 6.x (Strict), Vite 7 (Rolldown), Tauri v2.x (Native), WXT (Extensions).
    *   **State:** Signals (Standardized).

## 4. ARCHITECTURAL PRINCIPLES
*   **SOLID Principles:** Ensure Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion throughout the codebase.
*   **DRY (Don't Repeat Yourself):** Abstract common functionalities, especially for API interactions and response parsing.
*   **YAGNI (You Aren't Gonna Need It):** Implement only what is necessary for the current scope. Avoid over-engineering.
*   **Modularity & Extensibility:** Design for easy addition of new search engine plugins without modifying core components.
*   **Asynchronous Operations:** Utilize Python's `asyncio` for non-blocking I/O operations with web scraping and API calls to maintain responsiveness.

## 5. VERIFICATION & QUALITY ASSURANCE PROTOCOL
*   **Linting & Formatting:** `uv run ruff check .` and `uv run ruff format .` must pass with zero errors.
*   **Testing:** `uv run pytest` must execute all unit and integration tests successfully, achieving a minimum of 90% code coverage.
*   **Security Scans:** Integrate `bandit` for static analysis and `safety` for dependency vulnerability checks in CI/CD pipelines.
*   **Performance:** Profile critical sections (e.g., plugin execution, search result parsing) to ensure optimal speed and minimal resource consumption.

## 6. DEVELOPMENT WORKFLOW
*   **Feature Branches:** All new features or bug fixes must be developed in dedicated branches.
*   **Pull Requests:** Require at least one approving review before merging to `main`.
*   **Conventional Commits:** Adhere to the Conventional Commits specification for clear commit history.
*   **Semantic Versioning:** Follow SemVer 2.0.0 for all releases.

</details>

## FEATURES

*   **Extensible Plugin System:** Easily add or remove search engine plugins.
*   **High-Performance Search:** Utilizes asynchronous programming for rapid query execution.
*   **Seamless qBittorrent Integration:** Designed to work flawlessly with qBittorrent's native search functionality.
*   **Customizable Sources:** Configure which torrent engines to use for your searches.
*   **Robust Error Handling:** Gracefully manages network issues and parsing errors from external sources.
*   **CLI Interface:** For direct interaction, testing, and management of plugins.

## INSTALLATION

To get TorrentScout up and running, follow these steps:

1.  **Clone the Repository:**

    bash
    git clone https://github.com/chirag127/TorrentScout-qBittorrent-Search-Plugin-Suite.git
    cd TorrentScout-qBittorrent-Search-Plugin-Suite
    

2.  **Install `uv` (if you don't have it):**

    bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Ensure uv is in your PATH. For example, add to ~/.bashrc or ~/.zshrc:
    # export PATH="$HOME/.cargo/bin:$PATH"
    

3.  **Install Dependencies:**

    bash
    uv sync
    

## USAGE

### CLI Commands

TorrentScout provides a command-line interface for managing plugins and performing searches.

*   **List Available Plugins:**

    bash
    uv run python -m torrentscout --list-plugins
    

*   **Perform a Search:**

    bash
    uv run python -m torrentscout --search "your search query here"
    

*   **Enable/Disable Plugins (Example):**

    bash
    uv run python -m torrentscout --enable-plugin my_favorite_engine
    uv run python -m torrentscout --disable-plugin unwanted_engine
    

### Integrating with qBittorrent

1.  **Configure qBittorrent:**
    *   Open qBittorrent and navigate to `Tools > Search Engine`.
    *   Click `Search plugins...` and then `Install a new one`.
    *   Browse to the `src/torrentscout/` directory within your cloned repository and select the main plugin file (e.g., `torrentscout_plugin.py` or similar entry point).
    *   *Detailed instructions on creating the qBittorrent-compatible plugin file will be provided in the `docs/` directory.*

2.  **Run TorrentScout as a background service (Recommended for production):**
    *   For continuous operation, it's recommended to run TorrentScout as a background process or service that qBittorrent can communicate with. Examples for `systemd` or `Docker` will be provided.

## DEVELOPMENT STANDARDS

### Setup

1.  **Clone the repository:**
    bash
    git clone https://github.com/chirag127/TorrentScout-qBittorrent-Search-Plugin-Suite.git
    cd TorrentScout-qBittorrent-Search-Plugin-Suite
    
2.  **Install dependencies and create virtual environment:**
    bash
    uv sync
    

### Scripts

Utilize `uv run` for executing development scripts defined in `pyproject.toml`.

*   **Run tests:**
    bash
    uv run pytest
    
*   **Check linting and formatting:**
    bash
    uv run ruff check .
    
*   **Automatically format code:**
    bash
    uv run ruff format .
    
*   **Run a specific plugin (for testing):**
    bash
    uv run python -m torrentscout --search "test query" --only-plugin specific_engine
    

### Principles

Our development adheres to the following core software engineering principles:

*   **SOLID Principles:** Ensuring maintainable, flexible, and understandable code.
*   **DRY (Don't Repeat Yourself):** Promoting reusability and reducing redundancy.
*   **YAGNI (You Aren't Gonna Need It):** Focusing on immediate needs and avoiding premature optimization or complexity.
*   **Clean Architecture:** Maintaining clear separation of concerns between core logic, plugin interfaces, and external integrations.

## CONTRIBUTING

We welcome contributions to TorrentScout! Please refer to our [CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed guidelines on how to submit pull requests, report bugs, and suggest features.

## LICENSE

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License](LICENSE).

## SECURITY

For information on security vulnerabilities and how to report them, please review our [SECURITY.md](.github/SECURITY.md) policy.