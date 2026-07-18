# OCR Result: database_scanned

Source: `src/experiments/document_processing/test_data/Database-giữa kì cô Oanh.pdf`

## Segment 1

To tackle this problem, we'll break it down into steps that involve detecting different regions on the scanned mixed-layout page and then performing OCR (Optical Character Recognition) on those regions accordingly. This process involves a combination of image processing and machine learning techniques. While a detailed implementation would require programming, I'll outline a conceptual approach to solving this problem.

### Step 1: Preprocessing

- **Cleaning**: Remove any noise from the scanned image to improve OCR accuracy.
- **Binarization**: Convert the image to black and white to simplify further processing.

### Step 2: Detecting Table-like Regions

- **Approach**: Use algorithms that detect grid-like structures, such as:
  - **Projection profiles**: Analyze horizontal and vertical projection profiles to identify dense areas that could indicate table borders.
  - **Structural analysis**: Look for intersecting lines that form a grid.

- **Extraction**: Once table regions are identified, apply OCR to those areas specifically. Use the detected grid structure to infer table cell boundaries.

- **JSON Output**:
  ```json
  {
    "type": "table",
    "data": [
      ["Cell 1", "Cell 2"],
      ["Cell 3", "Cell 4"]
    ]
  }
  ```

### Step 3: Detecting Graph/Diagram Regions

- **Approach**: Identify regions that do not contain text or have characteristics of graphs (e.g., axes, legends).
  - **Edge detection**: Apply algorithms like Canny edge detection to highlight diagram edges.
  - **Image analysis**: Use features like lines, curves, and filled areas to distinguish diagrams.

- **Extraction**: These regions might not require OCR but could be stored as images or described in JSON.

- **JSON Output**:
  ```json
  {
    "type": "diagram",
    "description": "Line graph showing...",
    "image": "diagram_image.png"
  }
  ```

### Step 4: Detecting Handwritten Annotations

- **Approach**: Use machine learning models trained to distinguish handwritten text from typed text or other image elements.
  - **Texture analysis**: Handwritten areas often have different textures compared to printed text.

- **Extraction**: Apply handwritten text recognition techniques (if different from standard OCR).

- **Output**:
  ```json
  {
    "type": "handwritten",
    "text": "Some handwritten annotation"
  }
  ```

### Step 5: Extracting Body Text

- **Approach**: Apply standard OCR techniques to regions not classified into other categories.

- **Output**:
  ```json
  {
    "type": "text",
    "content": "This is the body text of the document..."
  }
  ```

### Step 6: Merging Content

- **Approach**: Use layout analysis to approximate the reading order. This might involve:
  - **Top-to-bottom and left-to-right analysis**: Generally, humans read documents in this manner.

### Example Combined Output

```json
[
  {
    "type": "text",
    "content": "Introduction to the document..."
  },
  {
    "type": "table",
    "data": [
      ["Cell 1", "Cell 2"],
      ["Cell 3", "Cell 4"]
    ]
  },
  {
    "type": "diagram",
    "description": "Line graph showing...",
    "image": "diagram_image.png"
  },
  {
    "type": "handwritten",
    "text": "Some handwritten annotation"
  },
  {
    "type": "text",
    "content": "Conclusion of the document..."
  }
]
```

### Implementation

Implementing these steps would typically involve using libraries and frameworks like:

- **OpenCV** for image processing.
- **Pytesseract** or **Tesseract-OCR** for OCR.
- **scikit-image** for advanced image analysis.
- **scikit-learn** or **TensorFlow** for machine learning tasks.

Each library provides functionalities that can be combined to achieve the outlined approach. However, a detailed implementation requires programming expertise and access to the specific libraries and tools mentioned.

## Segment 2

To tackle this problem, we'll break it down into steps that involve detecting different regions on the scanned mixed-layout page and then performing OCR (Optical Character Recognition) on those regions accordingly. The goal is to extract table-like regions, graph/diagram regions, handwritten annotations, and body text, and then merge them back in an approximate reading order.

### Step 1: Preprocessing

- **Cleaning:** Remove any noise from the scanned page to improve OCR accuracy.
- **Deskewing:** If the page is skewed, straighten it to ensure accurate region detection.

### Step 2: Detecting Table-like Regions

- **Approach:** Use algorithms like `camelot` or `tabula` which are specifically designed for table detection and extraction from PDFs and images.
- **Output:** Convert detected tables into structured JSON. For example:

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

### Step 3: Detecting Graph/Diagram Regions

- **Approach:** This can be challenging as there's no straightforward library like for tables. A combination of edge detection algorithms (e.g., Canny, Sobel) and contour detection might be used to identify these regions. Machine learning models can also be trained to classify regions as graphs/diagrams.
- **Output:** For simplicity, these could be represented as:

```json
{
  "graphs": [
    {
      "image": "path/to/graph/image.png",
      "description": "Detected graph/diagram with potential axes and labels"
    }
  ]
}
```

### Step 4: Detecting Handwritten Annotations

- **Approach:** Handwritten annotations can be detected using a combination of thresholding techniques to segment out handwritten parts from the rest of the document. Libraries like OpenCV can be helpful. Machine learning models, especially those trained on handwritten datasets, can improve accuracy.
- **Output:** Store the locations and potentially the recognized text (if an ICR - Intelligent Character Recognition - engine is used) of handwritten annotations:

```json
{
  "annotations": [
    {
      "text": "Sample handwritten text",
      "x": 100,
      "y": 100
    }
  ]
}
```

### Step 5: Extracting Body Text

- **Approach:** Use general-purpose OCR engines like `Tesseract-OCR` for text extraction. Pre-processing steps like binarization, and post-processing steps like spell-checking can enhance accuracy.
- **Output:** Extracted text.

### Step 6: Merging Content

- **Approach:** Use the detected regions and their positions on the page to approximate the reading order. This might involve sorting based on the y-coordinate and then the x-coordinate for elements on the same line.

### Example Combined Output

```json
{
  "tables": [
    // table data
  ],
  "graphs": [
    // graph data
  ],
  "annotations": [
    // annotation data
  ],
  "text": [
    // Extracted body text lines with their positions
    {
      "line": "This is a line of text",
      "x": 100,
      "y": 200
    }
  ]
}
```

### Implementation

The implementation would involve:

1. **Python** as the primary programming language.
2. **Libraries:** 
   - `OpenCV` for image processing.
   - `Pytesseract` or `pdf2image` + `Tesseract-OCR` for OCR.
   - `camelot` or `tabula-py` for table detection.
   - `scikit-image` for additional image processing.

### Challenges

- **Mixed Layout:** Handling mixed layouts accurately can be challenging.
- **Image Quality:** Low-quality scans can significantly affect OCR accuracy.
- **Complex Graphs:** Detailed extraction of information from complex graphs/diagrams might require manual intervention.

### Future Improvements

- **Training Machine Learning Models:** For specific tasks like handwritten text recognition or graph/diagram classification, training ML models can improve accuracy.
- **Improving Post-processing:** Enhancing the merging step to better approximate reading order and handle multi-column texts.
