# OCR Result: database_scanned

Source: `src/experiments/document_processing/test_data/Database-giữa kì cô Oanh.pdf`

## Segment 1

To tackle this problem, we'll break it down into steps that involve detecting different regions on the scanned mixed-layout page and then extracting information from those regions. The process involves:

1. **Pre-processing**: Cleaning up the scanned page to enhance image quality.
2. **Region Detection**: Identifying table-like regions, graph/diagram regions, handwritten annotations, and body text areas.
3. **Region-based OCR (Optical Character Recognition)**: Applying OCR to each type of region.
4. **Structured Data Extraction**: Converting detected regions into structured JSON format.
5. **Merging Results**: Combining extracted data in an approximate reading order.

### Step 1: Pre-processing

- **Binarization**: Convert the image to black and white to enhance contrast.
- **Noise Removal**: Apply filters to remove noise.
- **Deskewing**: Straighten the image if it's skewed.

### Step 2: Region Detection

- **Table Detection**: Use algorithms like table detection via borders, or learning-based approaches to identify table regions.
- **Graph/Diagram Detection**: Typically involves identifying non-text regions with possible geometric shapes or images.
- **Handwritten Annotation Detection**: Distinguishing handwritten text from typed text, often requiring machine learning models trained on annotated datasets.
- **Body Text Detection**: Identifying large blocks of text.

### Step 3: Region-based OCR

- **Apply OCR**: Use an OCR engine (like Tesseract) on detected text regions. For handwritten annotations, use handwritten text recognition tools if available.

### Step 4: Structured Data Extraction

- **Tables to JSON**: Convert detected tables into JSON format, preserving row and column structures.
- **Graphs/Diagrams to JSON**: Describe graphs/diagrams in JSON, potentially including axes, labels, and noted data points.
- **Handwritten Annotations**: Store as-is in JSON with a note that they are handwritten.

### Step 5: Merging Results

- **Reading Order Detection**: Approximate the reading order based on the spatial locations and sizes of the regions.
- **Combine Data**: Merge body text, table data, graph/diagram descriptions, and handwritten annotations in the detected reading order.

### Implementation Example (Conceptual)

```python
import json
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np

def detect_tables(image_path):
    # Placeholder for table detection logic
    pass

def detect_graphs(image_path):
    # Placeholder for graph detection logic
    pass

def detect_handwritten_annotations(image_path):
    # Placeholder for handwritten annotation detection logic
    pass

def extract_body_text(image_path):
    # Placeholder for body text extraction logic
    pass

def convert_to_json(data, type):
    if type == 'table':
        # Logic to convert table to JSON
        return json.dumps(data)
    elif type == 'graph':
        # Logic to convert graph to JSON
        return json.dumps(data)

def main():
    image_path = 'path_to_your_image.jpg'
    image = cv2.imread(image_path)

    tables = detect_tables(image_path)
    graphs = detect_graphs(image_path)
    handwritten_annotations = detect_handwritten_annotations(image_path)
    body_text = extract_body_text(image_path)

    table_json = convert_to_json(tables, 'table')
    graph_json = convert_to_json(graphs, 'graph')

    # Combine and output
    output = {
        'body_text': body_text,
        'tables': json.loads(table_json),
        'graphs': json.loads(graph_json),
        'handwritten_annotations': handwritten_annotations
    }

    print(json.dumps(output))

if __name__ == "__main__":
    main()
```

### Note

The actual implementation requires detailed knowledge of image processing (OpenCV, Pillow), OCR (Tesseract), and machine learning (scikit-learn, PyTorch). The provided code is a conceptual placeholder and would need significant expansion to perform the tasks described. Libraries like `camelot` or `tabula-py` for table detection, and `scikit-image` for image processing, could be particularly useful.

## Segment 2

To tackle this problem, we'll break it down into steps that involve detecting different regions on the scanned mixed-layout page and then performing OCR (Optical Character Recognition) on those regions accordingly. The goal is to extract table-like regions, graph/diagram regions, handwritten annotations, and body text, and then merge them back in an approximate reading order.

### Step 1: Preprocessing

- **Cleaning:** Remove any noise from the scanned page to improve OCR accuracy.
- **Deskewing:** If the page is skewed, straighten it to ensure accurate region detection.

### Step 2: Detecting Table-like Regions

- **Approach:** Use algorithms like `camelot` or `tabula` which are specifically designed for table detection and extraction in PDFs and images.
- **Output:** Convert detected tables into structured JSON, preserving row and column structures.

Example JSON Output for a Table:
```json
{
  "tables": [
    {
      "rows": [
        ["Column1", "Column2"],
        ["Cell1", "Cell2"],
        ["Cell3", "Cell4"]
      ]
    }
  ]
}
```

### Step 3: Detecting Graph/Diagram Regions

- **Approach:** Use image processing techniques to segment out images. Tools like OpenCV can help in detecting and isolating these regions.
- **Output:** Save graph/diagram regions as images and describe them in structured JSON, including their position on the page.

Example JSON Output for a Graph/Diagram:
```json
{
  "graphs": [
    {
      "image": "graph1.png",
      "description": "A line graph showing...",
      "position": "top-right"
    }
  ]
}
```

### Step 4: Detecting Handwritten Annotations

- **Approach:** Use machine learning models trained to distinguish between handwritten text and printed text or utilize specific annotation detection algorithms.
- **Output:** Extract handwritten annotations as text (if possible) or images and note their locations.

Example JSON Output for Handwritten Annotations:
```json
{
  "annotations": [
    {
      "text": "Note: This is important!",
      "position": "bottom-left",
      "confidence": 0.8
    }
  ]
}
```

### Step 5: Extracting Body Text

- **Approach:** Apply general OCR using tools like `Tesseract-OCR` on the remaining regions not classified as tables, graphs, or annotations.
- **Output:** Structured text.

### Step 6: Merging Content

- **Approach:** Use the detected positions of each content type to approximate the reading order. This might involve sorting based on the y-coordinate and then the x-coordinate for elements on the page.

### Implementation Example

Below is a simplified Python example using OpenCV and Pytesseract for basic detection and extraction:

```python
import cv2
import pytesseract
import json

def extract_tables(image_path):
    # Implement table detection logic here
    pass

def extract_graphs(image_path):
    # Implement graph detection logic here
    pass

def extract_annotations(image_path):
    # Implement annotation detection logic here
    pass

def extract_body_text(image_path):
    # Implement body text extraction logic here
    text = pytesseract.image_to_string(cv2.imread(image_path))
    return text

def main():
    image_path = "path_to_your_image.jpg"
    tables = extract_tables(image_path)
    graphs = extract_graphs(image_path)
    annotations = extract_annotations(image_path)
    body_text = extract_body_text(image_path)

    output = {
        "tables": tables,
        "graphs": graphs,
        "annotations": annotations,
        "body_text": body_text
    }

    with open('output.json', 'w') as f:
        json.dump(output, f)

if __name__ == "__main__":
    main()
```

### Note

- The actual implementation details for table, graph, and annotation detection are highly dependent on the specific characteristics of your documents and may require significant development.
- This example provides a conceptual overview. Real-world applications may need to handle more complexity, such as multi-column text, overlapping regions, and varied layouts.
