# semantic-kernel-playground

## Overview

This project is a playground for experimenting with the Microsoft Semantic Kernel, an SDK that enables integration of AI models, plugins, and planning capabilities into Python applications. The main goal is to demonstrate how to use Semantic Kernel to build an interactive, AI-powered assistant that can control a set of smart lights through a conversational interface.

## Goals
- Showcase the integration of Microsoft Semantic Kernel with OpenAI's GPT models.
- Demonstrate how to expose custom Python functions (plugins) to the AI for dynamic control of application logic.
- Provide a simple, extensible example for building chat-based assistants that can interact with real or simulated devices.

## Use of Microsoft Semantic Kernel
- **Kernel**: The core orchestrator that manages plugins, services, and execution flow.
- **Plugins**: Custom Python classes (e.g., `LightsPlugin`) that expose functions to the AI, allowing it to interact with application logic.
- **OpenAIChatCompletion**: Connects the kernel to OpenAI's GPT models for natural language understanding and response generation.
- **FunctionChoiceBehavior**: Enables the AI to automatically select and invoke available functions based on user input.
- **ChatHistory**: Maintains the conversation context between the user and the assistant.

## How the Code Works
1. **Plugin Definition**: The `LightsPlugin` class defines a set of light devices and exposes two functions:
   - `get_lights`: Returns the current state of all lights.
   - `change_state`: Changes the state (on/off) of a specific light by ID.
   These functions are decorated with `@kernel_function`, making them available to the AI.

2. **Kernel Initialization**: The main function initializes the Semantic Kernel, adds the OpenAI chat completion service, and registers the `LightsPlugin`.

3. **Chat Loop**: The program enters a loop where it accepts user input from the console. Each message is added to the chat history.

4. **AI Response**: The kernel uses the OpenAI model to generate a response. If the user's message matches a function signature (e.g., asking to turn on a light), the AI can invoke the corresponding plugin function automatically.

5. **Conversation Management**: The assistant's responses are printed to the console and added to the chat history, maintaining context for future interactions.

6. **Exit**: Typing `exit` ends the chat session.

---

## Installation and Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management. Make sure you have Python 3.9+ and uv installed.

### 1. Install uv

If you don't have uv, install it with:

```bash
pip install uv
```

### 2. Install dependencies

From the project root directory, run:

```bash
uv pip install -r requirements.txt
```

Or, if you are using a `pyproject.toml` (recommended):

```bash
uv pip install -r uv.lock
```

### 3. Set up environment variables

You need an OpenAI API key. Set it in your environment:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

You can add this line to your `.env` or shell profile for convenience.

---

## Running the Program

To start the chat assistant, run:

```bash
uv pip install .  # (if you want to install as a package, optional)
uv python main.py
```

You will see a prompt:

```
User >
```

Type your commands (e.g., "Turn on the table lamp"), and the assistant will respond. Type `exit` to quit.

---

This playground can be extended with additional plugins, services, or more complex device logic to explore the full capabilities of Microsoft Semantic Kernel in building intelligent, interactive applications.
