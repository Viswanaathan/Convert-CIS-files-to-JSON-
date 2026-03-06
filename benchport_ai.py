import pdfplumber
import openai
import json

openai.api_key = "YOUR_API_KEY_HERE"

def extract_rules(pdf_path):
    rules = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                rules.append(text)
    return rules

def enhance_with_ai(extracted_text):
    prompt = f"""
    Convert this CIS benchmark rule to JSON format:
    Rule text: {extracted_text}

    Output format:
    {{
        "rule_id": "...",
        "description": "...",
        "resource_type": "...",
        "condition": {{...}},
        "severity": "..."
    }}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    content = response.choices[0].message["content"]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"raw_output": content}

def main():
    pdf_path = "CIS_Benchmark.pdf"
    rules = extract_rules(pdf_path)
    results = []
    for rule in rules[:5]:
        structured = enhance_with_ai(rule)
        results.append(structured)
    with open("cis_rules.json", "w") as f:
        json.dump(results, f, indent=2)
    print("✅ Saved results to cis_rules.json")

if __name__ == "__main__":
    main()
