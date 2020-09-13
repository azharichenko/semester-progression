FEATURES = {"DEBUG_MODE": False}


def feature(feature_id: str) -> bool:
    if feature_id not in FEATURES:
        raise ValueError("Key not a valid feature")
    return FEATURES[feature_id]
