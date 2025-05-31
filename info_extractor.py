import os
import base64
import json
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Extraction Prompt ---
detailed_prompt = """
You are a highly accurate document parser tasked with extracting every single row from a table labeled “DESIGNED APPURTENANCE LOADING”. The table structure is either a **two-column** or **one-column** layout, where each column contains two subcolumns labeled:
- TYPE
- ELEVATION

These are tabular entries, often listing items like antennas or mounts with optional carrier or quantity information embedded in brackets.

Your job is to:
1. Carefully scan and extract **ALL rows** from both left and right columns (if both exist), row by row, without missing a single entry.
2.If there is 2 colums then extract all the information from left column then go to right column.
2. Extract each row’s details precisely based on the **text shown in the TYPE and ELEVATION columns**.
3. Treat each pair of TYPE and ELEVATION as one unique item. If either is missing, skip the row.
4. For the TYPE column, follow this breakdown:

    **Field Extraction Logic:**
    - **Qty**: If TYPE starts with a number in parentheses, like “(2)”, that number is the quantity. If missing, default Qty = 1.
    - **Type**: This is the core description **excluding any parentheses**, such as equipment type or model name.
    - **Carrier/Note**: If the last part of the TYPE string includes a name inside parentheses (like “(Verizon)”), that is the carrier or note. If not present, return null.

5. The ELEVATION value should be taken exactly as shown and converted to an integer if possible (e.g., “195” → 195). If elevation is unclear or missing, return null.

---

IMPORTANT RULES:
- Do NOT merge, reorder, or summarize any rows.
- Do NOT infer or assume values.
- If any value cannot be determined from the image, return **null**.
- Extract the values **exactly as shown**, cleaned of parentheses for `Type` and `Carrier`.

---

EXTRACTION FORMAT:
Return a valid JSON list. Each row should follow this format:

[
  {
    "Serial": 1,
    "Qty": 2,
    "Type": "Commscope NHH-65C-R2B w/MP",
    "Carrier": "Verizon",
    "Elevation": 195
  },
  {
    "Serial": 2,
    "Qty": 1,
    "Type": "Raycap DC-12 Surge Suppressor",
    "Carrier": null,
    "Elevation": 175
  }
  // More rows...
]

---

Only return valid JSON. Do NOT include any explanations, comments, or markdown formatting like ```json. If no valid rows are found, return an empty list: `[]`.
"""

# --- Extract Data from Image ---
def extract_from_image(image_path):
    with open(image_path, "rb") as img_file:
        image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")
    response = model.generate_content(
        [detailed_prompt, {"mime_type": "image/png", "data": image_base64}],
        generation_config={"temperature": 0.2}
    )

    text = response.text.strip().strip("```json").strip("```")

    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        if start == -1 or end == 0:
            raise ValueError("JSON list not found")
        items = json.loads(text[start:end])
    except Exception as e:
        print(f"Error parsing JSON for {image_path}: {e}")
        return []
    return items

# --- Save to Excel and JSON ---
def save_outputs(items, base_name, output_dir=None):
    df = pd.DataFrame(items)
    df["Serial"] = range(1, len(df) + 1)

    expected_columns = ["Serial", "Qty", "Type", "Carrier", "Elevation"]
    df = df[[col for col in expected_columns if col in df.columns] + 
            [col for col in df.columns if col not in expected_columns]]

    # Set output directory to root/Output if not specified
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Output")
    os.makedirs(output_dir, exist_ok=True)

    excel_path = os.path.join(output_dir, f"{base_name}.xlsx")
    json_path = os.path.join(output_dir, f"{base_name}.json")

    df.to_excel(excel_path, index=False)
    df.to_json(json_path, orient="records", indent=2)

    print(f"✅ Saved: {excel_path} and {json_path}")

# --- Main Batch Processor ---
if __name__ == "__main__":
    image_folder = "DA_Loading_OCR"

    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(image_folder, filename)
            base_name = os.path.splitext(filename)[0]
            # Output to root/Output
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Output")

            print(f"🔍 Processing {filename}...")
            items = extract_from_image(image_path)
            if items:
                save_outputs(items, base_name, output_dir)
            else:
                print(f"⚠️ No data extracted from {filename}")
