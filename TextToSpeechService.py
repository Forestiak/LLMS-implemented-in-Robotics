from openai import OpenAI
import datetime

class OpenAITTSService:
    def __init__(self):
        """
        Constructor with minimal setup. Use `initialize` to set up the service.
        """
        self.api_key = None
        self.voice = None

    def initialize(self, api_key, voice="default_voice"):
        """
        Initializes the service with an API key and a voice.
        :param api_key: API key for authenticating with the OpenAI service.
        :param voice: The voice to use for text-to-speech generation.
        """
        #openai.api_key = api_key
        self.api_key = api_key
        self.voice = voice

    def text_to_speech(self, text):
        """
        Converts text to speech using the configured voice.
        Ensure `initialize` has been called before using this method.
        :param text: The text to convert to speech.
        :return: Speech data as bytes, or None if an error occurs.
        """
        if not self.api_key or not self.voice:
            raise ValueError("The service has not been initialized. Please call 'initialize' first.")

        try:
            # Assuming OpenAI provides a text-to-speech API endpoint and method
            # This is a placeholder for the actual API call, which would look something like this:
            
            client = OpenAI(
                api_key = self.api_key
            )


            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"speech_{timestamp}.mp3"

            # Save the audio data to a file
            with open(file_name, "wb") as audio_file:
                audio_file.write(response.content)  # Assuming response.content is the audio data in bytes

            return file_name
            # Assuming the API returns the speech data directly
            return response.content  # This would be the audio data in bytes
        except Exception as e:
            print(f"Request failed: {e}")
            return None
        
if __name__ == "__main__":
    tts_service = OpenAITTSService()

    # Explicitly initialize the service before using it
    tts_service.initialize("", "alloy")

    text = "Hello, world! This is an example of text-to-speech conversion."
    
    # Get speech from text and save it
    filename = tts_service.text_to_speech(text)
    
    if filename:
        print(f"Speech conversion completed and saved to {filename}.")
    else:
        print("Failed to convert text to speech.")