import argparse
import subprocess
import time

def parse_hash(password_field):
    parts = password_field.split("$")
    # $y$j9T$salt$hash
    if len(parts) >= 5:
        #y
        algo = parts[1]
        #j9T
        params = parts[2]
        #salt
        salt = parts[3]
        #hash
        hash_value = parts[4]
        return "$"+algo+"$"+params+"$"+salt, hash_value
    return None, None


def shadow_users(line):
    line = line.strip()

    fields = line.split(":")
    user = fields[0]
    password_field = fields[1]

    superSalt, hash = parse_hash(password_field)
    if superSalt is not None:
        return user, superSalt, hash
    else:
        return None, None, None

def dictionnary(line):
    return line.strip()

def compare_hash(superSalt, hash_sadow, hash_generate):
    hash_value = hash_generate.stdout.strip()
    fullHash = superSalt+"$"+hash_sadow
    return hash_value == fullHash

def argument():
    parser = argparse.ArgumentParser(description="Script de copie de fichiers")

    parser.add_argument("-d", "--dictionnary", help="path to dictionary file", required=True)
    parser.add_argument("-s", "--shadow", help="path to shadow file", required=True)
    parser.add_argument("-D", "--delay", type=int, default=1, help="delay between try")
    parser.add_argument("-h2", "--help", action="store_true", help="view all possible command")

    args = parser.parse_args()
    return args.dictionnary, args.shadow, args.delay


if __name__ == "__main__":
    # path_dict, path_shadow, time_delay =argument()
    path_shadow = "shadow.txt"
    path_dict = "dictionnaire.txt"

    file_shadow = open(path_shadow, "r")
    
    is_running = True
    while is_running:
        line_shadow = file_shadow.readline()
        
        if line_shadow:
            user, superSalt, hash=shadow_users(line_shadow)
            if user is not None:
                file_dict = open(path_dict, "r")
                line_dict = file_dict.readline()
                while line_dict:
                    passwd = dictionnary(line_dict)
                    command = ['mkpasswd', '-m', 'yescrypt', '--salt', superSalt, passwd]
                    result = subprocess.run(command, capture_output=True, text=True)
                    find_hash = compare_hash(superSalt, hash, result)
                    if find_hash:
                        with open("file.txt", "a") as file:
                            file.write("User: "+user+"   Password: "+passwd+"\n")
                        break
                    line_dict = file_dict.readline()
                file_dict = open(path_dict, "r")
                                  
        else:
            is_running = False
            file_shadow = open(path_shadow, "r")