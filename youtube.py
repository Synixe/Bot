from urllib.request import urlopen
import json
import discord
import asyncio

import tokens

class Commands():
    def register(self, client):
        self.new_video_loop = client.loop.create_task(self.new_video_loop_task(client))
        return {}

    async def new_video_loop_task(self, client):
        await client.wait_until_ready()
        print("Youtube Loop Started")
        while not client.is_closed():
            video = get_most_recent("UCiBR5odYpO1_hcOyvzvuWhg")
            f = open("youtube")
            youtube = f.read().strip()
            f.close()
            if youtube != video["id"]["videoId"]:
                f = open("youtube","w")
                f.write(video["id"]["videoId"])
                f.close()
                print("Posting New Video")
                for guild in client.guilds:
                    if "synixe" in guild.name.lower():
                        for c in guild.channels:
                            if c.name.lower() == "random":
                                await c.send("New Video!\n\n"+video["snippet"]["description"]+"\n\nhttps://www.youtube.com/watch?v="+video["id"]["videoId"])
            await asyncio.sleep(60 * 5)

def get_all_video_in_channel(channel_id):
    api_key = tokens.getToken("youtube")
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
    url = base_search_url+'key={}&channelId={}&part=snippet,id&order=date&maxResults=1'.format(api_key, channel_id)
    video_links = []
    with urlopen(url) as inp:
        resp = json.loads(inp.read().decode("UTF-8"))
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(i)

    return video_links

def get_most_recent(channel_id):
    return get_all_video_in_channel(channel_id)[0]
