#!/usr/bin/env python3
import json
import argparse

def process_file(input_path: str, output_path: str, end_token: str = "<|end|>"):
    """
    Reads a JSONL from input_path, appends end_token to every assistant
    message's content, and writes the result to output_path.
    """
    with open(input_path, 'r', encoding='utf-8') as fin, \
         open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            if not line.strip():
                continue
            record = json.loads(line)
            # Only modify if there's a 'messages' list
            if 'messages' in record and isinstance(record['messages'], list):
                for msg in record['messages']:
                    if msg.get('role') == 'assistant' and 'content' in msg:
                        # Append the end token if not already present
                        if not msg['content'].endswith(end_token):
                            msg['content'] = msg['content'] + end_token
            # Write back out as one JSON object per line
            fout.write(json.dumps(record, ensure_ascii=False))
            fout.write("\n")

def main():
    parser = argparse.ArgumentParser(
        description="Append an end-of-message token to every assistant message in a JSONL chat dataset."
    )
    parser.add_argument(
        "input",
        help="Path to input JSONL file (one JSON object per line)."
    )
    parser.add_argument(
        "output",
        help="Path where the modified JSONL will be written."
    )
    parser.add_argument(
        "--token",
        default="<|end|>",
        help="The token to append to assistant messages (default: \"<|end|>\")."
    )
    args = parser.parse_args()

    process_file(args.input, args.output, end_token=args.token)
    print(f"Done! Modified file written to: {args.output}")

if __name__ == "__main__":
    main()
