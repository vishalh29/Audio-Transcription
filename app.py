import streamlit as st
import whisper
import tempfile

def transcribe_to_points(audio_file):
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=True) as tmp_file:
        # Write the BytesIO object's content to the temporary file
        tmp_file.write(audio_file.read())
        tmp_file.seek(0)  # Go back to the start of the file after writing

        # Load and transcribe the audio using Whisper
        model = whisper.load_model("base")
        result = model.transcribe(tmp_file.name)  # Use transcribe method directly

    # Extract text from the DecodingResult object
    text = result["text"]  # Assuming the 'transcribe' method still returns a dict; if not, adjust accordingly

    # Format the transcription into numbered points
    sentences = text.split('. ')
    points = [f"{idx + 1}. {sentence.strip()}" for idx, sentence in enumerate(sentences) if sentence.strip()]
    return points

def main():
    st.title('Audio Transcription')
    audio_file = st.file_uploader("Upload your audio file", type=['mp3', 'wav', 'ogg', 'flac'])

    if audio_file is not None:
        with st.spinner('Transcribing...'):
            points = transcribe_to_points(audio_file)
            if points:
                st.success("Transcription Complete")
                for point in points:
                    st.write(point)
            else:
                st.error("Failed to transcribe or no recognizable speech in audio.")

if __name__ == "__main__":
    main()
