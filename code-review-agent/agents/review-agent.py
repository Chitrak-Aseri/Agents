# code-review-agent/agents/review-agent.py
class ReviewAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_code_review(self, code: str, structure: str) -> str:
        prompt = f"""
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
        """

        response = self.llm.generate(prompt)
        return response
