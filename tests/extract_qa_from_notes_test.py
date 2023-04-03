import csv
import os
import unittest
from tempfile import NamedTemporaryFile

from src.ankime.extract_qa_from_notes import generate_qa_csv


class TestGenerateQACsv(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory and some test files
        self.tmp_dir = 'test_source_dir'
        os.mkdir(self.tmp_dir)
        self.test_files = [
            {
                'name': 'test1.md',
                'content': 'some text\n```md ankiMe\nWhat is the capital of France?\nParis\n```'
            },
            {
                'name': 'test2.md',
                'content': 'some text\n```md ankiMe\nWhat is 1+1?\n2\n```'
            },
            {
                'name': 'not_a_markdown_file.txt',
                'content': 'some text'
            },
            {
                'name': 'no_question.md',
                'content': 'some text\n```md ankiMe\n\nanswer\n```'
            },
            {
                'name': 'multi_line_answer.md',
                'content': 'some text\n```md ankiMe\nWhat is the capital of India?\nNew Delhi\nis the capital of India.\n```'
            },
            {
                'name': 'multi_q_and_a.md',
                'content': 'some text\n```md ankiMe\nWhat is the capital of Germany?\nBerlin\n```\n```md ankiMe\nWhat is the capital of Spain?\nMadrid\n```'
            },
            {
                'name': 'no_code_block.md',
                'content': 'some text\n'
            }
        ]
        for file in self.test_files:
            with open(os.path.join(self.tmp_dir, file['name']), 'w') as f:
                f.write(file['content'])

    def tearDown(self):
        # Remove temporary directory and files
        for file in self.test_files:
            os.remove(os.path.join(self.tmp_dir, file['name']))
        os.rmdir(self.tmp_dir)

    def test_generate_qa_csv(self):
        # Define expected output
        expected_output = [
            ['# Question, Answer, Source'],
            ['What is 1+1?', '<p>2</p>', 'test2.md'],
            ['What is the capital of France?', '<p>Paris</p>', 'test1.md'],
            ['What is the capital of India?', '<p>New Delhi\nis the capital of India.</p>', 'multi_line_answer.md'],
            ['What is the capital of Germany?', '<p>Berlin</p>', 'multi_q_and_a.md'],
            ['What is the capital of Spain?', '<p>Madrid</p>', 'multi_q_and_a.md'],
        ]

        # Generate CSV file using the function
        with NamedTemporaryFile(mode='w', delete=False) as f:
            csv_path = f.name
            generate_qa_csv(self.tmp_dir, csv_path)

        # Read CSV file and check that it matches the expected output
        with open(csv_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            actual_output = [row for row in reader]

        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
