# Multi-Bot

discord bot i made for myself but wanted to share :3

### Prerequisites
1. Install Pip Dependencies
   ```sh
   pip install yt_dlp pyttsx3 groq discord dotenv davey pynacl
   ```
2. Install FFmpeg
   - Windows: https://ffmpeg.org/download.html#build-windows
   - Mac: `brew install ffmpeg`
   - Linux: `sudo pacman -S ffmpeg`
3. Install eSpeak
   - Windows: https://sourceforge.net/projects/espeak/files/espeak/espeak-1.48.04/espeak-1.48.04-win32.zip/download
   - Mac: `brew install espeak espeak-ng`
   - Linux: `sudo pacman -S espeak espeak-ng`
### Installation

1. Get a Groq API key at https://console.groq.com/keys

2. Get a Discord Bot on-standby and copy it's token.

3. Go grab a pollunation API key to generate images

4. Clone the repo
   ```sh
   git clone https://github.com/4id3n063/bot.git
   ```

5. Create a new .env file and enter all of your APIs under
   ```env
   GROQ_API_KEY=
   DISCORD_BOT_TOKEN=
   POLL_API=
   ```
   and then your admin role under
   ```env
   ADMIN=
   ```

6. Make sure your discord bot is [ready and set up](https://discord.com/developers/applications)

7. Run main.py
   ```sh
   python main.py
   ```

