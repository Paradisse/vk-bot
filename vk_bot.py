# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

user_list = [194437246, 188852279]    # список с ID пользователей


def main():
    vk_session = vk_api.VkApi(token=token_group)    # переменную token_group либо заменить на токен, либо присвоить ей токен (str)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, '172647717')

    def check(array, f):    # проверка списка
        for item in array:    # берёт каждый ID из списка и проверяет
            if item == f:    # если хоть один ID подходит, то он выдаёт TRUE и не кикает, а иначе FALSE и соответственно кик
                return True
            else:
                pass
        return False

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:    # API метод. Принимает все новые сообщения
            try:    # проверяет сообщение это от юзера или просто заход в беседу

                if event.obj.action['type'] == 'chat_invite_user':    # проверяет тип метода
                    user_id = event.obj.action['member_id']
# Мой способ проверки списка
                    if not (check(user_list, user_id) == True):
                        vk.messages.removeChatUser(
                            chat_id=(event.obj.peer_id - 2000000000),    # ID беседы
                            user_id=event.obj.from_id,    # ID пользователя
                            member_id=event.obj.action['member_id'],    # ID пользователя
                        )
            except TypeError: pass

# Способ febday
                # print(event.obj)
                # a = (user_id in user_list)
                # if not a:
                #     vk.messages.removeChatUser(
                #         chat_id=(event.obj.peer_id - 2000000000),
                #         user_id=event.obj.from_id,
                #         member_id=event.obj.action['member_id'],
                #     )


if __name__ == '__main__':
    main()
