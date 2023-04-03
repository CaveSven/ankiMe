import argparse
import csv
import os

from markdown import markdown


def generate_qa_csv(source_dir, csv_path):
    # Define header and open CSV file for writing
    header = ['Question', 'Answer', 'Source']
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        # Write header as comment
        writer.writerow(['# ' + ', '.join(header)])

        # Iterate over files in source directory
        for filename in os.listdir(source_dir):
            # Ignore non-Markdown files
            if not filename.endswith('.md'):
                continue

            # Parse Markdown file
            with open(os.path.join(source_dir, filename), 'r') as f:
                md_content = f.read()

            # Find question and answer in Markdown code block
            md_question = md_content.find('```md ankiMe\n')
            if md_question == -1:
                # Markdown code block not found, skip file
                continue

            # Extract question and answer from Markdown code block
            md_question_end = md_content.find('\n', md_question) + 1
            md_answer = md_content[md_question_end:].strip()
            question = md_content[md_question_end:md_answer.find('\n') + md_question_end].strip()
            answer = md_answer[len(question):].strip()
            answer = answer[:-3].strip() if answer.endswith('\n```') else answer

            # Append question, answer, and filename to CSV file
            writer.writerow([question, markdown(answer), filename])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate CSV file from Markdown question-answer pairs.')
    parser.add_argument('source_dir', type=str, help='Path to source directory containing Markdown files.')
    parser.add_argument('csv_path', type=str, help='Path to output CSV file.')
    args = parser.parse_args()
    generate_qa_csv(args.source_dir, args.csv_path)
