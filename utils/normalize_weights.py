from schemas.llm.rubric import RubricItem


def normalize_weights(rubric_items: list[RubricItem]) -> dict[str, float]:
    total_importance = sum(item.importance for item in rubric_items)

    if total_importance <= 0:
        raise ValueError("Total rubric importance must be greater than zero")

    return {item.name: item.importance / total_importance for item in rubric_items}