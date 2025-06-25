import os
import json
from tqdm import tqdm
from src.parser.parse_group import parse_data_from_group, JSONEncoder
from src.llm.solver import LLMSolver

def read_groups(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    solver = LLMSolver()
    groups = read_groups("groups.txt")
    all_data = {}

    # Чтение существующих данных из db.json, если файл существует
    db_path = "db.json"
    if os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except Exception:
                all_data = {}
    print(f"Loaded existing data for {len(all_data)} groups from db.json")

    for group in tqdm(groups, desc="Processing groups", unit="group"):
        if group in all_data:
            tqdm.write(f"Skip {group=}, already in db.json")
            continue
        tqdm.write(f"Get db from {group=}")
        try:
            result = parse_data_from_group(group)
            relevant_items = list(filter(
                lambda post: len(post.text) > 0 and solver.is_animal_profile(post.text),
                result.items
            ))
            tqdm.write(f"Found {len(relevant_items)} relevant items in group '{group}'")
            for item in tqdm(relevant_items, desc=f"Processing posts in {group}", leave=False):
                item.shortText = solver.summarize(item.text)
                item.pet_info = solver.generate_pet_json_from_post(item.text)
            all_data[group] = relevant_items
        except Exception as e:
            tqdm.write(f"Error processing group '{group}': {e}")
            continue

    with open("db.json", "w", encoding='utf-8') as out:
        s = json.dumps(all_data, indent=4, ensure_ascii=False, cls=JSONEncoder)
        out.write(s)
