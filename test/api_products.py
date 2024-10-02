import requests


# Пример использования перехваченных данных для выполнения запроса к API
def send_api_request():
    url = 'https://kuper.ru/api/web/v1/products'  # URL, который мы перехватили
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Client-Token': '7ba97b6f4049436dab90c789f946ee2f',  # Перехваченный токен
        'Cookie': 'spid=1724067758295_ee701da9c99dcb589f38ef8c0caa4189_xtj7i4awxq3dstu7; external_analytics_anonymous_id=78d0306e-09d4-4210-bec7-060fe9338e91; _pk_id.6.ef9f=9131e108cf20d0c4.1724067762.; _sa=SA1.5c857c4b-03f7-404c-b7f7-bb1bea3ba99f.1724067761; iap.uid=3a062b2f2bc548b38628ebf2cfd5db83; _ym_uid=1724067763489494829; _ym_d=1724067763; rrpvid=325833235267327; rcuid=66c32fb31c7c78f0809d6ea2; flocktory-uuid=70a66b93-d20b-43cb-a85b-dbed2fa72ac5-6; uxs_uid=27389a00-5e20-11ef-86e1-c96f862ef74b; mindboxDeviceUUID=ab48e45a-1ef3-45af-a561-75b890eada97; directCrm-session=%7B%22deviceGuid%22%3A%22ab48e45a-1ef3-45af-a561-75b890eada97%22%7D; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX19Kc9Cmm5LDE0Sig4OU6QcJpcxGhDw775d32vQE7FThe8BH0DKfbh%2FR5qh4qd2m0dcl7YsqL%2Fa7LnQ5Lbn1NS78sftkNVdoZ0mXikvH%2FySVzlTgDtRVofXlMADB8iGJxVSsHmyE6BUl%2Bg%3D%3D; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2FIW%2Ft%2FabCH6UETJrhyLXlUPAweIm3JW1U%3D; adtech_uid=b40f50b5-c7eb-4f2c-99f0-1b02f289a39b%3Akuper.ru; top100_id=t1.7588506.1352552351.1724133208036; tmr_lvid=b47eed22a4ee9b1657dc631ac276eea8; tmr_lvidTS=1724133208081; adrcid=AVTl2Dl5HbzkrqIQWkkMMbQ; spsn=1726823036709_7b2276657273696f6e223a22332e332e33222c227369676e223a226638626161633366626632346137303036613338653032323165306638353136222c22706c6174666f726d223a2257696e3332222c2262726f7773657273223a5b226368726f6d65222c2279616e646578225d2c2273636f7265223a302e367d; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaGJDRnNHYVFOeUNqWkpJaGxyTVVaMFgzcEhUak51UlZsTWVIaFdRa3BEYUFZNkJrVlVTU0lXTVRjeU56QTNNVFV6T0M0NU1qSXhORGtHT3dCRyIsImV4cCI6IjIwMjQtMTAtMDdUMDY6MDU6MzguOTIyWiIsInB1ciI6bnVsbH19--2f8b1c2e8116801a56201184e262a5eb37ce19bf; identified_address=true; identified_user=true; OnboardingState={%22state%22:{%22viewedOnboardingKeys%22:[%22your_promocodes%22%2C%22user_goals%22]}%2C%22version%22:0}; cookies_consented=yes; _pk_ref.6.ef9f=%5B%22%22%2C%22%22%2C1727192337%2C%22https%3A%2F%2Fyandex.ru%2Fsearch%2F%3Ftext%3D%D0%BA%D1%83%D0%BF%D0%B5%D1%80%26clid%3D2668747%26win%3D651%26lr%3D44%22%5D; _pk_ses.6.ef9f=1; sessionId=1727192337618527499; acs_3=%7B%22hash%22%3A%225c916bd2c1ace501cfd5%22%2C%22nextSyncTime%22%3A1727278740882%2C%22syncLog%22%3A%7B%22224%22%3A1727192340882%2C%221228%22%3A1727192340882%2C%221230%22%3A1727192340882%7D%7D; adrdel=1727192343552; _ym_visorc=w; _ym_isad=1; domain_sid=7YR06CGdlyd14NEuimQXn%3A1727192386432; b2b_benefits_disabled=true; spsc=1727195622788_fd5f3c435517028a6f6be160c579501b_0d4e0eb9c92181c656f0cb950dff1b59a3402473b747382c8fc1bc9ef31a9efa; ssrMedia={%22windowWidth%22:880%2C%22primaryInput%22:%22mouse%22}; tmr_detect=0%7C1727196534742; rl_group_id=RudderEncrypt%3AU2FsdGVkX1%2B%2F%2BRswknnbEKvgU5gqWhb4VNKXd1Pu7j0%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2BrBa0Mzesn99ujlMOHHq0AgYGeNT5Ed9o%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX1%2Ba5LEn0GlpTud5n3wljeQJOeQcu1VVA6DFbrJvYB8Olvk9lTScw8LuLukSQOEwAVtLP4lzXpHF%2FQ%3D%3D; rl_user_id=RudderEncrypt%3AU2FsdGVkX18vIgVjU3cPbVofiJ%2Bbb9MXmIzxuOXqXqu2CO3Oucs6HtY2c8EuRANxwrZ9PXTIL6WUFlTYOxU%2FYQ%3D%3D; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2BX85lDZw%2FSvplaf3xpcQ%2FixqhLa6LKQWShWD47GNyNibIepUcSxlrxs%2BjoLA7LTtjUxzTYRnVlr398PfJt1PojAlycQJWEOAcHfHfWftq%2FL3a6xBOe%2F8yvsK%2FOuG8Fs4CJUhW6wH8QstORi2ktTB85Qy1omf%2BOxj9g7F89BopaMAZed%2BAy4VAjM7jV2mC9dW2XCeeWoZj%2Fgwi098ggVnv1Oqytn8NmsK6Vejzw%2B5t20hZw4nFWOQ2Wwcor7IZJWOuhuwE%2BS5yBtWNtLksNZqXwJEKvyWfxQUc%3D; rl_session=RudderEncrypt%3AU2FsdGVkX1%2BmjIR5bwQ3ZUwItk6qcndrnrjfgAgMyojCn8A3LvclRSUU5yb14PHtlJipcDA7RhuIKQkNdulBMBvBLmQqYHnGlICOxCfAJUIBmdxQ%2FAOWkZzymE1a0U2c0iu3aBC9M2%2Buvnked4T87w%3D%3D; _808db7ba1248=%5B%7B%22source%22%3A%22%28direct%29%22%2C%22medium%22%3A%22%28none%29%22%2C%22cookie_changed_at%22%3A1727194127%7D%2C%7B%22source%22%3A%22kuper.ru%22%2C%22medium%22%3A%22referral%22%2C%22cookie_changed_at%22%3A1727196553%7D%5D; _Instamart_session=TzZ1cGFTYTl3Wll4MkZmWU9NZU9vYmpGOGNZUHV4OVcxckRkYzUwemx0YjBWL1dDMHUvbVBqTjVnZmdjczROQVRLZVdzN2t2R1o2Uno4UW5zU3ZQL0VTWUlKSzJPMXJuak5OR0JiL21KVXJ6WXE5eVpBV1VoS3BWSGhTdTFoNEpIV05BNGFJU2NnVEhOUlk4blo1WElyUHc0R1BKc2ZBMmpQOVJtZVh0ZE4vRnd4SFRJNGdGUVpiN1BwRWVJbjJ4MTJnelg3TmUwbk5UcEtId3BQY1lXdzVsMzZhVjJjbDVvWmVKSXNKM2NIa2NuczEvb0FHellVREllTWVyNS84SVFDektoTTFmMzZ0Q28vYkZML041UFNNVXhEbW1Dd2V2Mkp0ZXVza2RyYXAvaGZyalBuS1ZobktBOTRJN3ZuTENzMVlMK0loOFNFbjNVMFQ3SVExdHlIeE9HQ2VPK1JWclovTnRON1k4QmowUk4xU1dzNmJuY0E3VW1Ha1JkZ054SnREMjZBZVMwL3REZk05ZFVlZmFlUFJyMDhaZGtpelhjcEUwNlkrNHZXeU13SWJFWFBYNU9Rb1hKREdBY2FHRS9lSFd1SndoY0RXZXlYdDVjVXBBWGRqTFZuU3NYalIvNlRqSjBzWnlBUjc1aVB5MExDNW05cU1Nc0NjZlJ3RjF4RGYzdVJ1YnRDRTlNNlZFYmgyV3JBeVdmYUxQZnBNSjRRU2dKNTNNU3lyeVVGaitEclZTenBueU0rZGxtZ2JtaVBueXpXaWx1Yk5vUG5BWnE3VXM0UTFLUFkxbncxVGFET0NZTUFRWTlsaz0tLUJKa1J5SkVNSUtNN1lWT2VrajhjbGc9PQ%3D%3D--aadb0fce9dac0f75089518ace040daebeb7fda02; t3_sid_7588506=s1.1102403335.1727192340085.1727196553972.8.89'  # Если сессия использует куки
    }

    # Если это POST запрос, добавляем данные
    data = {

        'page':'1',
        'per_page': '24',
        'q': 'Бананы',
        'store_id': '211',
        'tenant_id': 'sbermarket'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Запрос успешен!")
        print(response.text)  # Выводим полученные данные
    else:
        print(f"Ошибка: {response.status_code}")
        print(f"Ошибка: {response.text}")


if __name__== '__main__':
    # Отправляем запрос с перехваченными данными
    send_api_request()
