import os
import subprocess
from telebot import TeleBot, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)


def edit_video(input_path, output_path):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-vf", "crop=in_w:in_h-80:0:40",
        "-af", "atempo=1.02",
        "-preset", "fast",
        output_path
    ]
    subprocess.run(cmd)


@bot.message_handler(content_types=['video'])
def video_handler(message):
    msg = bot.reply_to(message, "⏳ Video processing...")

    file_info = bot.get_file(message.video.file_id)
    downloaded = bot.download_file(file_info.file_path)

    input_path = "input.mp4"
    output_path = "edited.mp4"

    with open(input_path, "wb") as f:
        f.write(downloaded)

    edit_video(input_path, output_path)

    bot.send_video(message.chat.id, video=open(output_path, "rb"))


if __name__ == "__main__":
    bot.infinity_polling()
