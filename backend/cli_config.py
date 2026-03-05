from streamlab import StreamLabWS
from json import dumps

print("Bienvenue dans le mode de configuration de StreamKitAuto !")
print("Nous allons commencer par configurer la connexion entre ce script et StreamLab !\n")
print("Instructions:\n"
      "1. Ouvrir StreamLab\n"
      "2. Aller dans Paramètres\n"
      "3. Ouvrir Mobile\n"
      "4. Descendre jusqu'à Connexions tierces\n"
      "5. Activer 'Autoriser les connexions de tiers'\n"
      )

input("\nPressez ENTER quand vous aurez tout fini !\n")

print("Parfait, maintenant, connectons-nous à StreamLab !")
ip = input("Addresse IP [localhost]: ")
port = input("Port [59650]: ")

conf = {
    "ip": "localhost" if ip == "" else ip,
    "port": 59650 if port == "" else port,
    "api_token": input("Token du WS: ")
}
slc = StreamLabWS(ip=conf["ip"], port=conf["port"], token=conf["api_token"])
scenes = []

for [index, scene] in enumerate(slc.list_scenes(), start=1):
    print(f"{index}: {scene['name']}")
    scenes.append(scene)

scene_int = int(input("\nNuméro de la scène: ")) - 1
scene = scenes[scene_int]
scene_id = scenes[scene_int]['id']

print("Récupération des sources...✅")
source_names = []
sources = []

for plugin in scene['nodes']:
    if 'browser_source' in plugin['sourceId']:
        if plugin['name'] not in source_names:
            source_names.append(plugin['name'])
            sources.append(plugin)

for [index, source] in enumerate(sources, start=1):
    print(f"{index}: {source['name']}")

source_int = int(input("\nNuméro de la source: ")) - 1
source_id = sources[source_int]['sourceId']

print(f"\nParfait ! Nous avons maintenant les paramètres nécessaires pour faire fonctionner StreamKitAuto !")
print("Enregistrement des données...", end="")

conf["browser_id"] = source_id

with open(file="config.json", mode="w", encoding="utf-8") as json_file:
    json_file.write(dumps(conf, indent=2, sort_keys=True))
