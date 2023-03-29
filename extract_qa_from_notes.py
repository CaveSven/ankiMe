import os
import csv
import re
import markdown
import argparse


def generate_qa_csv(source_dir, csv_path):
    # Regular expression to extract questions and answers
    regex = r'\* \*Q\*: (.+)\n\s+\* \*A\*: ([\s\S]+?)(?=\n\s+\* \*Q\*:|\Z)'

    # Initialize list to store question-answer pairs
    qa_pairs = []

    # Loop over files in source directory
    for filename in os.listdir(source_dir):
        # Check if file is a Markdown file
        if filename.endswith('.txt'):
            # Read Markdown content from file
            with open(os.path.join(source_dir, filename), 'r') as f:
                markdown_content = f.read()

            # Extract questions and answers from Markdown content
            file_qa_pairs = re.findall(regex, markdown_content, flags=re.MULTILINE)
            # Convert Markdown-formatted answer to HTML
            file_qa_pairs_html = [(q, markdown.markdown(a)) for q, a in file_qa_pairs]
            # Append question-answer pairs to overall list
            qa_pairs.extend(file_qa_pairs_html)

    # Write question and answer data to CSV file with ";" delimiter
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['Q', 'A'])
        writer.writerows(qa_pairs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate CSV file from Markdown question-answer pairs.')
    parser.add_argument('source_dir', type=str, help='Path to source directory containing Markdown files.')
    parser.add_argument('csv_path', type=str, help='Path to output CSV file.')
    args = parser.parse_args()
    generate_qa_csv(args.source_dir, args.csv_path)
