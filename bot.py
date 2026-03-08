# ============================================================
#  TELEGRAM MUSIC PROCESSING BOT
#  Ultra Pro Max – Clean Human Style Code
# ============================================================

import os
import telebot
import subprocess
from pydub import AudioSegment
from pydub.effects import normalize

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

BOT_TOKEN = os.getenv("8704240364:AAGsXqSmITtqjq4WwbaoDe_k2SjibWMLVf4")

DOWNLOAD_FOLDER = "downloads"
OUTPUT_FOLDER = "output"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

bot = telebot.TeleBot(BOT_TOKEN)


# ------------------------------------------------------------
# AUDIO PROCESSING ENGINE
# ------------------------------------------------------------

class AudioProcessor:
    """
    High-quality audio processing engine.
    Includes:
        - Slow + Reverb
        - Bass boost
        - Deep sound enhancement
        - Clean normalization
    """

    @staticmethod
    def slow_audio(audio):
        """Create slowed version of audio."""
        slowed = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * 0.80)
        })
        return slowed.set_frame_rate(audio.frame_rate)

    @staticmethod
    def bass_boost(audio):
        """Add bass boost."""
        return audio + 6

    @staticmethod
    def deep_sound(audio):
        """Deep sound enhancement."""
        return audio.low_pass_filter(120)

    @staticmethod
    def normalize_audio(audio):
        """Clean sound with normalization."""
        return normalize(audio)

    @staticmethod
    def apply_reverb(input_file, output_file):
        """Apply reverb using FFmpeg."""
        command = [
            "ffmpeg",
            "-i", input_file,
            "-af", "aecho=0.8:0.9:1000:0.3",
            output_file
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ------------------------------------------------------------
# BOT COMMANDS
# ------------------------------------------------------------

@bot.message_handler(commands=['start'])
def start_command(message):
    text = """
🎧 **Premium Music Processing Bot**

Features:
✔ Slowed + Reverb
✔ Bass Boost
✔ Deep Music
✔ High Quality
✔ Clean Sound
✔ Fast Processing
✔ Local Audio Engine

Send me an **audio file** to process.
"""
    bot.reply_to(message, text)


# ------------------------------------------------------------
# AUDIO HANDLER
# ------------------------------------------------------------

@bot.message_handler(content_types=['audio', 'voice'])
def process_audio(message):

    try:

        # File info
        file_info = bot.get_file(message.audio.file_id)
        downloaded = bot.download_file(file_info.file_path)

        input_path = os.path.join(DOWNLOAD_FOLDER, "input.mp3")
        output_path = os.path.join(OUTPUT_FOLDER, "processed.mp3")

        with open(input_path, "wb") as f:
            f.write(downloaded)

        # Load audio
        audio = AudioSegment.from_file(input_path)

        # Apply processing pipeline
        audio = AudioProcessor.slow_audio(audio)
        audio = AudioProcessor.bass_boost(audio)
        audio = AudioProcessor.deep_sound(audio)
        audio = AudioProcessor.normalize_audio(audio)

        # Export temporary file
        temp_file = os.path.join(OUTPUT_FOLDER, "temp.mp3")
        audio.export(temp_file, format="mp3")

        # Apply reverb via ffmpeg
        AudioProcessor.apply_reverb(temp_file, output_path)

        # Send processed audio
        with open(output_path, "rb") as f:
            bot.send_audio(message.chat.id, f)

        bot.send_message(message.chat.id, "✅ Processing Complete\n🎧 Ultra Clean Output")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")


# ------------------------------------------------------------
# BOT START
# ------------------------------------------------------------

print("🚀 Music Processing Bot Started")

bot.infinity_polling()
