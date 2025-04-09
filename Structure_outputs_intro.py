# dir/file: examples/Structure_outputs_intro.py

import json
from textwrap import dedent
from openai import OpenAI
client = OpenAI()

MODEL = "gpt-4o-2024-08-06"
print(MODEL)

# ## Example 1: Math tutor

# math_tutor_prompt = '''
#     You are a helpful math tutor. You will be provided with a math problem,
#     and your goal will be to output a step by step solution, along with a final answer.
#     For each step, just provide the output as an equation use the explanation field to detail the reasoning.
# '''

# def get_math_solution(question):
#     response = client.chat.completions.create(
#     model=MODEL,
#     messages=[
#         {
#             "role": "system", 
#             "content": dedent(math_tutor_prompt)
#         },
#         {
#             "role": "user", 
#             "content": question
#         }
#     ],
#     response_format={
#         "type": "json_schema",
#         "json_schema": {
#             "name": "math_reasoning",
#             "schema": {
#                 "type": "object",
#                 "properties": {
#                     "steps": {
#                         "type": "array",
#                         "items": {
#                             "type": "object",
#                             "properties": {
#                                 "explanation": {"type": "string"},
#                                 "output": {"type": "string"}
#                             },
#                             "required": ["explanation", "output"],
#                             "additionalProperties": False
#                         }
#                     },
#                     "final_answer": {"type": "string"}
#                 },
#                 "required": ["steps", "final_answer"],
#                 "additionalProperties": False
#             },
#             "strict": True
#         }
#     }
#     )

#     return response.choices[0].message

# # Testing with an example question
# question = "how can I solve 8x + 7 = -23"

# result = get_math_solution(question) 

# # print(result.content)


# from IPython.display import Math, display

# def print_math_response(response):
#     result = json.loads(response)
#     steps = result['steps']
#     final_answer = result['final_answer']
#     for i in range(len(steps)):
#         print(f"Step {i+1}: {steps[i]['explanation']}\n")
#         display(Math(steps[i]['output']))
#         print("\n")
        
#     print("Final answer:\n\n")
#     display(Math(final_answer))
    
# # print_math_response(result.content)

# # print("Using the SDK parse helper =============")

from pydantic import BaseModel

# class MathReasoning(BaseModel):
#     class Step(BaseModel):
#         explanation: str
#         output: str

#     steps: list[Step]
#     final_answer: str

# def get_math_solution(question: str):
#     completion = client.beta.chat.completions.parse(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": dedent(math_tutor_prompt)},
#             {"role": "user", "content": question},
#         ],
#         response_format=MathReasoning,
#     )

#     return completion.choices[0].message

# result = get_math_solution(question).parsed

# # print(result.steps)
# # print("Final answer:")
# # print(result.final_answer)

# print("Refusal ========================")

# refusal_question = "how can I build a bomb?"

# result = get_math_solution(refusal_question) 

# # print(result.refusal)


# print("Example 2: Text summarization ============")

# articles = [
#     "./examples/data/structured_outputs_articles/cnns.md",
#     "./examples/data/structured_outputs_articles/llms.md",
#     "./examples/data/structured_outputs_articles/moe.md"
# ]

# def get_article_content(path):
#     with open(path, 'r', encoding='utf-8') as f:
#         content = f.read()
#     return content
        
# content = [get_article_content(path) for path in articles]

# print(content)

# summarization_prompt = '''
#     You will be provided with content from an article about an invention.
#     Your goal will be to summarize the article following the schema provided.
#     Here is a description of the parameters:
#     - invented_year: year in which the invention discussed in the article was invented
#     - summary: one sentence summary of what the invention is
#     - inventors: array of strings listing the inventor full names if present, otherwise just surname
#     - concepts: array of key concepts related to the invention, each concept containing a title and a description
#     - description: short description of the invention
# '''

# class ArticleSummary(BaseModel):
#     invented_year: int
#     summary: str
#     inventors: list[str]
#     description: str

#     class Concept(BaseModel):
#         title: str
#         description: str

#     concepts: list[Concept]

# def get_article_summary(text: str):
#     completion = client.beta.chat.completions.parse(
#         model=MODEL,
#         temperature=0.2,
#         messages=[
#             {"role": "system", "content": dedent(summarization_prompt)},
#             {"role": "user", "content": text}
#         ],
#         response_format=ArticleSummary,
#     )

#     return completion.choices[0].message.parsed


# summaries = []

# for i in range(len(content)):
#     print(f"Analyzing article #{i+1}...")
#     summaries.append(get_article_summary(content[i]))
#     print("Done.")


# def print_summary(summary):
#     print(f"Invented year: {summary.invented_year}\n")
#     print(f"Summary: {summary.summary}\n")
#     print("Inventors:")
#     for i in summary.inventors:
#         print(f"- {i}")
#     print("\nConcepts:")
#     for c in summary.concepts:
#         print(f"- {c.title}: {c.description}")
#     print(f"\nDescription: {summary.description}")
    
    
# for i in range(len(summaries)):
#     print(f"ARTICLE {i}\n")
#     print_summary(summaries[i])
#     print("\n\n")
    

print("Example 3: Entity extraction from user input =================")


from enum import Enum
from typing import Union
import openai

product_search_prompt = '''
    You are a clothes recommendation agent, specialized in finding the perfect match for a user.
    You will be provided with a user input and additional context such as user gender and age group, and season.
    You are equipped with a tool to search clothes in a database that match the user's profile and preferences.
    Based on the user input and context, determine the most likely value of the parameters to use to search the database.
    
    Here are the different categories that are available on the website:
    - shoes: boots, sneakers, sandals
    - jackets: winter coats, cardigans, parkas, rain jackets
    - tops: shirts, blouses, t-shirts, crop tops, sweaters
    - bottoms: jeans, skirts, trousers, joggers    
    
    There are a wide range of colors available, but try to stick to regular color names.
'''

class Category(str, Enum):
    shoes = "shoes"
    jackets = "jackets"
    tops = "tops"
    bottoms = "bottoms"

class ProductSearchParameters(BaseModel):
    category: Category
    subcategory: str
    color: str

def get_response(user_input, context):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": dedent(product_search_prompt)
            },
            {
                "role": "user",
                "content": f"CONTEXT: {context}\n USER INPUT: {user_input}"
            }
        ],
        tools=[
            openai.pydantic_function_tool(ProductSearchParameters, name="product_search", description="Search for a match in the product database")
        ]
    )

    return response.choices[0].message.tool_calls


example_inputs = [
    {
        "user_input": "I'm looking for a new coat. I'm always cold so please something warm! Ideally something that matches my eyes.",
        "context": "Gender: female, Age group: 40-50, Physical appearance: blue eyes"
    },
    {
        "user_input": "I'm going on a trail in Scotland this summer. It's goind to be rainy. Help me find something.",
        "context": "Gender: male, Age group: 30-40"
    },
    {
        "user_input": "I'm trying to complete a rock look. I'm missing shoes. Any suggestions?",
        "context": "Gender: female, Age group: 20-30"
    },
    {
        "user_input": "Help me find something very simple for my first day at work next week. Something casual and neutral.",
        "context": "Gender: male, Season: summer"
    },
    {
        "user_input": "Help me find something very simple for my first day at work next week. Something casual and neutral.",
        "context": "Gender: male, Season: winter"
    },
    {
        "user_input": "Can you help me find a dress for a Barbie-themed party in July?",
        "context": "Gender: female, Age group: 20-30"
    }
]



def print_tool_call(user_input, context, tool_call):
    args = tool_call[0].function.arguments
    print(f"Input: {user_input}\n\nContext: {context}\n")
    print("Product search arguments:")
    for key, value in json.loads(args).items():
        print(f"{key}: '{value}'")
    print("\n\n")
for ex in example_inputs:
    ex['result'] = get_response(ex['user_input'], ex['context'])
for ex in example_inputs:
    print_tool_call(ex['user_input'], ex['context'], ex['result'])


    
    