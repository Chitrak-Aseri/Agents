# bot/agents/comment_agent.py
class CodeCommentAgent:
    """Agent for generating comments and docstrings for various code types (Python, SQL, Jupyter notebooks)."""
    
    def __init__(self, llm):
        """Initialize the comment agent with an LLM instance.
        
        Args:
            llm: Language model instance used for generating comments
        """
        self.llm = llm

    def generate_comment_for_python(self, code: str) -> str:
        """Generate Python docstrings and comments for the given code.
        
        Args:
            code: Python source code to be commented
            
        Returns:
            str: The original code with added docstrings and comments
        """
        

        prompt = f"""
        You are a Python expert code reviewer.

        Your job is to annotate the given Python source code by:
        - Inserting or updating docstrings for all functions, classes, and modules.
        - Adding helpful inline comments only where necessary (for non-obvious logic).
        - **Never** modifying or uncommenting any code (especially if it is commented out).
        - **Never** changing any logic, even if it seems broken.
        - **Never** reformatting large code sections.
        - Preserve all original indentation, spacing, and comments exactly as-is.

        ⚠️ **Critical Output Rules**:
        - Return only the **full Python source code** with added docstrings and inline comments.
        - Do **not** change or uncomment existing `#` comments or commented-out code.
        - Do **not** output anything except the raw Python code.
        - Do **not** use Markdown (` ``` ` or `python`), no prose, no explanations.
        - If the input contains only commented-out code or blank content, return exactly the same input — unchanged.

        Here is the code:

        {code}

        🔁 Repeat: Only return the fully annotated Python source code as plain text. No markdown. No explanations. No changes to existing logic or commented code. No blank lines removed. Do not try to fix or uncomment anything. Preserve all existing structure exactly as-is.
        """

        response = self.llm.generate(prompt)
        return response

    def generate_comment_for_sql(self, code: str) -> str:
        """Generate SQL comments for the given query.
        
        Args:
            code: SQL query to be commented
            
        Returns:
            str: The original SQL with added comments
        """
        prompt = f"""
        You are an expert SQL code annotator.

        Your task is to add **concise and meaningful inline comments** to the given SQL query. Only comment on non-trivial logic such as joins, subqueries, aggregations, filters, or expressions. Do **not** comment on simple SELECTs, FROMs, or aliases unless there is useful context to add.

        ❗️**Output Requirements**:
        - Return the SQL code as plain text only (no Markdown formatting).
        - Do NOT include code blocks (no triple backticks).
        - Do NOT add any prose, headings, or explanations before or after the SQL.
        - Keep all comments inline, using `--` after the relevant line of code.

        Here is the SQL query to annotate:

        {code}

        Now return ONLY the annotated SQL query as plain text.
        """
    
        response = self.llm.generate(prompt)
        return response
    
    def generate_comment_for_ipynb(self, nb_node) -> dict:
        """Generate comments for all code cells in a Jupyter notebook.
        
        Args:
            nb_node: Jupyter notebook node object
            
        Returns:
            dict: Modified notebook with commented code cells
        """
        modified_nb = nb_node.copy()
        for cell in modified_nb.cells:
            if cell.cell_type == 'code' and cell.source.strip():  # Only process non-empty code cells
                commented_code = self.generate_comment_for_python(cell.source)
                cell.source = commented_code
        return modified_nb