from io import BytesIO
from typing import Dict, Any
from openpyxl import Workbook
from app.services.export.core.render_context import RenderContext

class BaseExcelRenderer:
    """Base class for Excel Renderers."""
    
    def render(self, dataset: Dict[str, Any], context: RenderContext) -> BytesIO:
        wb = Workbook()
        ws = wb.active
        
        metadata = dataset.get("metadata", {})
        title = metadata.get("report_type", "Export")
        ws.title = title[:31] # Excel sheet titles max 31 chars
        
        self.build_document(wb, ws, dataset, context)
        
        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)
        return stream
        
    def build_document(self, wb: Workbook, ws, dataset: Dict[str, Any], context: RenderContext):
        raise NotImplementedError("Subclasses must implement build_document")
