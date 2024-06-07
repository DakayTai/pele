import telebot
from telebot import types
import time

API_TOKEN = '7424864995:AAHx18ywhNXrDHZvLIlRi4seUTV5uD3xXBc'
ADMIN_ID = 6803990183

bot = telebot.TeleBot(API_TOKEN)

start_time = time.time()

# Fungsi untuk mengirim pesan dengan format yang ditentukan
def send_message_copy(chat_id, message):
    if message.content_type == 'text':
        bot.send_message(chat_id, message.text)
    elif message.content_type == 'photo':
        bot.send_photo(chat_id, message.photo[-1].file_id, caption=message.caption)
    elif message.content_type == 'video':
        bot.send_video(chat_id, message.video.file_id, caption=message.caption)
    elif message.content_type == 'document':
        bot.send_document(chat_id, message.document.file_id, caption=message.caption)
    elif message.content_type == 'audio':
        bot.send_audio(chat_id, message.audio.file_id, caption=message.caption)
    elif message.content_type == 'voice':
        bot.send_voice(chat_id, message.voice.file_id, caption=message.caption)
    elif message.content_type == 'video_note':
        bot.send_video_note(chat_id, message.video_note.file_id)
    elif message.content_type == 'location':
        bot.send_location(chat_id, message.location.latitude, message.location.longitude)
    elif message.content_type == 'contact':
        bot.send_contact(chat_id, message.contact.phone_number, message.contact.first_name, message.contact.last_name)
    elif message.content_type == 'sticker':
        bot.send_sticker(chat_id, message.sticker.file_id)
    elif message.content_type == 'animation':
        bot.send_animation(chat_id, message.animation.file_id, caption=message.caption)
    else:
        bot.send_message(chat_id, "Unsupported message type")

@bot.message_handler(commands=['share'])
def share_message(message):
    if message.from_user.id == ADMIN_ID:
        try:
            parts = message.text.split()
            if len(parts) != 2:
                bot.reply_to(message, "Usage: /share [chat_id]")
                return
            chat_id = int(parts[1])
            if message.reply_to_message:
                send_message_copy(chat_id, message.reply_to_message)
                bot.reply_to(message, "Message sent successfully.")
            else:
                bot.reply_to(message, "Please reply to the message you want to share.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

@bot.message_handler(commands=['reason'])
def send_reason(message):
    if message.from_user.id == ADMIN_ID:
        if message.reply_to_message:
            bot.forward_message(ADMIN_ID, message.chat.id, message.reply_to_message.message_id)
            bot.send_message(ADMIN_ID, f"Reason from {message.from_user.username or message.from_user.first_name}: {message.text}")
            bot.reply_to(message, "Reason sent to admin.")
        else:
            bot.reply_to(message, "Please reply to the message you want to send the reason for.")

@bot.message_handler(commands=['add'])
def join_group(message):
    if message.from_user.id == ADMIN_ID:
        try:
            parts = message.text.split()
            if len(parts) != 2:
                bot.reply_to(message, "Usage: /add [group_link]")
                return
            group_link = parts[1]
            bot.send_message(message.chat.id, f"Joining group: {group_link}")
            bot.join_chat(group_link)
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

bot.polling()
