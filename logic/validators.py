from datetime import datetime
from logic.schema import ExtractionResult, ActionItem


def is_valid_date(date_str: str | None) -> bool:
    if date_str is None:
        return True  # null deadlines are allowed
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def flag_issues(result: ExtractionResult) -> list[str]:
    """Returns a list of human-readable warnings about the extraction."""
    issues = []
    seen_tasks = set()

    for i, item in enumerate(result.action_items):
        if item.owner is None:
            issues.append(f"Item {i+1}: missing owner — '{item.task}'")

        if item.deadline is not None and not is_valid_date(item.deadline):
            issues.append(f"Item {i+1}: invalid date format '{item.deadline}' — '{item.task}'")

        if item.confidence < 0.5:
            issues.append(f"Item {i+1}: low confidence ({item.confidence}) — '{item.task}'")

        normalized = item.task.strip().lower()
        if normalized in seen_tasks:
            issues.append(f"Item {i+1}: possible duplicate task — '{item.task}'")
        seen_tasks.add(normalized)

    return issues


def dedupe_action_items(result: ExtractionResult) -> ExtractionResult:
    """Removes exact duplicate tasks (same task + owner), keeps highest confidence."""
    best: dict[tuple[str, str | None], ActionItem] = {}

    for item in result.action_items:
        key = (item.task.strip().lower(), item.owner)
        if key not in best or item.confidence > best[key].confidence:
            best[key] = item

    return ExtractionResult(action_items=list(best.values()))