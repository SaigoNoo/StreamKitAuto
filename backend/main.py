from fastapi import FastAPI, WebSocket
from json import loads
from os.path import exists
from streamlab import StreamLabWS

app = FastAPI(debug=False, title="StreamKit")


# Discord config
class DiscordConfig:
    def __init__(self, server_id: str = None, channel_id: str = None):
        self.server_id = server_id
        self.channel_id = channel_id
        self.config = {}
        self.read_config()

    def read_config(self):
        if exists("config.json"):
            with open(file="config.json", mode="r", encoding="utf-8") as f:
                self.config = loads(f.read())
        else:
            self.config = "undefined"

    def set(self, server_id, channel_id):
        self.server_id = server_id
        self.channel_id = channel_id

    def response(self):
        if self.config == "undefined":
            print("[StreamKitAuto:Config] > Veuillez configurer votre fichier config via le fichier cli_config.py")
            return None
        else:
            if self.server_id is None or self.channel_id is None:
                return "#"
            else:
                return f"https://streamkit.discord.com/overlay/voice/{self.server_id}/{self.channel_id}?icon=true..."


dc = DiscordConfig()

slws = StreamLabWS(
    ip=dc.config.get("ip"),
    port=int(dc.config.get("port")),
    token=dc.config.get("api_token")
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = loads(data)
        dc.set(data["guildId"], data["vocalId"])
        slws.set_source_property(value=dc.response())
        print(f"StreamLabs Browser Plugin updated: {dc.response()}")
        await websocket.send_text("StreamKit Updated...")
