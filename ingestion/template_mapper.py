# ingestion/template_mapper.py

from typing import Dict


def map_text_to_sections(
    extracted_pages: Dict[int, str]
) -> Dict[str, str]:
    """
    Maps extracted PDF text into fixed template sections
    using page positions (no semantic assumptions).

    Template mapping:
    Page 2 -> idea_problem
    Page 3 -> team_capability
    Page 4 -> tech_stack
    """

    sections = {
        "idea_problem": "",
        "solution_approach": "",
        "uniqueness_claim": "",
        "tech_stack": "",
        "team_capability": "",
    }

    for page_num, text in extracted_pages.items():
        if not text.strip():
            continue

        if page_num == 2:
            sections["idea_problem"] += text + "\n"
            sections["solution_approach"] += text + "\n"
            sections["uniqueness_claim"] += text + "\n"

        elif page_num == 3:
            sections["team_capability"] += text + "\n"

        elif page_num == 4:
            sections["tech_stack"] += text + "\n"

        # Page 1 & 5 ignored intentionally

    # Final cleanup
    for key in sections:
        sections[key] = sections[key].strip()

    return sections
