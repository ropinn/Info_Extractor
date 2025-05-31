# 📦 Info Extractor (Image → JSON/Excel)

**Info Extractor** is a powerful AI-driven tool that extracts structured data from engineering images — specifically those containing **"DESIGNED APPURTENANCE LOADING"** tables. It uses the **Google Gemini API** (Generative AI) to detect and parse the tables, then converts the extracted content into clean, standardized **Excel** and **JSON** files.

Each image is processed independently. Results are saved inside individual folders, automatically named after the image file. This design is ideal for batch processing telecom site documents, structural records, or civil engineering loading data.

---

## 📌 Use Case

**Info Extractor** was built for use cases like:

- 📶 Telecom tower appurtenance loading sheets
- 🏗️ Antenna mounting configuration docs
- 🛠️ Structural/civil engineering forms containing TYPE and ELEVATION data
- 🔍 OCR-based data digitization from scanned plans or PDF extractions

---

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| 🔍 Intelligent Extraction | Uses Gemini AI to extract data from structured tables |
| 📊 Format Output | Exports both Excel (`.xlsx`) and JSON (`.json`) |
| 📁 Folder Organization | Each image gets its own output folder |
| ⚡ Batch Ready | Processes entire directories of images |
| 🔢 Auto-serial Numbers | Adds `Serial` numbers automatically for traceability |
| 🧠 Custom Prompting | Designed to follow strict extraction rules to avoid missed data |

---

## 🖼️ Supported Input

- PNG, JPG, JPEG image formats
- One-column and two-column "TYPE / ELEVATION" tables
- Quantity values formatted like `(2)`, carriers like `(Verizon)` inside `TYPE` cells

---

## 📂 Output Folder Structure

For each image `example.png`, the following folder is created:

```
DA_Loading_OCR/
├── example.png
├── example/
│   ├── example.xlsx
│   └── example.json
```

---

## 🧠 Output Format (JSON)

Each row represents a unique appurtenance loading entry extracted from the table.

```json
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
]
```

---

## 🧑‍💻 Tech Stack

- **Python 3.x**
- **Google Gemini API (via `google-generativeai`)**
- `pandas`
- `openpyxl`
- `python-dotenv`

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/info-extractor.git
cd info-extractor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> Example `requirements.txt`:
```
pandas
openpyxl
python-dotenv
google-generativeai
```

### 3. Configure Your Gemini API Key

Create a `.env` file in the project root and add your API key:

```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

---

## 🚀 Usage

### 1. Prepare Input

Place all your input images in the `DA_Loading_OCR/` folder:

```
DA_Loading_OCR/
├── site1.png
├── site2.jpg
```

### 2. Run the Extractor

```bash
python info_extractor.py
```

### 3. View the Output

Each image will be processed and saved in its own folder like:

```
DA_Loading_OCR/
├── site1/
│   ├── site1.xlsx
│   └── site1.json
```

---

## 🛡️ Extraction Logic Summary

Each entry from the TYPE + ELEVATION columns is parsed based on:

| Field     | Extraction Rule |
|-----------|-----------------|
| **Qty**   | If TYPE starts with (X), X is used as quantity. Else, defaults to 1. |
| **Type**  | Extracted from TYPE text, excluding all bracketed parts |
| **Carrier** | The last bracketed part in TYPE, if present, is used as Carrier |
| **Elevation** | Extracted as-is from the ELEVATION column, converted to integer |

---

## ❗ Important Notes

- Input images must clearly show the table (cropped scans work best)
- Rows where either TYPE or ELEVATION is missing are skipped
- Do **not** rename files during processing to avoid folder mismatches

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

---

## 📄 License

MIT License © 2025 [Your Name]

---

## 📫 Contact

For questions or support, email: `your.email@example.com`
