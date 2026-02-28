from generate import generate_dataset
from analyze import analyze_dialogue
import json


DATASET_SIZE = 100


def save_jsonl(path: str, data: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():
    print("Generating dataset...")

    dataset = generate_dataset(DATASET_SIZE)

    print("Analyzing dialogues...")

    results = []

    for item in dataset:
        dialogue = item["dialogue"]

        analysis = analyze_dialogue(dialogue)

        results.append({
            "id": item["id"],
            "dialogue": dialogue,
            "analysis": analysis,
            "ground_truth": item["ground_truth"],
        })

    print("Saving results...")

    save_jsonl("results.jsonl", results)

    print("Done ✅")


if __name__ == "__main__":
    main()