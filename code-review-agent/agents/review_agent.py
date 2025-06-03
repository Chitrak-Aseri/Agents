# code-review-agent/agents/review_agent.py
from langchain.output_parsers import PydanticOutputParser
from utils.schema import CodeReviewSchema
from langchain.prompts import PromptTemplate


class ReviewAgent:
    def __init__(self, llm):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=CodeReviewSchema)

    def generate_code_review(self, code: str, structure: str) -> dict:
        prompt = PromptTemplate(
            template="""
            You are a senior code reviewer. Analyze the following python code and return a structured JSON with:

                - score: Overall score from 0 to 100
                - feedback: Detailed list of issues, improvements, and observations
                - suggestions: Possible changes to improve quality
                - strengths: What the code does well

            Always return JSON only. No explanations outside the JSON block.

            Project strct:
            {structure}

            Complete Code-base:

            {code}

            Return the result as valid JSON with keys: "score", "feedback", "suggestions", "strengths"
            {format_instructions}

            NEVER REVIEW THE FILES ONE BY ONE , YOU WOULD REVIEW ALL THE FILES AND STRUCTURE AT ONCE AND THE SCORE IS COMPUTED BASED ON ALL THE FIL.
            ONLY output a JSON object conforming to the following schema. Do not include any code, markdown, explanations, or extra text. Your output MUST start with '{{' and end with '}}'.

            Output schema:
            {{
            "score": integer,
            "feedback": [string],
            "suggestions": [string],
            "strengths": [string]
            }}

            """,
            input_variables=["structure", "code"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        formatted_prompt = prompt.format(code=code, structure=structure)
        response = self.llm.generate(formatted_prompt)

        return self.parser.parse(response)
