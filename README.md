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

To run it locally:
```sh
adk web 
```

To deploy it to Google Cloud:
```sh
gcloud auth login

# Change the service_name to your own
adk deploy cloud_run --project=opentargets-hack25cam-309 --region=europe-west1 --service_name=paultestservice --app_name=opentargets-agent --with_ui ./
```

For Windows user, due to the bug in ADK, you need to use WSL. Also gcloud is the only way to authenticate, the API key simply does not work.
