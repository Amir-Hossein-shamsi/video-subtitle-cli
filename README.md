# Video Subtitle CLI Tool 📹🔊

**A command‑line utility to extract audio, transcribe speech, and embed subtitles into video files.**

---

## 🔍 Overview

This Python tool uses FFmpeg and OpenAI Whisper to:

1. **Extract** audio from video (WAV, MP3, AAC, or copy original).
2. **Transcribe** audio into text using Whisper models.
3. **Generate** subtitle files (SRT, TXT, JSON).
4. **Embed** subtitles into the original video with proper language tags.

## ⚙️ Setup

1. **Clone repository**

   ```bash
   git clone https://github.com/Amir-Hossein-shamsi/video-subtitle-cli.git
   cd video-subtitle-cli
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure FFmpeg is installed** and in your PATH:

   ```bash
   ffmpeg -version
   ```

## 🚀 Usage

```bash
python3 subtitle_cli.py -i <input_video> [options]
```

By default, outputs are placed in `./.output/`.

### CLI Options

| Option         | Short | Default      | Description                                                |
| -------------- | ----- | ------------ | ---------------------------------------------------------- |
| `--input`      | `-i`  | (required)   | Path to input video file (e.g., `video.mp4`).              |
| `--output-dir` | `-o`  | `./.output/` | Directory for generated audio, subtitles, video.           |
| `--codec`      |       | `wav`        | Audio codec: `copy`, `mp3`, `aac`, `wav`.                  |
| `--quality`    |       | —            | MP3 quality (0=best → 9=worst).                            |
| `--bitrate`    |       | —            | AAC bitrate (e.g., `192k`).                                |
| `--model`      |       | `small`      | Whisper model: `tiny`, `base`, `small`, `medium`, `large`. |
| `--lang`       |       | `eng`        | Subtitle language code (ISO 639‑2, e.g., `eng`).           |

## 🎬 Examples

* **Basic**: WAV + English

  ```bash
  python3 subtitle_cli.py -i lecture.mp4
  ```

* **High‑quality MP3 + French**

  ```bash
  python3 subtitle_cli.py -i interview.mov -o outputs/ --codec mp3 --quality 2 --model medium --lang fra
  ```

* **Copy original audio**

  ```bash
  python3 subtitle_cli.py -i movie.mp4 --codec copy
  ```

## 🛠 Troubleshooting

* **FFmpeg not found**: Install FFmpeg and add to PATH.
* **CUDA errors**: Verify GPU drivers and CUDA toolkit.
* **Permission denied**: Check write permissions on output directory.

## 🤝 Contributing

Contributions welcome:

1. Fork project
2. Create branch: `git checkout -b my-feature`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin my-feature`
5. Open Pull Request

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

*Happy subtitling! 🌟*
