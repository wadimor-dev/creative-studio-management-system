from typing import Dict, Any
from app.services.export.pdf.base_renderer import BasePDFRenderer, ProfessionalPDF
from app.services.export.core.render_context import RenderContext

class TablePDFRenderer(BasePDFRenderer):
    """Renderer that outputs data in a tabular layout (like old generic export)."""
    
    def build_document(self, pdf: ProfessionalPDF, dataset: Dict[str, Any], context: RenderContext):
        summary = dataset.get("summary", {})
        self.render_summary(pdf, summary)
        
        pdf.ln(5)
        
        # In a table renderer, we expect 'headers' and 'rows' in the dataset if it's purely generic.
        # But if we use 'activities' array, we map it to table rows.
        
        headers = dataset.get("headers", [])
        rows = dataset.get("rows", [])
        
        # If dataset structure is modern (activities), we extract rows
        if not headers and not rows and "activities" in dataset:
            headers = ["Date", "Activity", "Employee", "Status"]
            for act in dataset["activities"]:
                rows.append([
                    str(act.get("date", "-"))[:10],
                    str(act.get("activity", "-")),
                    str(act.get("employee", "-")),
                    str(act.get("status", "-"))
                ])
                
        if not headers or not rows:
            pdf.cell(0, 10, "No data available", align="C")
            return
            
        # Draw table header
        col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / len(headers)
        
        pdf.set_fill_color(241, 245, 249) # slate-100
        pdf.set_text_color(71, 85, 105) # slate-600
        pdf.set_font("helvetica", "B", 8)
        
        for h in headers:
            pdf.cell(col_w, 8, str(h), border=1, fill=True, align="C")
        pdf.ln()
        
        # Draw rows
        pdf.set_font("helvetica", "", 8)
        pdf.set_text_color(30, 41, 59)
        
        for row in rows:
            # Check page break
            if pdf.get_y() > pdf.h - 25:
                pdf.add_page()
                
            # Find max height for multi-cell if needed, but for simplicity use standard cell
            # A more advanced table renderer would use multi_cell for each col and align heights.
            for cell in row:
                # Truncate text if too long
                text = str(cell)
                if len(text) > 40:
                    text = text[:37] + "..."
                pdf.cell(col_w, 7, text, border=1, align="L")
            pdf.ln()
