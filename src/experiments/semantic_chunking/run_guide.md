# Semantic Chunking + ChromaDB Experiment

This experiment consumes a `normalized_result.md` produced by the document processing experiment, performs structure-aware semantic chunking, embeds each chunk with a small Sentence Transformer model, and persists the result into a local `chroma_db`.

## 1. Generate a local example pipeline output under `src/`

```bash
DOCUMENT_PROCESSING_OUTPUT_BASE=src/experiments/semantic_chunking/example_pipeline_output \
.venv/bin/python src/experiments/document_processing/document_processing_pipeline.py \
  run \
  --manifest src/experiments/document_processing/test_manifest.json \
  --run-id semantic_chunking_example
```

Example normalized markdown input created by that command:

```text
src/experiments/semantic_chunking/example_pipeline_output/semantic_chunking_example/graph_presentation/normalized_result.md
```

## 2. Install experiment dependencies

```bash
.venv/bin/pip install -r requirements.txt
```

## 3. Run semantic chunking and store into ChromaDB

```bash
.venv/bin/python src/experiments/semantic_chunking/semantic_chunking_chroma_experiment.py \
  --input src/experiments/semantic_chunking/example_pipeline_output/semantic_chunking_example/graph_presentation/normalized_result.md \
  --sample-id graph_presentation \
  --course-code TEST01 \
  --tier community \
  --subtype summary_note \
  --summary-output src/experiments/semantic_chunking/generated/graph_presentation_summary.json
```

Default persistence directory:

```text
src/experiments/semantic_chunking/chroma_db
```

## Notes

- Default embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Default Chroma collection: `document_chunks`
- Namespace routing follows `.agent/architecture/adr-002-rag-namespaces.md`
- Re-running for the same `sample_id` deletes old chunks for that document before inserting the new ones
