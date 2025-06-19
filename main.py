import click
from pathlib import Path

from generation_of_test_file import generate_test_file_content


@click.command()
@click.option("--project-path",
              type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
              help="Path of the root of the project to be tested")
@click.option("--file-path",
              help="Path of the file to be tested")
@click.option("--test-file-path",
              help="Path of the file where the tests will be stored")
def main(project_path: Path, file_path: str, test_file_path: str) -> None:
    generate_test_file(project_path, file_path, test_file_path)


def generate_test_file(project_path: Path, file_path: str, test_file_path: str) -> None:
    test_file_content = generate_test_file_content(project_path, file_path)
    with open(project_path / test_file_path, "w") as test_file:
        test_file.write(test_file_content)


if __name__ == "__main__":
    main()
