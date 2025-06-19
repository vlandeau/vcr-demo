import click

from generation_of_test_file import generate_test_file_content


@click.command()
@click.option("--file-path", help="Path of the file to be tested")
@click.option("--test-file-path", help="Path of the file where the tests will be stored")
def main(file_path: str, test_file_path: str) -> None:
    generate_test_file(file_path, test_file_path)


def generate_test_file(file_path: str, test_file_path: str) -> None:
    test_file_content = generate_test_file_content(file_path)
    with open(test_file_path, "w") as test_file:
        test_file.write(test_file_content)


if __name__ == "__main__":
    main()
