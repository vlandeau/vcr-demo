import subprocess
import pytest

from pathlib import Path
from main import generate_test_file


@pytest.mark.vcr()
def test_generate_test_file():
    # Given
    folder_path = Path("resources/fibonacci")
    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / "fibonacci.py"
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
    with open(file_path, "w") as file:
        file.write(file_content)
    test_file_path = folder_path / "test_fibonacci.py"
    init_file = folder_path / "__init__.py"
    init_file.touch()

    # When
    try:
        generate_test_file(str(file_path.absolute()), str(test_file_path.absolute()))

        # Then
        test_result = subprocess.run(["pytest", test_file_path], check=True)
        assert test_result.returncode == 0, "Tests failed, check the implementation or generated tests."
    finally:
        file_path.unlink()
        if test_file_path.exists():
            test_file_path.unlink()
        init_file.unlink()
