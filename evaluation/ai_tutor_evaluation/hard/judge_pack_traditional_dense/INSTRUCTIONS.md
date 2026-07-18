# Judge instructions — config `traditional_dense`

You are an impartial RAGAS-style grader. For EACH `<qid>.md` bundle in this folder:
1. Read `rubric.md` for the six metrics and their 1–5 anchors.
2. Score the tutor answer against the ground truth and the retrieved context.
3. Write `../results_traditional_dense/<qid>.json` matching `schema.json` exactly: a `qid`
   and a `scores` object with all six metrics, each `{"score": 1-5, "reason": "..."}`.

Rules: score only from the bundle; never invent facts; if the answer says the
materials do not cover the question AND the ground truth is absent from the retrieved
context, that is faithful (do not penalise faithfulness). Output valid JSON only.
