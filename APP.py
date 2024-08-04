import requests
res_user = requests.get('https://www.swapi.tech/api/films')
dic_users = res_user.json()
print(dic_users["result"][0]["properties"]["characters"])

personajes = dic_users["result"][0]["properties"]["characters"]

for personaje_url in personajes:
    req_personaje = requests.get(f"{personaje_url}")
    dic_personaje = req_personaje.json()["result"]["properties"]
    print(dic_personaje)
