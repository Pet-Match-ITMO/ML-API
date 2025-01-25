import json
import requests
import dataclasses
from dacite import from_dict
from decouple import config

from src.models.vk_post import GroupPostsResponse


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return super().default(obj)

def parse_data_from_group(group_name = "domikvlg", save = True) -> GroupPostsResponse:
    access_token = config('ACCESS_TOKEN')

    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=200&access_token={access_token}&v=5.81"
    response = requests.get(url)

    jsonResponse = response.json()["response"]
    groupPosts = from_dict(data=jsonResponse, data_class=GroupPostsResponse)

    if(save):
        with open("sample_data.json", "w", encoding='utf-8') as out:
            s = json.dumps(groupPosts, indent=4, ensure_ascii=False, cls=JSONEncoder)
            out.write(s)
    return groupPosts
