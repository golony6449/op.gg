def check_sync_data(income_data):
    if 'api_key'not in income_data:
        return False
    if 'score' not in income_data:
        return False
    if 'player_id' not in income_data:
        return False

    return True
