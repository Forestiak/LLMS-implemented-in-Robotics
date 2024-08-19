import pytest
import json
from LLMManager import LLMManager

def test_process_input_multiple_times(n=20):
    # Sample message and objects for the test
    message = "I need a banana"
    objects = ["banana", "large clamp"]

    # Initialize the LLMManager
    llm_manager = LLMManager(False)

    for i in range(n):
        try:
            # Call the process_input method
            response = llm_manager.process_input(message, objects)

            if response is None:
                print(f"Iteration {i}: Error - Response was null")
                continue

            # Verify the response can be parsed as JSON
            try:
                parsed_response = json.loads(response)
                is_valid_json = True
                print(f"Iteration {i}: JSON parsed successfully")
            except ValueError as e:
                is_valid_json = False
                print(f"Iteration {i}: Parsing error - {e}")

        except Exception as e:
            # Handle the case when LLM service is not available or any other exception occurs
            print(f"Iteration {i}: LLM service failed with exception - {e}")

if __name__ == "__main__":
    # Run the test multiple times
    test_process_input_multiple_times(n=20)
