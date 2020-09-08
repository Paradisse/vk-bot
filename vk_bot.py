# -*- coding: utf-8 -*-
import vk_api
import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

user_list = [455356105, 194437246, 188852279]       # список с ID пользователей
token_group = ''

def main():
    vk_session = vk_api.VkApi(token=token_group)    # переменную token_group либо заменить на токен, либо присвоить ей токен (str)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, '172647717')

    def add_user(id: int):
        user_list.append(id)

    def delete_user(id: int):
        check_member(members, id)
        user_list.remove(id)

    def check(array, f):        # проверка списка
        for item in array:      # берёт каждый ID из списка и проверяет
            if item == f:       # если хоть один ID подходит, то он выдаёт TRUE и не кикает, а иначе FALSE и соответственно кик
                return True
            else:
                pass
        return False

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            members = vk.messages.getConversationMembers(peer_id=event.obj.peer_id)

            def check_admin(array):
                for i in array['items']:
                    if i['member_id'] == event.obj.from_id:
                        try:
                            return i['is_admin']
                        except KeyError:
                            return False

            def check_member(array, id: int):
                for i in array['items']:
                    if i['member_id'] == id:
                        vk.messages.removeChatUser(
                            chat_id=(event.obj.peer_id - 2000000000),
                            user_id=id,
                            member_id=id,
                        )

            try:
                if event.obj.action['type'] == 'chat_invite_user':
                    user_id = event.obj.action['member_id']

                    if not (check(user_list, user_id) == True):
                        vk.messages.removeChatUser(
                            chat_id=(event.obj.peer_id - 2000000000),   # ID беседы
                            user_id=event.obj.from_id,                  # ID пользователя
                            member_id=event.obj.action['member_id'],    # ID пользователя
                        )
            except TypeError:
                pass

            try:
                if event.obj.text.split('/id ')[0] == '':
                    if check_admin(members):
                        user = int(event.obj.text.split('/id ')[1])
                        add_user(user)
                        print(f'добавил\nтеперь база:{user_list}')

                elif event.obj.text.split('/did ')[0] == '':
                    if check_admin(members):
                        user = int(event.obj.text.split('/did ')[1])
                        delete_user(user)
                        print(f'удалил\nтеперь база:{user_list}')
            except (ValueError, IndexError):
                pass


if __name__ == '__main__':
    main()
