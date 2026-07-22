from typing import Dict, Any, List
from app.services.export.pdf.base_renderer import BasePDFRenderer, ProfessionalPDF
from app.services.export.core.render_context import RenderContext
from app.core.storage.resolver import StorageResolver
import os

class BlockPDFRenderer(BasePDFRenderer):
    """Renderer that outputs data in a block layout with image evidence."""
    
    def build_document(self, pdf: ProfessionalPDF, dataset: Dict[str, Any], context: RenderContext):
        self._render_metadata_and_summary(pdf, dataset)
        
        activities = dataset.get("activities", [])
        if not activities:
            pdf.ln(10)
            pdf.set_font("helvetica", "I", 12)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(0, 10, "No activity found", align="C", ln=True)
            return
            
        for i, activity in enumerate(activities):
            self._render_activity_block(pdf, activity, i + 1)
            
    def _render_metadata_and_summary(self, pdf: ProfessionalPDF, dataset: Dict[str, Any]):
        summary = dataset.get("summary", {})
        metadata = dataset.get("metadata", {})
        
        pdf.set_y(pdf.get_y() + 5)
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 6, "Report Summary", ln=True)
        
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(71, 85, 105)
        
        # We will render summary metrics in columns
        metrics = [
            ("Total Activity", summary.get("total_activity", 0)),
            ("Completed", summary.get("completed", 0)),
            ("Working", summary.get("working", 0)),
            ("Duration", summary.get("total_duration_human", "0 Mins")),
            ("Assets", summary.get("total_assets", 0)),
            ("Evidences", summary.get("total_evidence", 0)),
        ]
        
        old_y = pdf.get_y()
        col_width = pdf.w / 3 - 10
        
        for i, (label, val) in enumerate(metrics):
            if i % 3 == 0 and i != 0:
                pdf.ln(6)
            col_x = pdf.l_margin + (i % 3) * col_width
            pdf.set_xy(col_x, pdf.get_y())
            pdf.set_font("helvetica", "B", 9)
            pdf.cell(30, 6, f"{label}:")
            pdf.set_font("helvetica", "", 9)
            pdf.cell(20, 6, str(val))
            
        pdf.ln(10)
        pdf.set_draw_color(226, 232, 240)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(5)

    def _render_activity_block(self, pdf: ProfessionalPDF, activity: Dict[str, Any], index: int):
        # Ensure we have enough space for the block header
        if pdf.get_y() > pdf.h - 50:
            pdf.add_page()
            
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(30, 41, 59)
        
        # Header
        pdf.set_fill_color(248, 250, 252) # slate-50
        pdf.rect(pdf.l_margin, pdf.get_y(), pdf.w - pdf.l_margin - pdf.r_margin, 8, "F")
        pdf.cell(0, 8, f"Activity #{index}: {activity.get('activity', 'Unnamed Activity')}", ln=True, align="L")
        
        pdf.ln(3)
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(71, 85, 105)
        
        details = [
            ("Employee", activity.get("employee", "-")),
            ("Division", activity.get("division", "-")),
            ("Category", activity.get("category", "-")),
            ("Status", activity.get("status", "-")),
            ("Duration", activity.get("duration_human", "-")),
            ("Date", activity.get("date", "-"))
        ]
        
        # Details 2-column layout
        start_y = pdf.get_y()
        col1_w = 25
        val1_w = 60
        
        for i, (label, val) in enumerate(details):
            if i % 2 == 0:
                pdf.set_xy(pdf.l_margin, start_y + (i // 2) * 6)
            else:
                pdf.set_xy(pdf.l_margin + 90, start_y + (i // 2) * 6)
                
            pdf.set_font("helvetica", "B", 9)
            pdf.cell(col1_w, 6, f"{label}:")
            pdf.set_font("helvetica", "", 9)
            pdf.cell(val1_w, 6, str(val))
            
        pdf.ln(8)
        
        # Notes
        notes = activity.get("notes", "")
        if notes:
            pdf.set_font("helvetica", "B", 9)
            pdf.cell(0, 6, "Notes:", ln=True)
            pdf.set_font("helvetica", "", 9)
            pdf.multi_cell(0, 5, str(notes))
            pdf.ln(3)
            
        # Assets
        assets = activity.get("assets", [])
        if assets:
            pdf.set_font("helvetica", "B", 9)
            pdf.cell(0, 6, "Assets Used:", ln=True)
            pdf.set_font("helvetica", "", 9)
            assets_str = ", ".join([f"{a.get('item', '')} ({a.get('qty', 1)})" for a in assets])
            pdf.multi_cell(0, 5, assets_str)
            pdf.ln(3)
            
        # Evidences
        self._render_evidences(pdf, activity.get("evidences", {}))
        
        # Separator for next activity
        pdf.ln(5)
        pdf.set_draw_color(226, 232, 240)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(5)

    def _render_evidences(self, pdf: ProfessionalPDF, evidences: Dict[str, Any]):
        if not evidences:
            return
            
        before = evidences.get("before")
        progress = evidences.get("progress", [])
        after = evidences.get("after")
        
        has_any = bool(before or progress or after)
        if not has_any:
            return
            
        pdf.set_font("helvetica", "B", 9)
        pdf.cell(0, 6, "Evidences:", ln=True)
        pdf.ln(2)
        
        # Draw before & after side by side if both exist
        if before and after:
            self._render_image_row(pdf, [("BEFORE", before), ("AFTER", after)])
        else:
            if before:
                self._render_image_row(pdf, [("BEFORE", before)])
            if after:
                self._render_image_row(pdf, [("AFTER", after)])
                
        # Draw progress in grid (max 2 per row)
        if progress:
            row = []
            for i, p in enumerate(progress):
                row.append((f"PROGRESS #{i+1}", p))
                if len(row) == 2:
                    self._render_image_row(pdf, row)
                    row = []
            if row:
                self._render_image_row(pdf, row)

    def _render_image_row(self, pdf: ProfessionalPDF, items: List[tuple]):
        """Render up to 2 images in a row."""
        # Ensure space
        if pdf.get_y() > pdf.h - 70:
            pdf.add_page()
            
        start_y = pdf.get_y()
        max_img_h = 60
        img_w = 80
        
        for i, (label, ev) in enumerate(items):
            x = pdf.l_margin + (i * (img_w + 10))
            
            pdf.set_xy(x, start_y)
            pdf.set_font("helvetica", "B", 8)
            pdf.cell(img_w, 5, label, align="C", ln=True)
            
            storage_path = ev.get("storage_path")
            abs_path = StorageResolver.resolve(storage_path)
            
            pdf.set_xy(x, start_y + 6)
            
            if abs_path and os.path.exists(abs_path):
                try:
                    # Keep aspect ratio
                    # FPDF handles aspect ratio automatically if only w is specified,
                    # but we also want to cap h. So we specify both but may need to check proportions.
                    # By passing w=img_w, h=max_img_h, it will distort unless we calculate or FPDF > 2 handles it.
                    # Actually in FPDF, passing w and h might stretch. Passing w=img_w and h=0 keeps aspect ratio.
                    # Let's use w=img_w, h=0
                    pdf.image(abs_path, x=x, y=start_y + 6, w=img_w)
                except Exception as e:
                    self._render_image_placeholder(pdf, x, start_y + 6, img_w, max_img_h, "Corrupted Image")
            else:
                self._render_image_placeholder(pdf, x, start_y + 6, img_w, max_img_h, "Image unavailable")
                
        # Move Y down by max_img_h + 10
        pdf.set_y(start_y + max_img_h + 15)
        
    def _render_image_placeholder(self, pdf: ProfessionalPDF, x: float, y: float, w: float, h: float, text: str):
        pdf.set_xy(x, y)
        pdf.set_fill_color(254, 226, 226) # red-100
        pdf.set_draw_color(239, 68, 68) # red-500
        pdf.rect(x, y, w, h, "DF")
        
        pdf.set_text_color(153, 27, 27) # red-800
        pdf.set_font("helvetica", "B", 10)
        
        # Center text in box
        pdf.set_xy(x, y + (h/2) - 3)
        pdf.cell(w, 6, text, align="C")

