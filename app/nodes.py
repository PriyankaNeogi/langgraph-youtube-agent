from openai import OpenAI
import requests
import os
import shutil
from pydantic import BaseModel
import base64
from datetime import datetime
from langchain_openai import ChatOpenAI
from app.tools import search_web
from app.prompts import PROMPT_WRITER_SYSTEM


llm = ChatOpenAI(model="gpt-4o-mini")
client = OpenAI()

class CritiqueOutput(BaseModel):
    rating: int
    critique: str


def web_search(state):
    topic = state["topic"]

    summary = search_web(topic)

    return {
        "search_summary": summary
    }


def prompt_writer(state):

    topic = state["topic"]
    search_summary = state["search_summary"]

    critique = state.get("critique", "")

    prompt = f"""
Topic:
{topic}

Search Insights:
{search_summary}

Previous Critique:
{critique}

Create a cinematic YouTube thumbnail prompt.
"""

    response = llm.invoke([
        ("system", PROMPT_WRITER_SYSTEM),
        ("human", prompt)
    ])

    return {
        "prompt": response.content
    }

def generator(state):

    import base64

    prompt = state["prompt"]

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024"
    )

    image_base64 = response.data[0].b64_json

    image_bytes = base64.b64decode(image_base64)

    topic_slug = state["topic"].replace(" ", "_")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = f"outputs/{timestamp}_{topic_slug}"

    os.makedirs(output_dir, exist_ok=True)

    iteration = state["iteration"] + 1

    image_path = f"{output_dir}/iter_{iteration}.png"

    with open(image_path, "wb") as f:
        f.write(image_bytes)

    return {
        "image_path": image_path,
        "iteration": iteration,
        "output_dir": output_dir
    }

def critic(state):

    image_path = state["image_path"]

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    critic_llm = ChatOpenAI(model="gpt-4o-mini")

    structured_llm = critic_llm.with_structured_output(CritiqueOutput)

    response = structured_llm.invoke([
        (
            "system",
            """
You are a harsh YouTube thumbnail critic.

Most thumbnails should score between 5 and 7.

Only exceptional thumbnails deserve 9 or 10.

Critique:
- readability
- contrast
- emotional impact
- clickability
- composition
"""
        ),
        (
            "human",
            [
                {
                    "type": "text",
                    "text": "Critique this thumbnail."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    }
                }
            ]
        )
    ])

    history_entry = {
        "iteration": state["iteration"],
        "rating": response.rating,
        "critique": response.critique,
        "prompt": state["prompt"],
        "image_path": image_path
    }

    best_rating = max(state.get("best_rating", 0), response.rating)

    best_image_path = state.get("best_image_path", image_path)

    if response.rating >= best_rating:
        best_image_path = image_path

    return {
        "rating": response.rating,
        "critique": response.critique,
        "history": [history_entry],
        "best_rating": best_rating,
        "best_image_path": best_image_path
    }

def should_continue(state):

    if (
        state["rating"] >= state["target_rating"]
        or state["iteration"] >= state["max_iterations"]
    ):
        return "saver"

    return "prompt_writer"

import shutil


def saver(state):

    best_image = state["best_image_path"]

    final_path = f"{state['output_dir']}/final.png"

    shutil.copy(best_image, final_path)

    report_path = f"{state['output_dir']}/report.md"

    with open(report_path, "w") as f:

        f.write("# Thumbnail Generation Report\n\n")

        for item in state["history"]:

            f.write(f"## Iteration {item['iteration']}\n\n")

            f.write(f"### Rating\n")
            f.write(f"{item['rating']}/10\n\n")

            f.write("### Critique\n")
            f.write(f"{item['critique']}\n\n")

            f.write("### Prompt\n")
            f.write(f"{item['prompt']}\n\n")

            f.write("---\n\n")

    return {
        "final_image": final_path
    }