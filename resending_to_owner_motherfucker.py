import PyBot


def resend(message):
    id_owner = 1275894304
    if message.chat.id == id_owner:
        print("хеллоу")
            #PyBot.MypyBot.send_message(id_owner, "хеллоу")