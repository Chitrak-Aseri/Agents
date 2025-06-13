# code-review-agent/agents/review_agent.py
from langchain.output_parsers import PydanticOutputParser
from code_commenter.utils.schema import CodeReviewSchema
from langchain.prompts import PromptTemplate


class ReviewAgent:
    """A code review agent that evaluates comment quality in Python code.
    
    This agent uses an LLM to analyze code comments and provides structured feedback
    about comment quality, including scores, feedback, and improvement suggestions.
    """
    def __init__(self, llm):
        """Initialize the ReviewAgent with an LLM instance.
        
        Args:
            llm: The language model instance to use for generating reviews.
        """
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=CodeReviewSchema)

    def generate_code_review(self, code: str, structure: str) -> dict:
        """Generate a code review focused on comment quality.
        
        Args:
            code: The Python code to be reviewed (as a string).
            structure: Description of the project structure for context.
            
        Returns:
            dict: Parsed review output containing score, feedback, and suggestions.
        """
        prompt = PromptTemplate(
            template="""
            You are a senior software engineer specializing in **code comment quality reviews**. Review the following Python code **only for its commenting quality**, and return a concise JSON with the fields:

            - **score**: An integer (0–100) representing how well the code is commented.
            - **code_comment**: A boolean indicating whether more comments are needed (`true` if additional comments are recommended).
            - **feedback**: A list of short, specific observations about comment issues (missing, redundant, unclear).
            - **suggestions**: Clear improvements for enhancing code comments (clarity, coverage, precision).
            - **strengths**: Highlights of well-commented aspects of the code.

            ⚠️ **Only review code comments** — do not evaluate code logic, syntax, or functionality unless it directly relates to comment quality.

            You are reviewing all files together, not individually. Base your score and feedback on the entire codebase context.

            Project Structure:
            {structure}

            Codebase:
            {code}

            Respond only with valid JSON (no markdown or extra text). Output must begin with `{{` and end with `}}`.

            Expected Output:
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