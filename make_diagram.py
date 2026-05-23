from app.graph import build_graph

graph = build_graph()

png_data = graph.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png_data)

print("graph.png generated")