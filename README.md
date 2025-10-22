#  Google multiagents

https://github.com/google/adk-samples

https://google.github.io/adk-docs/get-started/quickstart/


```sh
# Create
python -m venv .venv
# Activate (each new terminal)
# macOS/Linux: source .venv/bin/activate
# Windows CMD: .venv\Scripts\activate.bat
# Windows PowerShell: .venv\Scripts\Activate.ps1

pip install google-adk


```

You need to create this structure:

    parent_folder/
        multi_tool_agent/
            __init__.py
            agent.py
            .env

            
Create the folder 

    mkdir multi_tool_agent/




You can run it :

    adk run my_agent
    # or
    adk web --port 8000 my_agent