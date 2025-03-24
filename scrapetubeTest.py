import scrapetube
import json


channel_id = "UC7Q2CIsQreNeaMEeh0Gr_RQ"  # Replace with the actual LAPL YouTube channel ID

videos = list(scrapetube.get_channel(channel_id))
print(len(videos))
print(json.dumps(videos[0],indent=4))

