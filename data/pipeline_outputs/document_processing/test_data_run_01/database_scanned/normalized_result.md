# Document Analysis and Information Extraction

## Introduction

To tackle the problem of extracting information from scanned mixed-layout pages, we'll break it down into steps that involve detecting different regions on the page and then extracting information from those regions.

## Steps Involved

The process involves:

1. **Preprocessing**: Cleaning up the scanned page to enhance image quality.
2. **Region Detection**:
   - **Table-like Regions**: Detecting areas that resemble tables.
   - **Graph/Diagram Regions**: Identifying areas with graphical content.
   - **Handwritten Annotations**: Finding regions with handwritten text.
   - **Body Text Regions**: Detecting areas with the main body text.
3. **Region-based OCR (Optical Character Recognition)**: Applying OCR to each type of region.
4. **Information Extraction and Structuring**:
   - **Tables**: As structured JSON.
   - **Graphs/Diagrams**: Description in structured JSON.
   - **Handwritten Annotations**: As text or images.
   - **Body Text**: Extracted text.
5. **Merging and Ordering**: Combining extracted information in an approximate reading order.

## Step 1: Preprocessing

Preprocessing involves:

- **Image Cleaning**: Apply filters to remove noise, and binarization to enhance text visibility.

## Step 2: Region Detection

### Table-like Regions

- **Approach**: Use OpenCV to apply thresholding and edge detection. Tables often have a grid-like structure, which can be detected using techniques like the Hough Transform or by finding lines.
- **Extraction**: Once table regions are identified, use Tesseract-OCR with the `--psm 6` mode (Assume a single uniform block of text) to extract text. Structure the data into JSON by analyzing the layout and spacing.

### Graph/Diagram Regions

- **Approach**: Apply edge detection and contour finding. Graphs and diagrams often have distinctive shapes and lines.
- **Extraction**: Use libraries capable of analyzing graph structures (e.g., OpenCV, and then export to Graphviz for structured data extraction). The output could be a description of the graph.

### Handwritten Annotations

- **Approach**: Use a combination of edge detection and machine learning models (like SVM or neural networks) trained on examples of handwritten text vs. printed text.
- **Extraction**: Store the locations and transcriptions (if possible) of handwritten annotations. Tesseract-OCR with `--psm 11` (Sparse text. Find as much text as possible in no particular order) might help.

### Body Text Regions

- **Approach**: Use Tesseract-OCR with `--psm 3` (Assume a single column of text of variable sizes) or `--psm 6` on the entire document to extract body text.

## Step 3: Region-based OCR

- **For Table-like Regions**: Apply table-specific OCR tools like [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) with table layout analysis.
- **For Graph/Diagram Regions**: Use vectorization or object detection to describe graphical elements.
- **For Handwritten Annotations**: Apply handwritten text recognition tools like [Tesseract-OCR with LSTM models](https://github.com/tesseract-ocr/tesseract).
- **For Body Text Regions**: Use standard OCR tools.

## Step 4: Information Extraction and Structuring

### Tables

Convert to JSON with row and column structures.

| Column1 | Column2 |
|---------|---------|
| Cell1   | Cell2   |
| Cell3   | Cell4   |

```json
{
  "tables": [
    {
      "rows": [
        {"cells": ["Column1", "Column2"]},
        {"cells": ["Cell1", "Cell2"]},
        {"cells": ["Cell3", "Cell4"]}
      ]
    }
  ]
}
```

### Graphs/Diagrams

Describe in JSON.

```json
{
  "graphs": [
    {
      "type": "line_graph",
      "description": "A line graph showing..."
    }
  ]
}
```

### Handwritten Annotations

Store as text or images.

```json
{
  "annotations": [
    {
      "text": "Some handwritten annotation",
      "x": 100,
      "y": 100
    }
  ]
}
```

### Body Text

Store as extracted text.

## Step 5: Merging and Ordering

Combine all extracted information and order it based on the spatial locations and logical reading order.

```json
{
  "content": [
    {
      "type": "body_text",
      "text": "This is some body text."
    },
    {
      "type": "table",
      "rows": [...]
    },
    {
      "type": "graph",
      "description": "..."
    },
    {
      "type": "annotation",
      "text": "Some annotation."
    }
  ]
}
```

## Implementation

The implementation involves using libraries like OpenCV for image processing, Pytesseract for OCR, and custom algorithms for region detection. A high-level example:

```python
import cv2
import pytesseract
import numpy as np

def preprocess_image(image_path):
    # Load and preprocess image
    img = cv2.imread(image_path)
    # Binarize, remove noise, deskew, etc.
    return img

def detect_tables(img):
    # Detect and extract tables
    tables = []
    # Logic here
    return tables

def detect_graphs(img):
    # Detect and extract graphs
    graphs = []
    # Logic here
    return graphs

def detect_handwritten_annotations(img):
    # Detect handwritten annotations
    annotations = []
    # Logic here
    return annotations

def extract_body_text(img):
    # Extract body text
    text = pytesseract.image_to_string(img, config='--psm 6')
    return text

def main(image_path):
    img = preprocess_image(image_path)
    tables = detect_tables(img)
    graphs = detect_graphs(img)
    annotations = detect_handwritten_annotations(img)
    body_text = extract_body_text(img)

    output = {
        "tables": tables,
        "graphs": graphs,
        "annotations": annotations,
        "body_text": body_text
    }

    print(json.dumps(output))

if __name__ == "__main__":
    main("path_to_your_image.jpg")
```

This process requires detailed implementation for each step, potentially involving deep learning models for accurate region detection and OCR. Libraries and tools like [LayoutParser](https://layoutparser.github.io/) for layout analysis can significantly simplify the process.