from speech_components.utils.types import AdvancedRecognizer
from typing import Literal, List
from speech_components.config import ASSEMBLYAI_KEY
from speech_components.utils.types import Word
import assemblyai as aai
# Define key

class AssemblyRecognizer(AdvancedRecognizer):
    def __init__(self,model :Literal["best","nano"] = "best", api_key :str = ASSEMBLYAI_KEY):
        super().__init__()
        # Set API key
        aai.settings.api_key = api_key
        # Define model
        self.__speech_model = aai.SpeechModel.best if model == "best" else aai.SpeechModel.nano
        # Define config
        self.__config = aai.TranscriptionConfig(speech_model = self.__speech_model)
        # Define transcriber
        self.__transcriber = aai.Transcriber(config = self.__config)

    def transcribe(self,
                   audio_file :str,
                   **kwargs) -> str:
        """
        Transcribe audio into string
        :param audio_file: Path to the input file
        :return:
        """
        # Get transcription
        transcript = self.__transcriber.transcribe(audio_file)

        # Return status
        if transcript.status != aai.TranscriptStatus.completed:
            raise Exception(f"{transcript.error}")
        return transcript.text

    def segment(self,
                audio_file :str,
                in_milliseconds :bool = True,
                **kwargs) -> List[Word]:
        """
        Returning a list of dictionary information for words appeared in audio:
        :param audio_file: Path to the input file
        :param in_milliseconds: Specify time under second or millisecond format.
        :return:
        """
        # Get transcription
        transcript = self.__transcriber.transcribe(audio_file)
        # Return status
        if transcript.status != aai.TranscriptStatus.completed:
            raise Exception(f"{transcript.error}")
        # Return list of words under millisecond type
        output = []
        for word in transcript.words:
            # Specify second or millisecond format
            start = self._convert_to_second(word.start) if not in_milliseconds else word.start
            end = self._convert_to_second(word.end) if not in_milliseconds else word.end
            # Append to output
            output.append(Word(text=word.text, start=start, end=end, probability=word.confidence))
        return output
