import re
from pathlib import Path
import os

pipeline_path = Path("/Users/admin/Desktop/graduation-thesis/GraduationThesis/src/experiments/document_processing/document_processing_pipeline.py")
content = pipeline_path.read_text()

# 1. Inject functions after call_vlm
functions = """
def classify_visual(image_bytes: bytes) -> str:
    if not os.getenv("OCR_ENABLE_REAL_VISION", "false").lower() == "true":
        return "general_visual"
    prompt = "Classify this image into exactly one of these categories: table_or_matrix, graph_diagram, formula, general_visual, decorative. Output ONLY the category name."
    result = call_vlm(prompt, image_bytes).strip().lower()
    categories = ["table_or_matrix", "graph_diagram", "formula", "general_visual", "decorative"]
    for cat in categories:
        if cat in result:
            return cat
    return "general_visual"

def get_specialized_prompt(category: str) -> str:
    if category == "table_or_matrix":
        return "Extract row labels, column labels, and cell values. Return structured JSON with schema: {schema_version, content_type, row_labels, column_labels, values, notes}. Preserve exact numeric values."
    elif category == "graph_diagram":
        return "Extract node labels, edge list and directionality. Return a structured graph representation in JSON."
    elif category == "formula":
        return "Extract surrounding explanatory text separately from formula text. Return formulas in LaTeX."
    elif category == "decorative":
        return "This is a decorative image. Describe it minimally."
    else:
        return "Describe this visual element, focusing only on content that contributes to learning value. Avoid filler commentary about style."

def rule_based_cleanup(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cleaned = []
    for b in blocks:
        if b["kind"] == "text":
            text = b.get("content", "")
            text = text.replace("Here's a description", "").replace("Here is the table", "").replace("```json", "").replace("```", "")
            if "image_url" in text:
                text = text.replace("image_url", "")
            b_new = dict(b)
            b_new["content"] = text
            cleaned.append(b_new)
        else:
            cleaned.append(b)
    return cleaned

def llm_based_normalization(blocks: list[dict[str, Any]]) -> str:
    if not os.getenv("OCR_ENABLE_REAL_VISION", "false").lower() == "true":
        return "[VISION_PLACEHOLDER] Normalization skipped."
    combined = "\\n\\n".join([b.get("content", "") for b in blocks if b["kind"] == "text"])
    if not combined.strip():
        return "[EMPTY_OUTPUT]"
    prompt = f"Normalize the following extracted text into clean, coherent Markdown. Merge adjacent segments logically. Preserve exact meaning, tables, and formulas. Do not add explanatory prose.\\n\\n{combined}"
    return call_vlm(prompt)

"""

if "def classify_visual" not in content:
    content = content.replace("def extract_pdf_text", functions + "def extract_pdf_text")

# 2. Patch extract_pdf_text
content = content.replace(
    'prompt_text = "Describe this diagram/table/image from a PDF and convert to markdown."',
    'cat = classify_visual(image_bytes)\n                prompt_text = get_specialized_prompt(cat)'
)

# 3. Patch extract_pptx_text
content = content.replace(
    'prompt_text = "Describe this slide image and convert to markdown notes."',
    'cat = classify_visual(image_bytes)\n                    prompt_text = get_specialized_prompt(cat)'
)

# 4. Patch extract_image_text
old_extract_image = """    prompt_text = "Perform OCR and describe any table/formula/diagram in markdown format."
    
    if enable_real_vision:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        content = call_vlm(prompt_text, image_bytes)"""
new_extract_image = """    if enable_real_vision:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        cat = classify_visual(image_bytes)
        prompt_text = get_specialized_prompt(cat) + " Also perform OCR on any text."
        content = call_vlm(prompt_text, image_bytes)"""
if old_extract_image in content:
    content = content.replace(old_extract_image, new_extract_image)
else:
    print("Warning: extract_image_text not patched!")

# 5. Patch run_mode
old_run_mode = """            result_md = merge_blocks_to_markdown(sample_id, entry["input_path"], blocks)
            write_text(sample_root / "result.md", result_md)"""

new_run_mode = """            result_md = merge_blocks_to_markdown(sample_id, entry["input_path"], blocks)
            write_text(sample_root / "raw_result.md", result_md)
            
            cleaned_blocks = rule_based_cleanup(blocks)
            normalized_md = llm_based_normalization(cleaned_blocks)
            write_text(sample_root / "normalized_result.md", normalized_md)
            write_text(sample_root / "result.md", normalized_md)
            
            structured_data = {}
            for b in blocks:
                if b["kind"] == "text" and "schema_version" in str(b.get("content", "")):
                    try:
                        import re
                        match = re.search(r'\\{.*\\}', str(b["content"]), re.DOTALL)
                        if match:
                            import json
                            structured_data = json.loads(match.group(0))
                    except Exception:
                        pass
            write_json(sample_root / "structured.json", structured_data)
            write_json(sample_root / "normalization_trace.json", {"cleaned_blocks": cleaned_blocks})"""

if old_run_mode in content:
    content = content.replace(old_run_mode, new_run_mode)
else:
    print("Warning: run_mode not patched!")

pipeline_path.write_text(content)
print("Patch applied.")
