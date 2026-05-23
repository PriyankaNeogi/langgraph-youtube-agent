from app.graph import build_graph

graph = build_graph()

result = graph.invoke({
    "topic": "Why Python is best for AI",
    "iteration": 0,
    "target_rating": 8,
    "max_iterations": 3,
    "history": []
})

print(result)