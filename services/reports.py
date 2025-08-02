from pathlib import Path
from fastapi import HTTPException
from logger import log
from jinja2 import Template, TemplateError
from weasyprint import HTML
from logger import reports_log

class ReportsService:
    def __init__(
        self, 
        template: str,
        templates_dir: str,
        output_dir: str
    ):
        self.templates_dir = Path(__file__).parent.parent / templates_dir
        self.template_path = self.templates_dir / template
        self.output_path = Path(__file__).parent.parent / output_dir
        try:
            self.template = Template(self.template_path.read_text(encoding="utf-8"))
        except TemplateError as err:
            log.error(f"Invalid template: {err}")
            raise HTTPException(status_code=400, detail="Invalid template")

    def _render_template(self, data: dict) -> str:
        try:
            return self.template.render(**data)
        except TemplateError as err:
            log.error(f"Template rendering error: {err}")
            raise HTTPException(status_code=400, detail="Invalid template data")

    def _save_pdf_file(self, html: str, filename: str) -> Path:
        target = self.output_path / f"{filename}.pdf"
        try:
            HTML(string=html).write_pdf(target)
            return target
        except Exception as err:
            log.exception(f"PDF file saving failed: {err}")

    def generate_pdf_report(self, report_data: dict ) -> bytes:
        try:
            html_content = self._render_template(report_data)
            generated_pdf = HTML(string=html_content).write_pdf()
            filename = str(report_data["id"])
            file_path = self._save_pdf_file(html=html_content, filename=filename)
            reports_log.info("", extra={"report_id": report_data["id"], "report_filename": filename, "file_path": file_path})
            return generated_pdf
        except Exception as err:
            log.exception(f"Exception: {err}")
            raise HTTPException(status_code=500, detail="Internal server error")
            
    def get_report_path(self, report_id: int) -> Path:
        try:
            reports_list = Path(self.output_path).iterdir()
            for report_path in reports_list:
                if report_path.suffix.lower() == ".pdf" and int(report_path.stem) == report_id:
                    return report_path
            return None
        except Exception as err:
            log.exception(f"Exception: {err}")
            raise HTTPException(status_code=500, detail="Internal server error")