def predict_score(
    home_prob,
    away_prob
):

    if home_prob >= 0.75:
        return "3-0"

    elif home_prob >= 0.65:
        return "2-0"

    elif home_prob >= 0.55:
        return "2-1"

    elif away_prob >= 0.75:
        return "0-3"

    elif away_prob >= 0.65:
        return "0-2"

    elif away_prob >= 0.55:
        return "1-2"

    else:
        return "1-1"