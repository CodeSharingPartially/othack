from google.adk.agents import Agent

from opentargets_agent.tools.data_steward_tool import get_target_data_from_opentargets


biologist_agent = Agent(
    model="gemini-2.5-pro",
    name="biologist",
    description="",
    instruction="""
    """,
    tools=[],
    output_key="biologist_report"
)