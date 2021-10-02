import requests
import re


access_token = "" #access token

def main():
    id_user = input("Введите id пользователя:")
    if not id_user.isdigit():
        print("Ошибка ввода")
        return
    friend_list = requests.get("https://api.vk.com/method/friends.get?user_id=" + id_user + \
                 "&fields=name&access_token=" + access_token + "&v=5.131").text
    error_num = re.search(r'"error_code":(\d+)', friend_list)
    if error_num == 18:
        print("Страница пользователя была удалена или заблокирована")
        return
    if error_num == 10:
        print("Произошла внутренняя ошибка сервера")
        return
    if error_num == 28:
        print("Ключ доступа приложения недействителен")
        return
    friend_list_first_name = re.findall(r'"first_name":"(\w+)', friend_list)
    friend_list_last_name = re.findall(r'"last_name":"(\w+)', friend_list)
    friend_list_id = re.findall(r'"id":(\d+)', friend_list)
    for i in range(len(friend_list_id)):
        print(friend_list_first_name[i] + " " + friend_list_last_name[i] + " " + friend_list_id[i])


if __name__ == "__main__":
    main()
