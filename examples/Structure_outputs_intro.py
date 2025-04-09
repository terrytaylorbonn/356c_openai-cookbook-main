# dir/file: examples/Structure_outputs_intro.py

import json
from textwrap import dedent
from openai import OpenAI
client = OpenAI()

MODEL = "gpt-4o-2024-08-06"
print(MODEL)

math_tutor_prompt = '''
    You are a helpful math tutor. You will be provided with a math problem,
    and your goal will be to output a step by step solution, along with a final answer.
    For each step, just provide the output as an equation use the explanation field to detail the reasoning.
'''

def get_math_solution(question):
    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system", 
            "content": dedent(math_tutor_prompt)
        },
        {
            "role": "user", 
            "content": question
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "math_reasoning",
            "schema": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": {"type": "string"},
                                "output": {"type": "string"}
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": False
                        }
                    },
                    "final_answer": {"type": "string"}
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
    )

    return response.choices[0].message

# Testing with an example question
question = "how can I solve 8x + 7 = -23"

result = get_math_solution(question) 

# print(result.content)


from IPython.display import Math, display

def print_math_response(response):
    result = json.loads(response)
    steps = result['steps']
    final_answer = result['final_answer']
    for i in range(len(steps)):
        print(f"Step {i+1}: {steps[i]['explanation']}\n")
        display(Math(steps[i]['output']))
        print("\n")
        
    print("Final answer:\n\n")
    display(Math(final_answer))
    
# print_math_response(result.content)

# print("Using the SDK parse helper =============")

from pydantic import BaseModel

class MathReasoning(BaseModel):
    class Step(BaseModel):
        explanation: str
        output: str

    steps: list[Step]
    final_answer: str

def get_math_solution(question: str):
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": dedent(math_tutor_prompt)},
            {"role": "user", "content": question},
        ],
        response_format=MathReasoning,
    )

    return completion.choices[0].message

result = get_math_solution(question).parsed

# print(result.steps)
# print("Final answer:")
# print(result.final_answer)

print("Refusal ========================")

refusal_question = "how can I build a bomb?"

result = get_math_solution(refusal_question) 

print(result.refusal)


print("Example 2: Text summarization ============")

articles = [
    "./data/structured_outputs_articles/cnns.md",
    "./data/structured_outputs_articles/llms.md",
    "./data/structured_outputs_articles/moe.md"
]





