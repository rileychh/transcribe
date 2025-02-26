# Transcribe

A command-line tool to transcribe audio files using OpenAI's Whisper model.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/transcribe.git
   cd transcribe
   ```

2. Install dependencies using `uv` (requires Python 3.13+):
   ```bash
   uv sync
   ```

3. Set up your API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key.

## Usage

### Basic Usage

```bash
uv run main.py path/to/audio/file.mp3
```

### Options

- `--model MODEL` - Model to use (default: whisper-1)
- `--format FORMAT` - Response format: text, json, verbose_json, srt, vtt (default: text)
- `--language LANGUAGE` - Language of audio (optional)
- `--timestamps` - Include word-level timestamps (requires verbose_json format)
- `--output FILE` - Save transcription to file

### Examples

Transcribe an audio file:
```bash
uv run main.py recording.mp3
```

Transcribe with specific language:
```bash
uv run main.py recording.mp3 --language en
```

Include word-level timestamps:
```bash
uv run main.py recording.mp3 --timestamps
```

Save to output file:
```bash
uv run main.py recording.mp3 --output transcription.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
