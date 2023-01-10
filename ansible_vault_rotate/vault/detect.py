def has_vault_secrets(path: str):
    found = False
    with open(path, "r") as f:
        line = f.readline()
        while line:
            if line.startswith("$ANSIBLE_VAULT") or '$ANSIBLE_VAULT' in line:
                found = True
                break
            line = f.readline()

    return found
