# Faculty Advisor Agentic System - Core Framework

This document describes the core framework structure and components for the Faculty Advisor Agentic System.

## Project Structure

```
├── core/                           # Core framework components
│   ├── __init__.py                # Main exports
│   ├── config.py                  # Configuration management
│   ├── base/                      # Base classes
│   │   ├── __init__.py
│   │   └── agent.py              # BaseAgent class and AgentFactory
│   ├── models/                    # Data models
│   │   ├── __init__.py
│   │   └── agent_models.py       # Agent communication models
│   └── services/                  # Shared services
│       ├── __init__.py
│       ├── container.py          # Dependency injection container
│       ├── memory.py             # Memory management system
│       ├── tools.py              # Tool registry and execution
│       ├── reasoning.py          # LLM reasoning engine
│       └── persona.py            # Agent persona management
├── agents/                        # Agent implementations
│   ├── __init__.py
│   ├── orchestrator/             # Orchestrator agent
│   ├── solution_advisory/        # Solution Advisory agent
│   ├── leave_management/         # Leave Management agent
│   ├── monitoring/               # Monitoring agent
│   └── communications/           # Communications agent
├── config.yaml                   # System configuration
└── test_framework.py             # Framework test script
```

## Core Components

### 1. BaseAgent Class

The `BaseAgent` class provides a standardized processing pipeline for all agents:

- **Initialization**: Sets up persona, memory, tools, and reasoning components
- **Processing Pipeline**: Validates requests, retrieves context, applies reasoning, executes actions, and generates responses
- **Memory Integration**: Automatically stores interactions and retrieves context
- **Error Handling**: Provides consistent error handling and logging
- **Health Monitoring**: Tracks performance metrics and status

### 2. Data Models

#### AgentConfig
Configuration model for agent initialization with persona, memory, tools, and LLM settings.

#### AgentRequest
Standard request format containing student ID, session ID, query, context, and metadata.

#### AgentResponse
Standard response format with content, confidence, processing time, and error handling.

### 3. Service Components

#### Memory System
- **Short-term Memory**: Redis-based session storage for conversational context
- **Long-term Memory**: PostgreSQL-based persistent storage for conversation summaries
- **Context Retrieval**: Intelligent context building for agent requests

#### Tool Registry
- **Tool Management**: Registration and execution of agent tools
- **Schema Definition**: Standardized tool parameter schemas
- **Error Handling**: Consistent tool execution error handling

#### Reasoning Engine
- **LLM Integration**: Ollama integration for reasoning and decision making
- **Multi-step Reasoning**: Structured reasoning process with confidence scoring
- **Action Planning**: Determines required tool actions based on requests

#### Persona Manager
- **Behavioral Configuration**: Defines agent personality and communication style
- **Response Formatting**: Applies persona-specific response formatting
- **System Prompts**: Generates LLM system prompts based on persona

### 4. Dependency Injection Container

The DI container manages service lifecycles and dependencies:

- **Singleton Services**: Shared instances across the application
- **Scoped Services**: Per-request or per-session instances
- **Transient Services**: New instances for each resolution
- **Automatic Dependency Resolution**: Constructor injection based on type hints

## Configuration

The system uses a hierarchical configuration approach:

1. **Default Configuration**: Built-in defaults in code
2. **YAML Configuration**: `config.yaml` file settings
3. **Environment Variables**: Runtime overrides

### Key Configuration Sections

- **System Settings**: Environment, debug mode, logging
- **Database**: PostgreSQL connection settings
- **Redis**: Session storage and short-term memory
- **LLM**: Ollama model configuration
- **Agent-Specific**: Per-agent customization

## Usage Example

```python
import asyncio
from core import BaseAgent, AgentFactory, AgentConfig, AgentType

# Create agent configuration
config = AgentConfig(
    agent_type=AgentType.SOLUTION_ADVISORY,
    agent_id="advisor-001",
    name="Academic Advisor",
    description="Provides academic guidance",
    persona={
        "name": "Dr. Smith",
        "role": "Senior Academic Advisor",
        "personality_traits": ["helpful", "knowledgeable"]
    }
)

# Create and initialize agent
agent = AgentFactory.create_agent(config)
await agent.initialize()

# Process request
request = AgentRequest(
    request_id="req-001",
    student_id="STU001",
    session_id="sess-001",
    query="How can I improve my CGPA?"
)

response = await agent.process(request)
print(response.content)
```

## Testing

Run the framework test to verify functionality:

```bash
python test_framework.py
```

This test creates a simple agent, processes a request, and verifies the response pipeline.

## Next Steps

With the core framework in place, the next tasks involve:

1. **Authentication System**: Implement JWT-based authentication with @amrita.edu validation
2. **Database Schema**: Set up PostgreSQL with student data models
3. **Agent Implementations**: Create specific agent classes extending BaseAgent
4. **RAG System**: Implement agentic RAG for Solution Advisory Agent
5. **API Layer**: Create FastAPI endpoints for agent communication

## Requirements Satisfied

This implementation satisfies the following requirements from the specification:

- **Requirement 1.1**: Multi-agent architecture with distinct agents
- **Requirement 1.2**: Inter-agent communication through standardized interfaces
- **Requirement 1.3**: Modular design allowing independent agent updates
- **Requirement 1.4**: Agent registration and discovery system (via AgentFactory)

The framework provides a solid foundation for building the complete Faculty Advisor Agentic System.