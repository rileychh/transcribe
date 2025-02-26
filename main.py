import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv


def transcribe_audio(
    file_path, model="whisper-1", response_format="text", language=None
):
    """
    Transcribe audio file to text using OpenAI's Whisper model.

    Args:
        file_path (str): Path to the audio file
        model (str): The model to use for transcription
        response_format (str): The format of the response (text, json, verbose_json, etc.)
        language (str, optional): The language of the audio file

    Returns:
        The transcription result
    """
    # Ensure file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    # Open the audio file in binary mode
    with open(file_path, "rb") as audio_file:
        # Create transcription request
        transcription_params = {
            "model": model,
            "file": audio_file,
            "response_format": response_format,
        }

        # Add optional parameters if provided
        if language:
            transcription_params["language"] = language

        # Make the API call
        transcription = client.audio.transcriptions.create(**transcription_params)

    return transcription


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Transcribe audio files using OpenAI's Whisper model"
    )
    parser.add_argument("file_path", help="Path to the audio file to transcribe")
    parser.add_argument(
        "--model",
        default="whisper-1",
        help="Model to use for transcription (default: whisper-1)",
    )
    parser.add_argument(
        "--format",
        default="text",
        choices=["text", "json", "verbose_json", "srt", "vtt"],
        help="Response format (default: text)",
    )
    parser.add_argument("--language", help="Language of the audio file (optional)")
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps (requires verbose_json format)",
    )
    parser.add_argument("--output", help="Output file path (optional)")

    args = parser.parse_args()

    try:
        # Handle timestamp option
        if args.timestamps and args.format != "verbose_json":
            print(
                "Note: --timestamps option requires verbose_json format. Switching format."
            )
            args.format = "verbose_json"

            with open(args.file_path, "rb") as audio_file:
                result = client.audio.transcriptions.create(
                    model=args.model,
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["word"],
                )

            # Print transcription and word timestamps
            print("\nTranscription:")
            print(result.text)
            print("\nWord timestamps:")
            for word in result.words:
                print(f"{word['word']}: {word['start']} - {word['end']}")

            # Save to output file if specified
            if args.output:
                import json

                with open(args.output, "w") as f:
                    json.dump(result.model_dump(), f, indent=2)
        else:
            # Standard transcription
            result = transcribe_audio(
                args.file_path,
                model=args.model,
                response_format=args.format,
                language=args.language,
            )

            # Print result
            if args.format == "text" or args.format == "srt" or args.format == "vtt":
                print(result)
            else:
                print(result.text)

            # Save to output file if specified
            if args.output:
                if args.format == "text":
                    with open(args.output, "w") as f:
                        f.write(result)
                else:
                    with open(args.output, "w") as f:
                        f.write(result.text)

            print(
                f"\nTranscription {'saved to ' + args.output if args.output else 'complete'}!"
            )

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables or .env file")
        print(
            "Please create a .env file with your OpenAI API key: OPENAI_API_KEY=your_key_here"
        )
        exit(1)

    client = OpenAI()

    # Run main function
    main()
