import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

TOKEN = "ВАШ_ТОКЕН"
GROUP_ID = "ID_ВАШЕГО_СООБЩЕСТВА"

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()

def send_message(user_id, message, attachment=None):
    """Отправляет сообщение пользователю."""
    vk.messages.send(
        user_id=user_id,
        message=message,
        attachment=attachment,
        random_id=0
    )

def handle_image(event):
    """Обрабатывает изображение и отправляет его обратно."""
    attachment = ""
    for attachment_item in event.message['attachments']:
        if attachment_item['type'] == 'photo':
            photo_sizes = attachment_item['photo']['sizes']
            largest_photo = max(photo_sizes, key=lambda size: size['width'])
            attachment = f"photo{attachment_item['photo']['owner_id']}_{attachment_item['photo']['id']}"

    if attachment:
        send_message(event.obj.message['from_id'], "Ваше изображение:", attachment=attachment)

def main():
    print("Бот запущен...")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            message_text = event.obj.message['text']

            if 'is_new_user' in event.obj.message:
                send_message(user_id, "Добро пожаловать! Отправьте изображение.")

            if event.obj.message['attachments']:
                handle_image(event)

            elif message_text:
                print(f"Игнорируем сообщение: {message_text}")

if __name__ == "__main__":
    main()
