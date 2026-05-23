from typing import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    topic: str
    search_summary: str
    prompt: str
    image_path: str
    critique: str
    rating: int
    iteration: int
    target_rating: int
    max_iterations: int
    history: Annotated[list, operator.add]
    output_dir: str
    best_image_path: str
    best_rating: int