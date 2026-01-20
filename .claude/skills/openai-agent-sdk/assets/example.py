# Example: Basic OpenAI Agent with Tools
# This demonstrates the core functionality of the OpenAI Agent SDK

from agents import Agent, function_tool

# Define a simple tool
@function_tool
def get_current_time() -> str:
    """Get the current time."""
    import datetime
    return str(datetime.datetime.now())

@function_tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b

# Create an agent with tools
simple_agent = Agent(
    name="Calculator",
    instructions="You are a helpful calculator assistant. Use the tools available to perform calculations.",
    model="gpt-4o",
    tools=[get_current_time, calculate_sum]
)

# Example usage (this would typically be run in an async context)
async def run_example():
    result = await simple_agent.run(
        messages=[{"role": "user", "content": "What time is it and what is 5 + 3?"}]
    )
    print(result.messages[-1]["content"])

if __name__ == "__main__":
    print("OpenAI Agent SDK example:")
    print("1. Defined tools: get_current_time, calculate_sum")
    print("2. Created agent with tools")
    print("3. Agent is ready to handle requests that require these tools")
    print("\nTo run the full example, call run_example() in an async context")