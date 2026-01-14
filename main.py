import click
import subprocess
from pathlib import Path

from generation_of_test_file import generate_test_file_content, fix_test_file_content
from models import Model


@click.command()
@click.option("--project-path",
              type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
              help="Path of the root of the project to be tested")
@click.option("--file-path",
              help="Path of the file to be tested")
@click.option("--test-file-path",
              help="Path of the file where the tests will be stored")
@click.option("--model", default=Model.OPENAI,
              type=click.Choice([Model.OLLAMA, Model.OPENAI]),
              help="Model to use for generating the test file (ollama or openai). Default is openai.")
@click.option("--max-retries", default=3, type=int,
              help="Maximum number of retries to fix the test file. Default is 3.")
def main(project_path: Path, file_path: str, test_file_path: str, model: Model, max_retries: int) -> None:
    generate_test_file(project_path, file_path, test_file_path, model, max_retries)


def generate_test_file(project_path: Path, file_path: str, test_file_path: str,
                       model: Model = Model.OPENAI, max_retries: int = 3) -> None:
    test_file_content = generate_test_file_content(project_path, file_path, model)
    with open(project_path / test_file_path, "w") as test_file:
        test_file.write(test_file_content)

    for i in range(max_retries):
        result = subprocess.run(["pytest", test_file_path], cwd=project_path, capture_output=True, text=True)
        if result.returncode == 0:
            print("Tests passed successfully.")
            break

        print(f"Tests failed (Attempt {i + 1}/{max_retries}). Fixing...")
        error_message = result.stdout + result.stderr
        test_file_content = fix_test_file_content(project_path, file_path, test_file_content, error_message, model)
        with open(project_path / test_file_path, "w") as test_file:
            test_file.write(test_file_content)
    else:
        print("Max retries reached. Tests failed.")


if __name__ == "__main__":
    main()
