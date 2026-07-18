# OCR Result: database_scanned

Source: `src/experiments/document_processing/test_data/Database-giữa kì cô Oanh.pdf`

## Segment 1

To tackle this problem, we'll break it down into steps that involve detecting different regions on the scanned mixed-layout page and then extracting information from those regions. The process involves:

1. **Pre-processing**: Cleaning up the scanned image to improve OCR (Optical Character Recognition) accuracy.
2. **Detecting Regions**: Identifying table-like regions, graph/diagram regions, handwritten annotations, and body text areas.
3. **Extracting Information**: Applying OCR and other techniques to extract data from each region type.
4. **Merging Results**: Combining extracted data into a coherent output.

### Step 1: Pre-processing

- **Binarization**: Convert the image to black and white to enhance OCR performance.
- **Noise Removal**: Apply filters to remove scan artifacts.
- **Deskewing**: Straighten the image if it's skewed.

### Step 2: Detecting Regions

- **Table-like Regions**: Use algorithms that detect grid structures, such as finding intersecting lines or clustering of similar distances.
- **Graph/Diagram Regions**: Identify regions with significant graphical content, possibly leveraging edge detection and classification algorithms.
- **Handwritten Annotations**: Detect regions with significant handwritten content, using techniques like texture analysis or machine learning models trained on handwriting samples.
- **Body Text**: Regions not classified into the above categories are likely body text.

### Step 3: Extracting Information

- **Table-like Regions**: Apply table detection algorithms (like `camelot` or `tabula`) to extract structured JSON. 
  ```json
  {
    "tables": [
      {
        "rows": [
          ["Column1", "Column2"],
          ["Value1", "Value2"]
        ]
      }
    ]
  }
  ```

- **Graph/Diagram Regions**: Describe the graph/diagram in structured JSON, potentially including axes, labels, and noted trends.
  ```json
  {
    "diagrams": [
      {
        "type": "line_graph",
        "axes": ["X", "Y"],
        "description": "Shows trend over time"
      }
    ]
  }
  ```

- **Handwritten Annotations**: Store raw text or a digital representation (e.g., an image) of handwritten annotations.
  ```json
  {
    "annotations": [
      {
        "text": "Sample handwritten note",
        "location": "Top right corner"
      }
    ]
  }
  ```

- **Body Text**: Perform OCR using tools like `Tesseract-OCR` to extract plain text.

### Step 4: Merging Results

The final step involves merging the extracted data into a single, coherent output that approximates the reading order. This might require:

- **Layout Analysis**: Understanding the physical layout to infer reading order.
- **Heuristics**: Applying rules (e.g., left-to-right, top-to-bottom) to approximate reading order.

### Example Output

```json
{
  "text": "Main body text here...",
  "regions": [
    {
      "type": "table",
      "data": [
        ["Column1", "Column2"],
        ["Value1", "Value2"]
      ]
    },
    {
      "type": "diagram",
      "data": {
        "type": "line_graph",
        "axes": ["X", "Y"],
        "description": "Shows trend over time"
      }
    },
    {
      "type": "annotation",
      "text": "Sample handwritten note"
    }
  ]
}
```

### Implementation

- **Libraries/Tools**: Leverage libraries like OpenCV for image processing, `pytesseract` for OCR, and specialized libraries for table and diagram detection (`camelot`, `tabula`, etc.).
- **Custom Code**: Write custom scripts to integrate these tools, perform region detection, and merge results.

This process requires a combination of image processing, machine learning, and information extraction techniques. The exact implementation details can vary based on the specific requirements and the characteristics of the scanned pages.

## Segment 2

To tackle this problem, we'll break it down into steps that involve detecting different regions on the scanned mixed-layout page and then extracting information from those regions. The process involves:

1. **Pre-processing**: Cleaning up the scanned page to enhance image quality.
2. **Region Detection**: Identifying table-like regions, graph/diagram regions, handwritten annotations, and body text areas.
3. **Region-based OCR (Optical Character Recognition)**: Applying OCR to each type of region.
4. **Structured Data Extraction**: Converting detected regions into structured JSON.
5. **Merging Results**: Combining extracted data in an approximate reading order.

### Step 1: Pre-processing

- **Binarization**: Convert the image to black and white to reduce noise.
- **Noise Removal**: Apply filters to remove speckles and noise.
- **Deskewing**: Straighten the image if it's skewed.

### Step 2: Region Detection

- **Table-like Regions**: Use algorithms that detect grid-like structures, such as the table detection algorithm.
- **Graph/Diagram Regions**: Detect regions with significant graphical content, possibly using edge detection and shape analysis.
- **Handwritten Annotations**: Identify regions with less structured, handwritten text, potentially using texture analysis.
- **Body Text**: Detect large blocks of text not contained within tables or diagrams.

### Step 3: Region-based OCR

- **Apply OCR**: Use an OCR engine (like Tesseract) on detected text regions. For tables, consider table-specific OCR that preserves cell structure.
- **Layout Analysis**: For body text, analyze and preserve paragraph and sentence structures.

### Step 4: Structured Data Extraction

- **Tables to JSON**: Convert table data into JSON format, preserving row and column structures.
  ```json
  {
    "tables": [
      {
        "rows": [
          {"cells": ["Cell1", "Cell2"]},
          {"cells": ["Cell3", "Cell4"]}
        ]
      }
    ]
  }
  ```

- **Graphs/Diagrams to JSON**: Describe graphs/diagrams in JSON, potentially including axes, labels, and data points.
  ```json
  {
    "graphs": [
      {
        "type": "line",
        "dataPoints": [[1, 2], [3, 4]],
        "labels": ["X", "Y"]
      }
    ]
  }
  ```

- **Handwritten Annotations**: Store as-is or transcribed into text format.
  ```json
  {
    "annotations": [
      {
        "text": "Some handwritten note"
      }
    ]
  }
  ```

- **Body Text**: Store in a structured format preserving paragraphs and possibly sentence structures.
  ```json
  {
    "bodyText": [
      {
        "paragraphs": ["This is a paragraph.", "This is another."]
      }
    ]
  }
  ```

### Step 5: Merging Results

- **Order Detection**: Use heuristics (e.g., spatial proximity, reading order algorithms) to approximate the reading order.
- **Combine JSON**: Merge all extracted data into a single JSON structure.

```json
{
  "content": [
    {"tables": [...]},
    {"graphs": [...]},
    {"annotations": [...]},
    {"bodyText": [...]},
  ]
}
```

### Implementation

This process can be implemented using Python libraries such as:

- **OpenCV** for image pre-processing and region detection.
- **Pytesseract** or **Tesseract-OCR** for OCR.
- **Tabula** or **camelot** for table detection and extraction.
- **scikit-image** for additional image processing.

### Example Python Snippet

```python
import cv2
import pytesseract
from PIL import Image

# Load image
img = cv2.imread('image.png')

# Pre-processing
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect and extract regions
# ...

# Apply OCR
text = pytesseract.image_to_string(Image.fromarray(gray))

# Structured data extraction and merging
# ...

```

### Conclusion

The detailed process outlined above provides a comprehensive approach to performing region-based OCR on a scanned mixed-layout page. The exact implementation details may vary based on the specific requirements and the characteristics of the input documents.
