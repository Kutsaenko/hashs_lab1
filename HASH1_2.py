from hashlib import sha3_224
import random
import numpy as np
import pandas as pd

message = "DmytroOlegovuchKutsaienko"

original_hash = sha3_224(message.encode()).hexdigest()[-8:]

hashes = {}

collision_found = False
i = 1

while not collision_found:
    modified_message = message + str(i)

    modified_hash = sha3_224(modified_message.encode()).hexdigest()[-8:]

    if modified_hash in hashes:
        collision_found = True
        print("Колізія знайдена!")
        print(f"Перше повідомлення: {hashes[modified_hash]}")
        print(f"Друге повідомлення: {modified_message}")
        print(f"Хеш: {modified_hash}")
    else:
        hashes[modified_hash] = modified_message
    i += 1


