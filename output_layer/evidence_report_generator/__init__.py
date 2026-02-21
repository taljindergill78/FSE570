"""Evidence report generator: Markdown and HTML reports with citations."""

from output_layer.evidence_report_generator.report import (
    generate_html_report,
    generate_markdown_report,
    write_markdown_report,
)

__all__ = ["generate_markdown_report", "generate_html_report", "write_markdown_report"]
