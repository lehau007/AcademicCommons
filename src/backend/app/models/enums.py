from enum import StrEnum


class DocumentStatus(StrEnum):
    UPLOADED = "UPLOADED"
    PARSING = "PARSING"
    EVALUATING = "EVALUATING"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    APPROVED = "APPROVED"
    INDEXING = "INDEXING"
    INDEXED = "INDEXED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class DocumentTier(StrEnum):
    OFFICIAL = "official"
    COMMUNITY = "community"


class MaterialType(StrEnum):
    SYLLABUS = "syllabus"
    TEXTBOOK = "textbook"
    LECTURE_SLIDES = "lecture_slides"


class ContributionType(StrEnum):
    PAST_EXAM = "past_exam"
    SUMMARY_NOTE = "summary_note"
    REVIEW_NOTE = "review_note"
    SOLVED_EXERCISE = "solved_exercise"


class FileFormat(StrEnum):
    PDF = "pdf"
    PPTX = "pptx"
    JPG = "jpg"
    PNG = "png"


class Language(StrEnum):
    VI = "vi"
    EN = "en"
    MIXED = "mixed"


class OcrQuality(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RagNamespace(StrEnum):
    KNOWLEDGE = "knowledge"
    EXERCISE = "exercise"


class JobStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ProcessingJobType(StrEnum):
    OCR = "ocr"
    INDEX = "index"


class QuestionType(StrEnum):
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    TRUE_FALSE = "true_false"


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ChatRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

