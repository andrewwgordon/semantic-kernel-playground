import asyncio
import logging
from os import environ
from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from typing import Annotated
from semantic_kernel.functions import kernel_function


# Plugin class to manage a set of lights and expose control functions to the kernel
class LightsPlugin:
    # List of light devices with their state
    lights = [
        {"id": 1, "name": "Table Lamp", "is_on": False},
        {"id": 2, "name": "Porch light", "is_on": False},
        {"id": 3, "name": "Chandelier", "is_on": True},
    ]

    @kernel_function(
        name="get_lights",
        description="Gets a list of lights and their current state",
    )
    def get_state(
        self,
    ) -> str:
        """
        Returns a list of all lights and their current state.

        Returns:
            str: A list of dictionaries representing each light and its state.
        """
        return self.lights

    @kernel_function(
        name="change_state",
        description="Changes the state of the light",
    )
    def change_state(
        self,
        id: int,
        is_on: bool,
    ) -> str:
        """
        Changes the state (on/off) of the light with the given id.

        Args:
            id (int): The ID of the light to change.
            is_on (bool): The new state for the light (True for on, False for off).

        Returns:
            str: The updated light dictionary if found, otherwise None.
        """
        for light in self.lights:
            if light["id"] == id:
                light["is_on"] = is_on
                return light
        return None


# Main asynchronous function to run the chat-based light control
async def main():
    """
    Main entry point for the chat-based light control assistant.
    Initializes the kernel, sets up the OpenAI chat completion service, registers plugins,
    and starts a chat loop to interact with the user for controlling lights.
    """
    # Initialize the kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completion service to the kernel
    chat_completion = OpenAIChatCompletion(
        ai_model_id="gpt-4.1-mini", api_key=environ["OPENAI_API_KEY"]
    )
    kernel.add_service(chat_completion)

    # Set up logging for the kernel at DEBUG level
    setup_logging()
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Register the LightsPlugin with the kernel under the name "Lights"
    kernel.add_plugin(
        LightsPlugin(),
        plugin_name="Lights",
    )

    # Enable planning and set function choice behavior to automatic
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create a chat history object to store the conversation
    history = ChatHistory()

    # Start a chat loop with the user
    userInput = None
    while True:
        # Collect user input from the console
        userInput = input("User > ")

        # Exit the loop if the user types "exit"
        if userInput == "exit":
            break

        # Add the user's message to the chat history
        history.add_user_message(userInput)

        # Get the AI's response using the chat completion service
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        # Print the AI's response to the console
        print("Assistant > " + str(result))

        # Add the AI's message to the chat history
        history.add_message(result)


# Run the main function if this script is executed directly
if __name__ == "__main__":
    asyncio.run(main())
