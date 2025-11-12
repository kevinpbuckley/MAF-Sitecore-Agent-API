import asyncio
import json
import os
import logging
import requests
from typing import get_type_hints
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIChatClient
from azure.core.credentials import AzureKeyCredential

logging.basicConfig(level=logging.ERROR)
load_dotenv()

class SitecoreAPI:
    def __init__(self):
        self.token = self._get_token()
        self.base_url = "https://edge-platform.sitecorecloud.io/stream/ai-agent-api"
        
    def _get_token(self):
        client_id = os.getenv('SITECORE_CLIENT_ID')
        client_secret = os.getenv('SITECORE_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            raise Exception("SITECORE_CLIENT_ID and SITECORE_CLIENT_SECRET must be set in .env")
        
        response = requests.post(
            'https://auth.sitecorecloud.io/oauth/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'client_credentials',
                'audience': 'https://api.sitecorecloud.io'
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Auth failed: {response.status_code} - {response.text}")
        
        return response.json()['access_token']
    
    def call_api(self, method, path, **kwargs):
        headers = {'Authorization': f'Bearer {self.token}'}
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, headers=headers, **kwargs)
        
        if response.status_code != 200:
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
        
        return response.json()

def create_tools_from_spec():
    spec_url = "https://api-docs.sitecore.com/_spec/ai-capabilities/agent-api/index.json?download"
    
    try:
        response = requests.get(spec_url)
        response.raise_for_status()
        spec = response.json()
    except Exception as e:
        print(f"Warning: Failed to download spec, using local index.json: {e}")
        with open('index.json', 'r') as f:
            spec = json.load(f)
    
    api = SitecoreAPI()
    tools = []
    
    for path, methods in spec['paths'].items():
        for method, operation in methods.items():
            if not isinstance(operation, dict) or 'operationId' not in operation:
                continue
            
            op_id = operation['operationId']
            summary = operation.get('summary', '')
            
            def make_tool(p=path, m=method.upper(), desc=summary):
                def tool(**kwargs):
                    try:
                        full_path = p
                        for key, value in kwargs.items():
                            full_path = full_path.replace(f'{{{key}}}', str(value))
                        
                        result = api.call_api(m, full_path)
                        return json.dumps(result, indent=2)
                    except Exception as e:
                        return f"Error: {str(e)}"
                
                tool.__name__ = op_id.replace('-', '_')
                tool.__doc__ = desc
                return tool
            
            tools.append(make_tool())
    
    return tools

async def main():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT").split('/openai')[0]
    
    tools = create_tools_from_spec()
    
    agent = AzureOpenAIChatClient(
        credential=AzureKeyCredential(os.getenv("AZURE_OPENAI_API_KEY")),
        endpoint=endpoint,
        deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    ).create_agent(
        instructions="You are a Sitecore assistant. Use the available tools to help users. Be concise.",
        tools=tools
    )
    
    print("Sitecore Agent (type 'exit' to quit)")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
                
            result = await agent.run(user_input)
            print(result.text)
        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":
    asyncio.run(main())
