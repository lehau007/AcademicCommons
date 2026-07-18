flowchart TB
 subgraph ARTIFACTS["Per-file artifacts"]
        R["📄 result.md"]
        M["📄 metadata.json\n(route, sha256, duration)"]
        VP["📄 vision_prompts.json"]
        QF["📄 quality_flags.json\n(route_match, warnings)"]
  end
 subgraph LOOP["For each valid entry..."]
        ROUTE["decide_route(input_file)\n- .jpg/.png → vision_only\n- .pptx → hybrid\n- .pdf → classify_pdf_type()"]
        EXT{"Extract by format"}
        PDF_EXT["extract_pdf_text()\nPyMuPDF\n→ text blocks + vision prompts"]
        PPTX_EXT["extract_pptx_text()\npython-pptx\n→ slide text + image prompts"]
        IMG_EXT["extract_image_text()\n→ vision prompt only"]
        MERGE["merge_blocks_to_markdown()\n- text block → ## Segment N\n- vision block → blockquote"]
        ARTIFACTS
  end
 subgraph RUN_OUT["Run-level artifacts"]
        RS["📄 run_summary.json\n(success/partial/failed)"]
        CR["📄 coverage_report.json"]
        ER["📄 errors.json"]
  end
    CLI["🖥️ CLI: python document_processing_pipeline.py <mode>"] --> LOAD["load_dotenv()"]
    LOAD --> MODE{"Mode?"}
    MODE -- inventory --> INV_SCAN["discover_samples(data/sample/)"]
    INV_SCAN --> INV_META["parse_sample_metadata()\n(tier, course_code, format)"]
    INV_META --> INV_PDF{"Is PDF?"}
    INV_PDF -- Yes --> CLASSIFY["classify_pdf_type()\n- text_chars &lt; 80 → scanned_pdf\n- avg_chars ≥ 120 &amp; img_density ≤ 0.3 → text_pdf\n- image_count &gt; 0 → mixed_pdf"]
    INV_PDF -- PPTX --> INV_PPTX["inferred = pptx"]
    INV_PDF -- Image --> INV_IMG["inferred = image"]
    CLASSIFY --> INV_OUT["📄 inventory_report.json"]
    INV_PPTX --> INV_OUT
    INV_IMG --> INV_OUT
    MODE -- "gap-report" --> GAP["Load inventory_report.json\n(hoặc tự chạy inventory)"]
    GAP --> GAP_CHECK["So sánh inferred_edge_case_counts\nvới REQUIRED_EDGE_CASES\n[text_pdf, scanned_pdf, mixed_pdf, pptx, image]"]
    GAP_CHECK --> GAP_OUT["📄 gap_report.json"]
    MODE -- run --> MANIFEST["validate_manifest()\ndataset_manifest.json"]
    MANIFEST --> MVAL["📄 manifest_validation.json\n(valid_count, invalid_count)"]
    MVAL --> LOOP
    ROUTE --> EXT
    EXT -- PDF --> PDF_EXT
    EXT -- PPTX --> PPTX_EXT
    EXT -- Image --> IMG_EXT
    PDF_EXT --> MERGE
    PPTX_EXT --> MERGE
    IMG_EXT --> MERGE
    MERGE --> ARTIFACTS
    LOOP --> RUN_OUT

    style VP fill:#ffe0b2,stroke:#e65100
    style IMG_EXT fill:#ffe0b2,stroke:#e65100
    style MERGE fill:#ffe0b2,stroke:#e65100
    style LOAD fill:#ffcccc,stroke:#cc0000
    style GAP_OUT fill:#fff9c4,stroke:#f9a825