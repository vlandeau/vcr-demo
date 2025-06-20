import subprocess
import pytest

from pathlib import Path
from main import generate_test_file
from models import Model


@pytest.mark.vcr()
def test_generate_test_file_should_generate_a_working_test_file_with_openai():
    # Given
    project_path = Path("resources/fibonacci")
    project_path.mkdir(parents=True, exist_ok=True)
    file_path = "fibonacci.py"
    file_content = """
def fibonacci(n: int) -> int:
    if n < 0: #xxx
        raise ValueError("Input cannot be negative")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
"""
    with open(project_path / file_path, "w") as file:
        file.write(file_content)
    test_file_path = "test_fibonacci.py"
    init_file = project_path / "__init__.py"
    init_file.touch()
    model = Model.OPENAI

    # When
    try:
        generate_test_file(project_path, file_path, test_file_path, model)

        # Then
        test_result = subprocess.run(["cd", str(project_path), "&", "pytest", test_file_path], check=True)
        assert test_result.returncode == 0, "Tests failed, check the implementation or generated tests."
    finally:
        (project_path / file_path).unlink()
        if (project_path / test_file_path).exists():
            (project_path / test_file_path).unlink()
        init_file.unlink()



@pytest.mark.vcr()
def test_generate_test_file_should_generate_a_working_test_file_with_ollama():
    # Given
    project_path = Path("resources/fibonacci")
    project_path.mkdir(parents=True, exist_ok=True)
    file_path = "fibonacci.py"
    file_content = """
def fibonacci(n: int) -> int:
    if n < 0: #xxx
        raise ValueError("Input cannot be negative")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
"""
    with open(project_path / file_path, "w") as file:
        file.write(file_content)
    test_file_path = "test_fibonacci.py"
    init_file = project_path / "__init__.py"
    init_file.touch()
    model = Model.OLLAMA

    # When
    try:
        generate_test_file(project_path, file_path, test_file_path, model)

        # Then
        test_result = subprocess.run(["cd", str(project_path), "&", "pytest", test_file_path], check=True)
        assert test_result.returncode == 0, "Tests failed, check the implementation or generated tests."
    finally:
        (project_path / file_path).unlink()
        if (project_path / test_file_path).exists():
            (project_path / test_file_path).unlink()
        init_file.unlink()
