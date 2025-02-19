#%%
import asyncio
import nest_asyncio
# from bridge import App

from wnox import App
import json

nest_asyncio.apply()
o = App(app="mypy",
        resource="default",
        securekey="",
        image="/files/app/robot.webp",
        public=True)

udb = o.udb

async def on_connect(_):
    print("[bridge] connected.")
    rs = await o.api(app="myapp", cmd="ping", body={})
    print("ping result:",rs)

    o.subscribe("mychannel")

o.on("__connect",on_connect)

async def on_disconnect(_):
    print("disconnected!")
o.on("__disconnect",on_disconnect)


async def ping_handler(data:dict):
    jid = data["from"]
    app = data["app"]
    uid = data["uid"]
    resource = data["resource"]
    print("ping:", json.dumps(data, indent=True))

    return {"pong": True, "code": 0}
o.on("ping",ping_handler)



async def on_message(data:dict):
    sender = data["from"]
    channel = data["channel"]
    app = data["app"]
    body = data["body"]
    resource = data["resource"]
    uid = data["uid"]
    itsme = data["itsme"]
    itsbro = data["itsbro"]
    
    print("message:", json.dumps(data, indent=True))
o.on("__message",on_message)


# async def set_interval():
#     while True:
#         if o.connected():
#             print("sending mypi to mychannel...")
#             o.sendtochannel("mychannel", "mypy!")
#         await asyncio.sleep(3)
        



loop = asyncio.get_event_loop()
loop.create_task(o.loop())
# t = loop.create_task(set_interval())
loop.run_forever()
