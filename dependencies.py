from services.reports import ReportsService
from config import settings

def getReportsServiceDep() -> ReportsService:
    return ReportsService(
        template=settings.TEMPLATE, 
        templates_dir=settings.TEMPLATES_DIR, 
        output_dir=settings.OUTPUT_DIR
    )