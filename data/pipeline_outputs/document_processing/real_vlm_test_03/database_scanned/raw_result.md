# OCR Result: database_scanned

Source: `src/experiments/document_processing/test_data/Database-giữa kì cô Oanh.pdf`

## Segment 1

To tackle this problem, we'll break it down into steps that involve detecting different regions on the scanned mixed-layout page and then performing OCR (Optical Character Recognition) on those regions accordingly. The goal is to extract table-like regions, graph/diagram regions, handwritten annotations, and body text, and then merge them back in an approximate reading order.

### Step 1: Preprocessing

- **Cleaning:** Remove any noise from the scanned page to improve OCR accuracy.
- **Deskewing:** If the page is skewed, straighten it to ensure accurate region detection.

### Step 2: Detecting Table-like Regions

- **Approach:** Use algorithms like `camelot` or `tabula` which are specifically designed for table detection and extraction in PDFs and images.
- **Output:** Convert detected tables into structured JSON, preserving the table structure (rows, columns).

Example JSON for a table:
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

- **Approach:** Use OpenCV for image processing and analysis. Detect regions that do not contain text or have characteristics of graphs (e.g., axes, lines, legends).
- **Output:** Describe the graph/diagram regions in structured JSON, noting their positions and any discernible information (e.g., labels).

Example JSON for a graph:
```json
{
  "graphs": [
    {
      "description": "Line graph showing...",
      "x_axis_label": "X Axis",
      "y_axis_label": "Y Axis",
      "legend": ["Line1", "Line2"]
    }
  ]
}
```

### Step 4: Detecting Handwritten Annotations

- **Approach:** Train or use a pre-trained model (e.g., from TensorFlow or PyTorch) to distinguish between handwritten and printed text. Alternatively, use a rule-based approach assuming annotations have certain characteristics (e.g., short, cursive).
- **Output:** Store handwritten annotations as is, possibly with location information.

Example JSON for handwritten annotations:
```json
{
  "annotations": [
    {
      "text": "Note: This is important!",
      "location": "Top right corner"
    }
  ]
}
```

### Step 5: Extracting Body Text

- **Approach:** Use general-purpose OCR software (e.g., Tesseract-OCR) on the entire document or regions not classified as tables, graphs, or annotations.
- **Output:** Plain text.

### Step 6: Merging Content

- **Approach:** Arrange the extracted content in a logical reading order. This might involve:
  1. Ordering text blocks based on their spatial locations on the page.
  2. Integrating table and graph descriptions closely with the surrounding body text.

### Implementation

The steps outlined can be implemented using Python with libraries such as:

- **OpenCV** for image processing.
- **Pytesseract** (a Python wrapper for Google’s Tesseract-OCR Engine) for OCR.
- **Camelot** or **Tabula** for table detection.
- **Scikit-image** and **scikit-learn** for more advanced image analysis and machine learning tasks.

### Example Python Snippet

```python
import cv2
import pytesseract
import camelot

def extract_content(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Detect and extract tables
    tables = camelot.read_image(image_path)
    table_data = []
    for table in tables:
        table_data.append(table.df.to_dict(orient='records'))

    # Detect and extract body text
    text = pytesseract.image_to_string(image)

    # ... Implement other steps

    return {"tables": table_data, "text": text}

# Usage
image_path = "path/to/scanned/page.jpg"
content = extract_content(image_path)
print(content)
```

This snippet only scratches the surface. A complete solution requires fleshing out each step with more sophisticated techniques and handling edge cases.

## Segment 2

To tackle this problem, we'll break it down into steps that involve detecting different regions on the scanned mixed-layout page and then extracting information from those regions. The process involves:

1. **Pre-processing**: Cleaning up the scanned page to enhance image quality.
2. **Region Detection**: Identifying table-like regions, graph/diagram regions, handwritten annotations, and body text areas.
3. **Region-based OCR (Optical Character Recognition)**: Applying OCR to each type of region.
4. **Structured JSON Extraction**: Converting detected regions into structured JSON format.
5. **Merging Results**: Combining extracted data in an approximate reading order.

### Step 1: Pre-processing

- **Binarization**: Convert the image to black and white to enhance contrast.
- **Noise Removal**: Apply filters to remove noise.
- **Deskewing**: Straighten the image if it's skewed.

### Step 2: Region Detection

- **Table-like Regions**: Use algorithms that detect grid-like structures, such as:
  - **Grid Detection**: Look for intersecting lines that form a grid.
  - **Table Detection Libraries**: Tesseract, OpenCV, or specialized table detection algorithms.

- **Graph/Diagram Regions**: Detect regions that do not resemble text or tables, focusing on:
  - **Image Segmentation**: Techniques to segment images into components.
  - **Edge Detection**: Find regions with significant edges or lines.

- **Handwritten Annotations**: Identify regions with less structured, cursive, or irregular writing:
  - **Text Analysis**: Compare text characteristics to known handwriting.

- **Body Text**: Detect large blocks of text not contained in tables or diagrams.

### Step 3: Region-based OCR

- **Tesseract OCR**: A popular engine for converting images of text into actual text. It supports various languages and can handle different types of input.

### Step 4: Structured JSON Extraction

- **Table-like Regions**: Represented as JSON arrays of objects, where each object represents a cell.
  ```json
  {
    "tables": [
      {
        "rows": [
          {"cells": ["cell1", "cell2"]},
          {"cells": ["cell3", "cell4"]}
        ]
      }
    ]
  }
  ```

- **Graph/Diagram Regions**: Metadata could include type, contained elements, and relationships.
  ```json
  {
    "diagrams": [
      {
        "type": "flowchart",
        "elements": [
          {"type": "box", "content": "start"},
          {"type": "diamond", "content": "decision"}
        ]
      }
    ]
  }
  ```

- **Handwritten Annotations**: Store the text and possibly an image of the annotation.
  ```json
  {
    "annotations": [
      {
        "text": "example annotation",
        "image": "base64 encoded image"
      }
    ]
  }
  ```

- **Body Text**: Extracted as a string.

### Step 5: Merging Results

The final step involves merging these outputs into a single document that approximates the reading order. This could involve:
- Ordering based on detected positions and known reading patterns (e.g., left to right, top to bottom).
- Prioritizing regions based on detected importance or prominence on the page.

### Example Implementation

Here's a simplified Python example using OpenCV and Pytesseract for OCR:

```python
import cv2
import pytesseract
import json

def detect_tables(image_path):
    # Implement table detection logic here
    pass

def detect_diagrams(image_path):
    # Implement diagram detection logic here
    pass

def detect_annotations(image_path):
    # Implement handwritten annotation detection logic here
    pass

def extract_body_text(image_path):
    # Implement body text extraction logic here
    return pytesseract.image_to_string(cv2.imread(image_path))

def main():
    image_path = 'path_to_your_image.jpg'
    # Pre-processing steps...

    tables = detect_tables(image_path)
    diagrams = detect_diagrams(image_path)
    annotations = detect_annotations(image_path)
    body_text = extract_body_text(image_path)

    output = {
        "tables": tables,
        "diagrams": diagrams,
        "annotations": annotations,
        "body_text": body_text
    }

    print(json.dumps(output))

if __name__ == "__main__":
    main()
```

### Conclusion

The detailed implementation of each step requires significant development, especially for accurately detecting regions and performing OCR. Libraries like OpenCV, Tesseract, and specialized algorithms for table and diagram detection play crucial roles. The output can be structured into JSON for easy parsing and integration into further processing or analysis pipelines.
