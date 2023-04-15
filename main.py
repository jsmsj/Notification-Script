from bs4 import BeautifulSoup
import requests,json,base64

WEBHOOK_URLS = [
    'https://discord.com/api/webhooks/12345/sdfghjk',
    'https://discord.com/api/webhooks/1234345/sdf34567bvghjk'
]


def post_to_webhook(data,url):

    r = requests.get(url)
    r = r.json()

    headers = {
        'Content-Type': 'application/json'
    }

    resp = requests.post(url,headers=headers,json=data)
    if resp.status_code == 204:
        print(f'Successfully sent message to channel_id ({r["channel_id"]}) in guild_id ({r["guild_id"]})')
    else:
        print(f'Unable to send message to channel_id ({r["channel_id"]}) in guild_id ({r["guild_id"]})')
        print(resp.content)

target_list = [{"url":url} for url in WEBHOOK_URLS]


def b64e(s):
    return base64.urlsafe_b64encode(s.encode()).decode()

icon_url = 'https://i.imgur.com/gL4SV7x.png'

user_name = 'Releases'

role_id_to_ping = '<@&790138905533743124>'

def get_details_from_steam_url(url):
    data = {}
    site = requests.get(url) 
    soup = BeautifulSoup(site.content, 'html.parser') 
    image_url = soup.find_all(class_='game_header_image_full')[0]['src']
    genre_tags = [a.text.strip() for a in soup.find_all(class_='glance_tags popular_tags')[0].find_all('a')]
    name = soup.find(class_='apphub_AppName').text
    app_id = soup.find(class_='game_page_background')['data-miniprofile-appid']
    data.update({'image_url':image_url})
    data.update({'genre_tags':genre_tags})
    data.update({'name':name})
    data.update({'app_id':app_id})
    return data


game_name = input('Enter Game Name / Release Name: ')

steam_url = input('Enter Steam Url: ')

def get_x_link(name):
    x = input(f'Enter {name} link, if none then press enter: ')
    return x

torrent_link = get_x_link('torrent')

pixeldrain_link = get_x_link('PixelDrain')

anonymousfiles_link = get_x_link('AnonymousFiles')

fileditch_link = get_x_link('FileDitch')

run_exe_name = input('Enter the name of the final executable. (Will be written in instructions. Run (gmae_name.exe)): ')

based_on = input('Based on: ')

size_after_extraction = input('Size after extraction: ')

size_downloaded = input('Size downloaded: ')

langs = input('Language(s): ')


language_changable_in_settings = input('Can language be changed in settings? Type (Y,y) or (N,n): ')


new_line = '\n'

if language_changable_in_settings.lower() == 'y':
    lang_change_str = "- Language can be changed in game settings"
else:
    lang_change_str = None

credit = input('Whom to thank for crack ? : ')

steam_data = get_details_from_steam_url(steam_url)

json_data = {
  "content": f"{role_id_to_ping}",
  "embeds": [
    {
      "color": 4183567,
      "image": {
        "url": f"{steam_data.get('image_url','')}"
      }
    },
    {
      "title": f"{game_name}",
      "description": f"""
**Torrent** *(Not recommended to use Utorrent, or Bittorrent)*
[Torrent]({torrent_link})

**Downloads**{new_line+f'[AnonymousFiles]({anonymousfiles_link})' if anonymousfiles_link else ''}{new_line+f'[FileDitch]({fileditch_link})' if fileditch_link else ''}{new_line+f'[PixelDrain]({pixeldrain_link})' if pixeldrain_link else ''}

**Instructions:**
1:Download game
2:Extract files
3:Run ({run_exe_name})

Enjoy the game!

**Info**
- Based on: {based_on}
- Size after extraction: {size_after_extraction}
- Size downloaded: {size_downloaded}{new_line + lang_change_str if lang_change_str else ''}
- Language(s): {langs}

*Thanks to {credit} for crack.*

{steam_url}""",
      "color": 4183567
    }
  ],
  "username": user_name,
  "avatar_url": icon_url,
  "attachments": []
}


print()
edit = input('Do you wish to edit the message ? Type (Y,y) or (N,n): ')
if edit.lower() == 'n':
    for url in WEBHOOK_URLS:
        post_to_webhook(json_data,url)
    input('Press enter to exit')
    exit()


# json_obj = json.dumps(json_data,indent=4)

discohook_data = {
    "messages": [
        {
            "data": json_data,
            "reference":""
        }
    ]
}
print()
print('Go to this url to edit. But you will need to add the webhook urls yourself')
print(f'https://discohook.org/?data={b64e(json.dumps(discohook_data))}')


discohook_backup_data = {
    "version": 7,
    "backups": [
        {
            "name": steam_data['app_id'],
            "targets": target_list,
            "messages":discohook_data['messages']
        }
    ]
}

final_json_data = json.dumps(discohook_backup_data,indent=4)

with open(f'{steam_data["app_id"]}.json','w') as f:
    f.write(final_json_data)

print()
print(f'Alternatively import {steam_data["app_id"]}.json file in https://discohook.org The backup file retains the webhook urls.')
input('Press enter to exit')
exit()