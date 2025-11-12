# Sitecore Agent API with Microsoft Agent Framework

Sample project demonstrating how to use the Microsoft Agent Framework with the Sitecore Agent API using OpenAPI specifications.

## Features

- Automatically generates function tools from Sitecore Agent API OpenAPI spec
- Downloads latest API spec on each run
- OAuth 2.0 authentication with Sitecore Cloud
- Interactive chat interface for Sitecore operations
- All 39 Sitecore API operations available (Sites, Pages, Content, Components, Assets, Jobs, etc.)

## Prerequisites

- Python 3.13+
- Azure OpenAI account with deployment
- Sitecore XM Cloud instance
- Sitecore automation client credentials

## Setup

1. Clone the repository:
```bash
git clone https://github.com/kevinpbuckley/MAF-Sitecore-Agent-API.git
cd MAF-Sitecore-Agent-API
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from sample:
```bash
cp .env.sample .env
```

4. Configure your environment variables in `.env`:
   - Azure OpenAI credentials
   - Sitecore client ID and secret (from XM Cloud Deploy automation credentials)

## Sitecore Credentials Setup

1. Go to Sitecore Cloud Portal
2. Open XM Cloud Deploy
3. Navigate to **Credentials** > **Environment** > **Create credentials** > **Automation**
4. Copy the client ID and client secret to your `.env` file

## Usage

Run the interactive agent:
```bash
python sitecore_agent.py
```

Example commands:
- "list sites"
- "show pages for nextjs-skate-park site"
- "get site details for alaris"
- "search for content items"

Type `exit` or `quit` to stop.

## How It Works

The agent automatically:
1. Downloads the latest Sitecore Agent API OpenAPI spec
2. Generates Python function tools for all 39 operations
3. Authenticates with Sitecore using OAuth 2.0
4. Uses Azure OpenAI to understand natural language commands
5. Calls appropriate Sitecore API operations based on user intent

## Available Operations

- **Sites**: List sites, get site details, list pages, get site ID from item
- **Pages**: Create pages, add languages, add components, search, get HTML/screenshots
- **Content**: Create, read, update, delete content items
- **Components**: List components, create datasources, search datasources
- **Assets**: Upload, search, get info, update metadata
- **Environments**: Get available languages
- **Personalization**: Create personalized variants
- **Jobs**: View job details, revert operations

## Project Structure

```
MAF-Sitecore-Agent-API/
├── sitecore_agent.py       # Main agent implementation
├── tutorial1.py            # Basic agent operations tutorial
├── tutorial2.py            # Image analysis tutorial
├── tutorial3.py            # Multi-turn conversations tutorial
├── tutorial4.py            # Function tools tutorial
├── tutorial4-sitecore.py   # Sitecore OpenAPI tutorial
├── index.json              # Cached OpenAPI spec (auto-updated)
├── requirements.txt        # Python dependencies
├── .env.sample             # Environment variables template
└── README.md               # This file
```

## Tutorials

The project includes several tutorials demonstrating Microsoft Agent Framework features:

- **tutorial1.py**: Basic agent operations (run, stream, ChatMessage)
- **tutorial2.py**: Image analysis with vision models
- **tutorial3.py**: Multi-turn conversations with threads
- **tutorial4.py**: Function tools (simple, decorated, class-based)
- **tutorial4-sitecore.py**: OpenAPI specification tools overview

Run any tutorial:
```bash
python tutorial1.py
```

## License

MIT

## Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [Sitecore Agent API Documentation](https://api-docs.sitecore.com/ai-capabilities/agent-api)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
