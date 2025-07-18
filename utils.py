def valider_reddit_credentials(creds):
    """
    Vérifie si les credentials Reddit sont complets (non vides).
    """
    requis = ["client_id", "client_secret", "username", "password", "user_agent"]
    if not isinstance(creds, dict):
        return False
    for champ in requis:
        if not creds.get(champ) or not creds[champ].strip():
            return False
    return True
