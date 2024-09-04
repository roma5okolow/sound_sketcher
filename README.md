# **Sound Stretcher**

### **Description**
Sound Stretcher is a Python tool that stretches audio files in time without altering their pitch. It uses the Phase Vocoder algorithm to achieve high-quality time-stretching, making it ideal for audio processing applications such as slowing down or speeding up music and speech while preserving the original tone.

### **Features**
- **Time Stretching**: Adjust the duration of an audio file without changing its pitch.
- **Flexible Parameters**: Control the stretch ratio to either slow down or speed up the audio.
- **Support for WAV Files**: Works seamlessly with `.wav` files, commonly used in audio processing.
- **Multi-Channel Handling**: Automatically converts multi-channel audio to mono for processing.

### **Installation**
To use the Sound Stretcher, clone the repository and install the required dependencies:

```bash
git clone https://github.com/roma5okolow/sound_sketcher.git
cd audio-time-stretcher
pip install -r requirements.txt
```

### **Usage**
Once installed, you can run the script from the command line to stretch an audio file. Below is an example command:

```bash
python time_stretcher.py sample_input.wav output.wav 1.5
```
You can also provide strech values less that 1 in order to accelerate the file.
