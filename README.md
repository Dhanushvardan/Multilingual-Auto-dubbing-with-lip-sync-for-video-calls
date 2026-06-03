# 🎙️ Multilingual Auto Dubbing with Lip Sync for Video Calls

> Real-time speech translation, voice dubbing, and lip-sync generation for video calls — bridging language barriers with AI.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Wav2Lip](https://img.shields.io/badge/Wav2Lip-lip--sync-FF6B35?style=flat-square)
![gTTS](https://img.shields.io/badge/gTTS-TTS-34A853?style=flat-square&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🧠 Overview

**Multilingual Auto Dubbing with Lip Sync** is a Python-based pipeline that enables real-time multilingual communication in video calls. It captures webcam video and microphone audio, transcribes the speech, translates it to a target language, synthesizes the translated speech, and uses **Wav2Lip** to generate a lip-synced video — all transmitted over a local socket connection simulating a video call.

The system operates in two modes: a **Server (Sender)** that records, processes, and sends the dubbed video, and a **Receiver (Client)** that receives and saves the final lip-synced output.

---

## ✨ Features

- 🎥 **Webcam + Microphone Recording** — Simultaneous video and audio capture using OpenCV and PyAudio
- 🗣️ **Speech-to-Text** — Transcribes audio chunks using Google Speech Recognition (`speech_recognition`)
- 🌍 **Multilingual Translation** — Translates transcribed text using Google Translate (`googletrans`) — English → Tamil (configurable)
- 🔊 **Text-to-Speech Synthesis** — Converts translated text to audio using Google Text-to-Speech (`gTTS`)
- ⏱️ **Audio Speed Normalization** — Dynamically adjusts synthesized audio duration to match video length using `librosa` + `scipy`
- 👄 **Lip Sync Generation** — Applies **Wav2Lip** to sync the dubbed audio with the speaker's face in the video
- 📡 **Socket-Based Video Transmission** — Sends the final processed video over a TCP socket to the receiver

---

## 🏗️ Architecture & Pipeline

```
┌─────────────────────────────────────────────────────┐
│                    SERVER (Sender)                  │
│                                                     │
│  1. 📹 Record Webcam + 🎙️ Microphone (10s)         │
│           ↓                                         │
│  2. 🔊 Split Audio into 1-min Chunks (pydub)        │
│           ↓                                         │
│  3. 🗣️ Speech Recognition (Google STT)             │
│           ↓                                         │
│  4. 🌍 Translate Text (googletrans: en → ta)        │
│           ↓                                         │
│  5. 🔈 Text-to-Speech (gTTS → .wav)                │
│           ↓                                         │
│  6. ⏱️ Speed-Match Audio to Video Duration          │
│     (librosa + scipy resample)                      │
│           ↓                                         │
│  7. 👄 Wav2Lip Inference → Lip-Synced Video         │
│           ↓                                         │
│  8. 📡 Send via TCP Socket (press 's')             │
└─────────────────────────────────────────────────────┘
                        │
                        ▼  TCP Socket (localhost:8888)
┌─────────────────────────────────────────────────────┐
│                   RECEIVER (Client)                 │
│                                                     │
│  1. 📡 Connect to Server Socket                    │
│  2. 📥 Receive Video Data (4096-byte chunks)        │
│  3. 💾 Save → received_video.mp4                   │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component             | Library / Tool                        |
|-----------------------|---------------------------------------|
| Video Capture         | OpenCV (`cv2`)                        |
| Audio Recording       | PyAudio, Wave                         |
| Audio Processing      | pydub, librosa, soundfile, scipy      |
| Speech Recognition    | `speech_recognition` (Google STT)    |
| Translation           | `googletrans`                         |
| Text-to-Speech        | `gTTS` (Google Text-to-Speech)        |
| Lip Sync              | Wav2Lip (deep learning model)         |
| Video Editing         | MoviePy                               |
| Networking            | Python `socket` (TCP)                 |
| Input Handling        | `keyboard`                            |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Webcam and microphone
- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) repository set up locally
- Wav2Lip pretrained checkpoint (`wav2lip.pth`) downloaded

### 1. Clone the Repository

```bash
git clone https://github.com/Dhanushvardan/Multilingual-Auto-dubbing-with-lip-sync-for-video-calls.git
cd Multilingual-Auto-dubbing-with-lip-sync-for-video-calls
```

### 2. Install Dependencies

```bash
pip install opencv-python pyaudio moviepy pydub SpeechRecognition googletrans==4.0.0-rc1 gTTS librosa soundfile scipy keyboard
```

> **Note:** For PyAudio on Windows, install via: `pip install pipwin && pipwin install pyaudio`

### 3. Set Up Wav2Lip

Clone and set up Wav2Lip in your working directory:

```bash
git clone https://github.com/Rudrabha/Wav2Lip.git
```

Download the `wav2lip.pth` checkpoint from the [Wav2Lip releases](https://github.com/Rudrabha/Wav2Lip) and place it at:

```
Wav2Lip/checkpoints/wav2lip.pth
```

### 4. Update File Paths

In `app.py`, update the hardcoded paths to match your local setup:

```python
output_directory = "your/path/cap"
oD = "your/path/cap/temp"
```

### 5. Run the Application

**Terminal 1 — Start the Server (Sender):**

```bash
python app.py
# Enter 't' when prompted
```

**Terminal 2 — Start the Receiver:**

```bash
python app.py
# Enter 'y' when prompted
```

Once the server finishes processing, press **`s`** to send the lip-synced video to the receiver.

---

## 📁 Project Structure

```
Multilingual-Auto-dubbing-with-lip-sync-for-video-calls/
├── app.py                    # Main application (server + receiver)
├── Wav2Lip/                  # Wav2Lip repo (set up separately)
│   ├── inference.py
│   └── checkpoints/
│       └── wav2lip.pth
├── cap/                      # Output directory
│   ├── final_output_b.mp4    # Merged video with original audio
│   ├── output_audio_b.wav    # Extracted audio
│   ├── chunk_folder/         # Audio chunks for STT
│   └── temp/
│       ├── result.avi        # Raw video
│       └── temp.wav          # Speed-adjusted TTS audio
├── results/
│   └── result_voice.mp4      # Wav2Lip output
└── received_video.mp4        # Final video received by client
```

---

## 🔄 How It Works — Step by Step

**Step 1 — Record:** OpenCV captures 10 seconds of webcam video while PyAudio simultaneously records microphone audio.

**Step 2 — Merge:** MoviePy combines the raw video and audio into `final_output_b.mp4`.

**Step 3 — Chunk & Transcribe:** pydub splits the audio into 60-second chunks. Each chunk is sent through Google Speech Recognition to produce a text transcript.

**Step 4 — Translate:** The full transcript is passed to `googletrans` for translation (default: English → Tamil).

**Step 5 — TTS:** The translated text is converted to speech using `gTTS` and saved as `temp.wav`.

**Step 6 — Speed Match:** `librosa` measures the duration of both the synthesized audio and the original video. `scipy.signal.resample` adjusts the audio speed so both durations match exactly.

**Step 7 — Lip Sync:** Wav2Lip's `inference.py` is called via `subprocess` with the original video and the speed-adjusted translated audio. It generates a lip-synced output video.

**Step 8 — Transmit:** The final video is read as bytes and sent over a TCP socket. The receiver saves it as `received_video.mp4`.

---

## ⚙️ Configuration

| Parameter         | Default         | Description                              |
|-------------------|-----------------|------------------------------------------|
| `record_seconds`  | `10`            | Duration of webcam/mic recording         |
| `frame_width`     | `640`           | Video frame width                        |
| `frame_height`    | `480`           | Video frame height                       |
| `fps`             | `30`            | Video frames per second                  |
| `sample_rate`     | `44100`         | Audio sample rate (Hz)                   |
| `src` language    | `'en'`          | Source language for translation          |
| `dest` language   | `'ta'`          | Target language (Tamil)                  |
| Socket port       | `8888`          | TCP port for video transmission          |

To change the translation language, update in `app.py`:

```python
translation = translator.translate(text, src='en', dest='fr')  # e.g., French
tts = gTTS(translation.text, lang="fr", slow=True)
```

---

## ⚠️ Known Limitations

- File paths are currently hardcoded for Windows (`E:/cap/`). Refactoring to relative paths or config file is recommended.
- Recording duration is fixed at 10 seconds per segment; streaming support is a planned improvement.
- Translation accuracy depends on Google's free API; rate limits may apply for longer sessions.
- Wav2Lip requires a CUDA-capable GPU for real-time or near-real-time performance.

---

## 🔮 Roadmap

- [ ] Refactor hardcoded paths to use config file / CLI args
- [ ] Support real-time streaming instead of fixed-duration recording
- [ ] Add support for more language pairs via config
- [ ] WebRTC integration for true browser-based video calls
- [ ] GPU acceleration and optimization for lower latency
- [ ] Simple UI/dashboard for mode selection and language config

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgements

- [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) — A Lip Sync Expert Is All You Need for Speech to Lip Generation in the Wild
- [gTTS](https://github.com/pndurette/gTTS) — Google Text-to-Speech
- [googletrans](https://github.com/ssut/py-googletrans) — Python Google Translate
- [librosa](https://librosa.org/) — Audio analysis library

---

## 👤 Author

**DHANUSHVARDAN A V J** — Python & AI Developer  
[GitHub](https://github.com/Dhanushvardan) · [LinkedIn](https://linkedin.com/in/your-profile)
