# Document Text Normalization

To normalize extracted document text into clean, coherent Markdown, follow these steps:

## Step 1: Preprocessing

- **Cleaning**: Remove noise from the scanned image to improve OCR accuracy.
- **Binarization**: Convert the image to black and white to simplify further processing.

## Step 2: Detecting Table-like Regions

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

## Step 3: Detecting Graph/Diagram Regions

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

## Step 4: Detecting Handwritten Annotations

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

## Step 5: Extracting Body Text

- **Approach**: Apply standard OCR techniques to regions not classified into other categories.

- **Output**:

```json
{
  "type": "text",
  "content": "This is the body text of the document..."
}
```

## Step 6: Merging Content

- **Approach**: Use layout analysis to approximate the reading order. This might involve:
  - **Top-to-bottom and left-to-right analysis**: Generally, humans read documents in this manner.

## Example Combined Output

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

## Implementation

Implementing these steps would typically involve using libraries and frameworks like:

- **OpenCV** for image processing.
- **Pytesseract** or **Tesseract-OCR** for OCR.
- **scikit-image** for advanced image analysis.
- **scikit-learn** or **TensorFlow** for machine learning tasks.

Each library provides functionalities that can be combined to achieve the outlined approach. However, a detailed implementation requires programming expertise and access to the specific libraries and tools mentioned.