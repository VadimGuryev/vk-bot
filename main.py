import vk_api
import my_token
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

vk_session = vk_api.VkApi(token=my_token.api_token)
vk = vk_session.get_api()


def send_welcome(user_id):
    vk.messages.send(
        user_id=user_id,
        message=f"Привет! Я чат-бот. Отправь мне картинку, и я верну тебе ее обратно :)",
        random_id=get_random_id()
    )


def send_photo_back(user_id, photo_attachment):
    print("photo_attachment_str:", photo_attachment)
    vk.messages.send(
        user_id=user_id,
        attachment=photo_attachment,
        message="Вот ваше фото:",
        random_id=get_random_id()
    )


print("Бот запущен!")
longpoll = VkLongPoll(vk_session)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:
        if event.text.lower() == 'привет':
            send_welcome(event.user_id)
        elif event.attachments:
            print("event.attachments:", event.attachments)
            attachment_type = event.attachments.get('attach1_type')
            if attachment_type == 'photo':
                photo_attachment_str = f"photo{event.attachments.get('attach1')}"
                if photo_attachment_str:
                    send_photo_back(event.user_id, photo_attachment_str)
