from fastapi.responses import FileResponse
from dependencies import getReportsServiceDep
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from schemas.report import ReportData, ReportDataIn
from services.reports import ReportsService

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/generate", summary="Generate PDF report", status_code=status.HTTP_201_CREATED)
async def generate_report(
    report_data_input: Annotated[ReportDataIn, Body(..., title="Report data for PDF generation")],
    reports_service: Annotated[ReportsService, Depends(getReportsServiceDep)]
):
    report_data = ReportData.model_validate(report_data_input.model_dump())
    reports_service.generate_pdf_report(report_data.model_dump())
    return {
        "status": status.HTTP_201_CREATED,
        "message": f"PDF report with ID:{report_data.id} was successfully generated"
    }


@router.get("/{report_id}", response_class=FileResponse, summary="Get PDF report by ID", status_code=status.HTTP_200_OK)
async def get_report(
    report_id: Annotated[int, Path(..., title="Report ID")],
    reports_service: Annotated[ReportsService, Depends(getReportsServiceDep)]
):
    report_path = reports_service.get_report_path(report_id=report_id)
    if not report_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PDF report with ID:{report_id} not found")
    filename = f"report_{report_id}"
    return FileResponse(
        path=report_path,
        filename=filename,
        media_type="application/pdf"
    )