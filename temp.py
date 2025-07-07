import json
from typing import List

def convert_jsonl_line(line: str) -> str:
    entry = json.loads(line)
    for msg in entry.get("messages", []):
        if msg.get("role") == "assistant":
            content = msg["content"].strip()
            # classify type
            if '$' in content:
                t = "currency"
            elif '%' in content:
                t = "percentage"
            else:
                try:
                    int(content.replace(",", ""))
                    t = "number"
                except ValueError:
                    t = "text"
            msg["content"] = f"'''json{{\"{t}\": \"{content}\"}}'''"
            break
    return json.dumps(entry, ensure_ascii=False)


def convert_jsonl_file(input_path: str, output_path: str) -> None:
    """
    Read a JSONL file, try several encodings to decode it, convert each valid JSON line,
    and write results to output. Skips lines that don't parse as JSON.
    """
    encodings = ("utf-8-sig", "utf-16", "latin-1")
    for enc in encodings:
        try:
            with open(input_path, 'r', encoding=enc) as fin:
                fin.readline()  # try reading one line
            chosen_enc = enc
            print(f"⮕ Successfully opened with encoding: {enc}")
            break
        except Exception as e:
            print(f"⚠️  Cannot open with {enc}: {e}")
    else:
        raise RuntimeError(f"All encoding attempts failed for {input_path}")

    with open(input_path, 'r', encoding=chosen_enc) as fin, \
         open(output_path, 'w', encoding='utf-8') as fout:
        for raw in fin:
            line = raw.strip()
            if not line:
                continue
            try:
                converted = convert_jsonl_line(line)
                fout.write(converted + "\n")
            except json.JSONDecodeError:
                print(f"⚠️  Skipping invalid JSON line: {line[:50]}...")
                continue


convert_jsonl_file('sample_data/auryn_qna.jsonl', 'output101.jsonl')
print("Function `convert_jsonl_file(input_path, output_path)` is ready to use.")
