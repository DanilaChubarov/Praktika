import json
from typing import Any, Dict, List


DEFAULT_INSULIN_RATIO = 10.0


def save_data(path: str, items: List[Dict[str, Any]], insulin_ratio: str) -> None:
    payload = {
        "items": [
            {
                "food": item["food"],
                "calories": int(item["calories"]),
                "carbs": float(item["carbs"]),
                "sugar": float(item["sugar"]),
                "protein": float(item["protein"]),
            }
            for item in items
        ],
        "insulin_ratio": insulin_ratio,
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def load_data(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return {
        "items": [
            {
                "food": item.get("food", ""),
                "calories": int(item.get("calories", 0)),
                "carbs": float(item.get("carbs", 0.0)),
                "sugar": float(item.get("sugar", 0.0)),
                "protein": float(item.get("protein", 0.0)),
            }
            for item in data.get("items", [])
        ],
        "insulin_ratio": str(data.get("insulin_ratio", str(DEFAULT_INSULIN_RATIO))),
    }


def calculate_totals(items: List[Dict[str, Any]]) -> Dict[str, float]:
    totals = {"calories": 0, "carbs": 0.0, "sugar": 0.0}
    for item in items:
        totals["calories"] += int(item["calories"])
        totals["carbs"] += float(item["carbs"])
        totals["sugar"] += float(item["sugar"])
    return totals


def calculate_bread_units(carbs: float) -> float:
    return carbs / 12.0 if carbs >= 0 else 0.0


def estimate_insulin_units(carbs: float, ratio: float) -> float:
    if ratio <= 0:
        return 0.0
    return carbs / ratio
