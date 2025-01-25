import json
from src.parser.parse_group import parse_data_from_group, JSONEncoder
from src.llm.solver import LLMSolver

if __name__ == "__main__":
    solver = LLMSolver()
    result = parse_data_from_group()
    relevant_items = list(filter(
        lambda post: len(post.text) > 0 and solver.is_animal_profile(post.text),
        result.items
    ))
    for item in relevant_items:
        item.shortText = solver.summarize(item.text)
    with open("db.json", "w", encoding='utf-8') as out:
        s = json.dumps(relevant_items, indent=4, ensure_ascii=False, cls=JSONEncoder)
        out.write(s)
