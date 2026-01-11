RAG-based Idea Evaluation System for Hackathons

Overview

This project is an AI-assisted evaluation system designed to screen and shortlist hackathon idea submissions submitted as PDFs.

The system ingests idea proposal PDFs, extracts structured content, evaluates them using a Retrieval-Augmented Generation (RAG) pipeline, applies rubric-based scoring, checks internal uniqueness, and outputs explainable scores in structured JSON (and optionally Excel for batch mode).

The primary goal is to assist organizers in fair, consistent, and scalable shortlisting, not to replace human judgment.

Key Objectives

Handle hundreds to thousands of idea submissions

Enforce template-aware evaluation

Penalize vague, generic, or near-duplicate ideas

Prioritize clarity, feasibility, and originality

Ensure explainability and auditability

Avoid unreliable AI-plagiarism claims

High-Level Flow PDF Upload ↓ Text Extraction (PDF) ↓ Template-aware Chunking (5 logical sections) ↓ Embeddings Generation ↓ Vector Storage (ChromaDB) ↓ RAG-based Rubric Evaluation (LLM) ↓ Internal Similarity / Uniqueness Check ↓ Score Aggregation ↓ JSON / Excel Output

Input

Format: PDF (Hackathon Idea Proposal)

Assumption: Submissions broadly follow the provided idea template

Metadata provided externally:

team_name

week

hackathon_id

Output

Structured evaluation per submission

Scores with reasons for:

Problem clarity

Solution quality

Technical feasibility

Team capability

Uniqueness

Final score out of 100

Status flags for:

Invalid / template-only submissions

Incomplete submissions

Chunking Strategy (Important)

This project uses semantic, template-aware chunking, not arbitrary token windows.

Each PDF is mapped into 5 logical chunks:

idea_problem Problem definition, motivation, and context

solution_approach Proposed solution, workflow, and approach

uniqueness_claim Differentiation and novelty claims

tech_stack Tools, technologies, platforms

team_capability Team skills, experience, execution readiness

Why this strategy?

Aligns directly with judging rubrics

Prevents semantic mixing

Enables targeted retrieval per criterion

Improves explainability

Chunking is structure-driven, not keyword-forced.

Embeddings

Model: sentence-transformers/all-MiniLM-L6-v2

Embedding size: 384 dimensions

Granularity: One embedding per chunk

Metadata stored:

ppt_id

team_name

section

week

timestamp

Vector Database

Engine: ChromaDB

Purpose:

Context retrieval for RAG

Internal similarity checks

Isolation strategy:

Current PPT is excluded during similarity search

Section-aware filtering is applied where needed

RAG Usage (Clarified)

RAG is used only for evaluation, not generation.

For each evaluation criterion:

A rubric-specific query is embedded

Relevant chunks are retrieved from ChromaDB

Retrieved context is injected into a frozen prompt

The LLM returns strict JSON

This ensures:

No hallucinated context

Conservative scoring

Explainable outputs

Evaluation Rubric Criterion Max Score Problem Clarity 20 Solution Quality 15 Technical Feasibility 15 Team Capability 10 Uniqueness 40 Total 100

Each score is returned with a natural-language justification.

Uniqueness Handling (Critical Design)

Uniqueness is not based on web scraping or AI plagiarism detection.

Instead, the system uses:

Internal Semantic Similarity
Compares idea_problem embeddings against previous submissions

Uses cosine similarity

High similarity → penalty

LLM-Based Novelty Judgment
Evaluates differentiation from similar ideas

Conservative scoring (no auto-rejection)

Final Uniqueness Score final_uniqueness = base_llm_score ± similarity_adjustment

This avoids false accusations and keeps evaluation fair.

Template & Empty Submission Handling

The system detects and flags:

Template-only PDFs

Instructional text without real idea content

Missing or empty sections

Such submissions are marked as:

status = "invalid_submission"

They are excluded from scoring and ranking.

LLM Details

Model: LLaMA 3

Parameters: 8 Billion (8B)

Runtime: Local via Ollama

Why local:

No paid APIs

Data privacy

Offline demos

LLM outputs are strictly parsed JSON with retries and validation.

Folder Structure Hack-Nocturne_ai_evaluator/ │ ├── ingestion/ # PDF parsing and text extraction ├── chunking/ # Section-aware chunk building & validation ├── embeddings/ # Embedding generation ├── vector_store/ # ChromaDB setup & retrieval ├── evaluation/ # Prompts, rubric scoring, retrieval rules ├── uniqueness/ # Internal similarity & adjustments ├── llm/ # Ollama LLaMA 3 client ├── pipeline/ # Orchestration logic ├── output/ # Excel writer & ranking logic ├── api/ # (Optional) API wrapper ├── data/ # Runtime PDFs (gitignored) ├── main.py # Entry point (batch mode) ├── requirements.txt └── README.md

What This System Is (and Is Not) ✔ What it IS

A fair, explainable first-pass evaluator

A scalable shortlisting assistant

A consistency and bias-reduction tool

✖ What it is NOT

A plagiarism detector

A final judge

An AI-generated-text classifier

A winner-deciding system

Design Philosophy

Conservative over aggressive

Explainable over clever

Penalize vagueness, not AI usage

Assist humans, don’t replace them

Typical Use Case

Weekly evaluation of submissions

Generate ranked shortlists

Reduce judge workload

Provide structured feedback

Known Limitations

Depends on reasonable template adherence

Does not evaluate visual diagrams or images

Does not crawl the web for novelty

Final judgment should involve human review

Status

✔ End-to-end functional ✔ Batch processing tested ✔ Robust error handling ✔ Demo-ready

Created with love by Suparn Nayak ❤️
