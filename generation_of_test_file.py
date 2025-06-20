from pathlib import Path

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field


MODEL_NAME = "gemma3:12b"


class GeneratedTestFileContent(BaseModel):
    content: str = Field(
        description="The content of the generated test file.",
        example="def test_example():\n    assert True",
    )
    test_file_description: str = Field(
        description="A brief description of the test file.",
        example="This test file contains unit tests for the example module.",
    )


def generate_test_file_content(project_path: Path, file_path: str) -> str:
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

    model = ChatOllama(model=MODEL_NAME)
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
