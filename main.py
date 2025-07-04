"""
semantic-kernel-playground

This module demonstrates the use of Microsoft Semantic Kernel to build a chat-based assistant that can control a set of smart lights.

Features:
- Defines a plugin (`LightsPlugin`) to manage and control light devices.
- Integrates with OpenAI's GPT models for natural language understanding.
- Exposes plugin functions to the AI for dynamic invocation based on user input.
- Maintains chat history and context for interactive conversations.

Run this script to start a console-based assistant that can turn lights on/off and report their status using natural language commands.
"""
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
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

# Plugin class to manage a set of lights and expose control functions to the kernel
class LightsPlugin:
    """
    Plugin class to manage a set of smart lights and expose control functions to the Semantic Kernel.

    This class simulates a collection of light devices, allowing their states to be queried and changed.
    The methods are decorated as kernel functions so they can be invoked by the AI assistant.
    """

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
    ) -> list:
        """
        Returns a list of all lights and their current state.

        Returns:
            list: A list of dictionaries representing each light and its state.
        """
        return self.lights

    @kernel_function(
        name="change_state",
        description="Changes the state of the light",
    )
    def change_state(
        self,
        light_id: int,
        is_on: bool,
    ) -> dict | None:
        """
        Changes the state (on/off) of the light with the given light_id.

        Args:
            light_id (int): The ID of the light to change.
            is_on (bool): The new state for the light (True for on, False for off).

        Returns:
            dict | None: The updated light dictionary if found, otherwise None.
        """
        for light in self.lights:
            if light["id"] == light_id:
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
        ai_model_id="gpt-4.1-mini",
        api_key=environ["OPENAI_API_KEY"]
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
    user_input = None
    while True:
        # Collect user input from the console
        user_input = input("User > ")

        # Exit the loop if the user types "exit"
        if user_input == "exit":
            break

        # Add the user's message to the chat history
        history.add_user_message(user_input)

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
