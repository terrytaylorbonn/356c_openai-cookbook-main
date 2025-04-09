# from typing import List

# import rich
# from pydantic import BaseModel

# from openai import OpenAI


# class Step(BaseModel):
#     explanation: str
#     output: str


# class MathResponse(BaseModel):
#     steps: List[Step]
#     final_answer: str


# client = OpenAI()

# rsp = client.responses.parse(
#     input="solve 8x + 31 = 2",
#     model="gpt-4o-2024-08-06",
#     text_format=MathResponse,
# )

# for output in rsp.output:
#     if output.type != "message":
#         raise Exception("Unexpected non message")

#     for item in output.content:
#         if item.type != "output_text":
#             raise Exception("unexpected output type")

#         if not item.parsed:
#             raise Exception("Could not parse response")

#         rich.print(item.parsed)

#         print("answer: ", item.parsed.final_answer)

# # or

# message = rsp.output[0]
# assert message.type == "message"

# text = message.content[0]
# assert text.type == "output_text"

# if not text.parsed:
#     raise Exception("Could not parse response")

# rich.print(text.parsed)

# print("answer: ", text.parsed.final_answer)


### THIS IS FROM structure_outputs_tools.py


from enum import Enum
from typing import List, Union

import rich
from pydantic import BaseModel

import openai
from openai import OpenAI


class Table(str, Enum):
    orders = "orders"
    customers = "customers"
    products = "products"


class Column(str, Enum):
    id = "id"
    status = "status"
    expected_delivery_date = "expected_delivery_date"
    delivered_at = "delivered_at"
    shipped_at = "shipped_at"
    ordered_at = "ordered_at"
    canceled_at = "canceled_at"


class Operator(str, Enum):
    eq = "="
    gt = ">"
    lt = "<"
    le = "<="
    ge = ">="
    ne = "!="


class OrderBy(str, Enum):
    asc = "asc"
    desc = "desc"


class DynamicValue(BaseModel):
    type: str  # Add a type field to match the expected input structure
    column_name: str


class Condition(BaseModel):
    column: str
    operator: Operator
    value: Union[str, int, DynamicValue]


class Query(BaseModel):
    table_name: Table
    columns: List[Column]
    conditions: List[Condition]
    order_by: OrderBy


client = OpenAI()

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input="look up all my orders in november of last year that were fulfilled but not delivered on time",
    tools=[
        openai.pydantic_function_tool(Query),
    ],
)

rich.print(response)

function_call = response.output[0]
assert function_call.type == "function_call"
assert isinstance(function_call.parsed_arguments, Query)
print("table name:", function_call.parsed_arguments.table_name)