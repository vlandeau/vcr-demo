import os
from pathlib import Path

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from models import Model
from langchain_ollama import ChatOllama



load_dotenv()

class GeneratedTestFileContent(BaseModel):
    content: str = Field(
        description="The content of the generated test file.",
        example="def test_example():\n    assert True",
    )
    test_file_description: str = Field(
        description="A brief description of the test file.",
        example="This test file contains unit tests for the example module.",
    )


def generate_test_file_content(project_path: Path, file_path: str, model: Model) -> str:
    file_content = _get_file_content(project_path / file_path)

    prompt = f"""Generate a test file for the following code of the file at {file_path}:
```python
{file_content}
```

Please adopt the following conventions:
1. Use pytest as the testing framework.
2. Use descriptive test names.
3. Structure the tests as follows:
# Given
x = 1
y = 2

# When
result = add(x, y)

# Then
assert result == 3
    """

    if model is Model.OLLAMA:
        model = ChatOllama(model=os.environ.get("OLLAMA_MODEL_NAME"))
    else:
        model = ChatOpenAI()
    model_with_structure = model.with_structured_output(GeneratedTestFileContent)

    output = model_with_structure.invoke(input=prompt, stream=False)
    test_file_content = output.content
    return test_file_content


def _get_file_content(file_path: Path) -> str:
    if not file_path.exists():
        raise ValueError(f"File {file_path} does not exist.")
    with open(file_path, "r") as file:
        content = file.read()
    return content
