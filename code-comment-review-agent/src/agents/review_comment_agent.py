# code-review-agent/agents/review_agent.py
from langchain.output_parsers import PydanticOutputParser
from src.utils.schema import CodeReviewSchema
from langchain.prompts import PromptTemplate


class ReviewAgent:
    def __init__(self, llm):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=CodeReviewSchema)

    def generate_code_review(self, code: str, structure: str) -> dict:
        prompt = PromptTemplate(
            template="""
            You are a senior software engineer specializing in **code comment quality reviews**. Your task is to review the following Python code **purely based on its comments** and provide a concise, structured JSON output with:

            - **score** (0–100): A numeric rating of how well the code is commented for readability and maintainability.
            - **code_comment** (true/false): Should more comments be added? Return `true` if the code lacks sufficient comments.
            - **feedback**: Short, specific notes about missing, redundant, unclear, or misleading comments.
            - **suggestions**: Precise recommendations for improving comment clarity, relevance, and coverage.
            - **strengths**: Brief points highlighting what’s done well in terms of code commenting.

            **Review only the quality, clarity, sufficiency, and relevance of comments in the code.** Ignore logic, structure, or functionality unless it directly relates to commenting needs.

            You are reviewing the entire codebase at once. DO NOT evaluate file-by-file. Base your score and analysis on the full context provided.

            Project structure:
            {structure}

            Codebase:
            {code}

            Your response must strictly follow the format below. Do not include markdown, explanations, or any extra text. Start your response with '{{' and end with '}}'.

            Output schema:
            {{
            "score": integer,
            "code_comment": boolean,
            "feedback": [string],
            "suggestions": [string],
            "strengths": [string]
            }}

            {format_instructions}
            """
            ,
            input_variables=["structure", "code"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        formatted_prompt = prompt.format(code=code, structure=structure)
        response = self.llm.generate(formatted_prompt)

        return self.parser.parse(response)
