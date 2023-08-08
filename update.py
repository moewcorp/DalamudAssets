import requests
import codecs,json,hashlib,os

recover_cheatname=True
all_plugins_hashs=dict()
if recover_cheatname:
    plugins = requests.get("https://api.xivplugins.com/v1/dalamud/plugins").json()
    repos = requests.get("https://api.xivplugins.com/v1/dalamud/repos").json()
    all_plugins=set(["NKPlugin"])
    for plugin in plugins:
        all_plugins.add(plugin["name"])
    print(f"Found plugins: {len(all_plugins)}")
    all_plugins_hashs={hashlib.sha256(name.encode("utf-8")).hexdigest().upper():name for name in all_plugins}

cheatplugin = requests.get("https://raw.githubusercontent.com/ottercorp/DalamudAssets/cn/UIRes/cheatplugin.json").json()
meta = requests.get("https://aonyx.ffxiv.wang/Dalamud/Asset/Meta").json()
print(f"Assets Version: {meta['Version']}")
os.environ["AssetsVersion"]=str(meta['Version'])
print(f"CheatBannedLen: {len(cheatplugin)}")

for plugin in cheatplugin:
    print(f"Banned {plugin['Name']}")
    plugin["AssemblyVersion"]="0.0.0.0"
    if recover_cheatname and plugin["Name"] in all_plugins_hashs:
        plugin["Name"]=all_plugins_hashs[plugin["Name"]]
        print(f"  Recover name: {plugin['Name']}")
    if "Reason" in plugin:
        print(f"  Reason: {plugin['Reason']}")

cheat_txt=json.dumps(cheatplugin, indent=4, ensure_ascii=False)

with codecs.open("UIRes/cheatplugin.json", "w", encoding="utf-8") as f:
    f.write(cheat_txt)

readable_hash = hashlib.sha1(cheat_txt.encode("utf-8")).hexdigest().upper()
print(f"Hash: {readable_hash}")

for item in meta["Assets"]:
    if item["FileName"]=="UIRes/cheatplugin.json":
        item["Url"]="https://raw.githubusercontent.com/moewcorp/DalamudAssets/main/UIRes/cheatplugin.json"
        item["Hash"]=readable_hash

with codecs.open("asset.json", "w") as f:
    json.dump(meta, f, indent=4)



