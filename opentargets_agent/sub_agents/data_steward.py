from google.adk.agents import Agent

from opentargets_agent.tools.data_steward_tool import get_target_data_from_opentargets


data_steward_agent = Agent(
    model="gemini-2.5-pro",
    name="data_steward",
    description="",
    instruction="""
    """,
    tools=[get_target_data_from_opentargets],
    output_key="target_data"
)