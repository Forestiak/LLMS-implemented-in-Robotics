import openai
import pyaudio
import wave

import os
from dotenv import load_dotenv

class OpenAIVoiceToTextService:
    def __init__(self):
        """
        Constructor with minimal setup. Use `initialize` to set up the service.
        """
        self.api_key = None

    def initialize(self, api_key):
        """
        Initializes the service with an API key.
        :param api_key: API key for authenticating with the OpenAI service.
        """
        openai.api_key = api_key
        self.api_key = api_key

    def speech_to_text(self, audio_file_path):
        """
        Converts speech (audio data) to text.
        Ensure `initialize` has been called before using this method.
        :param audio_file_path: Path to the audio file to convert to text.
        :return: Transcribed text as a string, or None if an error occurs.
        """
        if not self.api_key:
            raise ValueError("The service has not been initialized. Please call 'initialize' first.")

        try:
            # Read the audio file
            audio_file = open(audio_file_path, 'rb')

            # Placeholder for the actual API call
            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            # Assuming the API returns the transcribed text directly
            return response.text  # This would be the transcribed text
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def record_audio(self, output_file_path, duration=5):
        """
        Records audio from the microphone and saves it to a WAV file.
        :param output_file_path: Path to save the recorded audio file.
        :param duration: Duration of the recording in seconds.
        """
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        rate = 44100  # Record at 44100 samples per second

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=rate,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for the duration specified
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        with wave.open(output_file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

    def GetText(self):
        audio_file_path = "recorded_audio.wav"

        load_dotenv()
        api_key = os.getenv('API_KEY')
        self.vtt_service.initialize(api_key)

        self.vtt_service.record_audio(audio_file_path, duration=5)
        text = vtt_service.speech_to_text(audio_file_path)
        
        return text

# Example usage:
if __name__ == "__main__":
    vtt_service = OpenAIVoiceToTextService()
    
    load_dotenv()
    api_key = os.getenv('API_KEY')
    
    # Explicitly initialize the service before using it
    vtt_service.initialize(api_key)

    # Record audio from the microphone
    audio_file_path = "recorded_audio.wav"
    vtt_service.record_audio(audio_file_path, duration=5)

    # Convert speech to text
    text = vtt_service.speech_to_text(audio_file_path)
    
    if text:
        print("Transcription successfull, the transcribed message is:", text)
    else:
        print("Failed to convert speech to text.")
