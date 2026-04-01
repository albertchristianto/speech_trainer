class Text2SpeechInterface:
    def forward(self, input_text: str, lang: str, output_path: str) -> str:
        """Generate the wave and write the audio files into the path"""
        pass

    def version(self):
        return self._version
