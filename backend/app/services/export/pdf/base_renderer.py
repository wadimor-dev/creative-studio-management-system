"""
Base classes for professional PDF report generation using fpdf2.

Design goals:
- No hardcoded branding (company name / logo) baked into the class.
  All branding comes from `dataset["metadata"]` or a `BrandConfig`,
  so this renderer is reusable across tenants/products.
- Defensive: a missing/corrupt logo file never crashes report generation.
- Consistent, named color palette instead of magic RGB tuples scattered around.
- Summary box layout is responsive to page width/orientation instead of a
  hardcoded x=150 that breaks on A4 vs Letter / portrait vs landscape.
- `{nb}` (total page count) actually resolves, via alias_nb_pages().
"""

from __future__ import annotations

import datetime
import os
from dataclasses import dataclass, field
from io import BytesIO
from typing import Any, Dict, Optional

from fpdf import FPDF

from app.services.export.core.render_context import RenderContext


# --------------------------------------------------------------------------- #
# Palette — single source of truth for report colors
# --------------------------------------------------------------------------- #

class Palette:
    ACCENT = (79, 70, 229)        # brand-600 (indigo)
    TEXT_PRIMARY = (30, 41, 59)   # slate-800
    TEXT_SECONDARY = (100, 116, 139)  # slate-500
    TEXT_MUTED = (148, 163, 184)  # slate-400
    BORDER = (226, 232, 240)      # slate-200
    WHITE = (255, 255, 255)


# --------------------------------------------------------------------------- #
# Branding config
# --------------------------------------------------------------------------- #

@dataclass
class BrandConfig:
    """Branding is data, not code. Pulled from dataset metadata with sane
    fallbacks so a report never renders literally blank."""

    DEFAULT_LOGO_PATH = "app/static/logo.webp"

    company_name: str = "WADIMOR"
    company_suffix: str = "."      # e.g. the "." accent after the name
    tagline: str = ""
    logo_path: Optional[str] = DEFAULT_LOGO_PATH
    footer_text: str = ""

    @classmethod
    def from_metadata(cls, metadata: Dict[str, Any]) -> "BrandConfig":
        company = metadata.get("company", "Creative Division")
        return cls(
            company_name=metadata.get("brand_name", "WADIMOR"),
            company_suffix=metadata.get("brand_suffix", "."),
            tagline=metadata.get("tagline", company),
            logo_path=metadata.get("logo_path", cls.DEFAULT_LOGO_PATH),
            footer_text=metadata.get("footer_text", company),
        )


class ProfessionalPDF(FPDF):
    """Custom FPDF subclass with a professional header/footer.

    Must be constructed via `set_meta()` before `add_page()` is called,
    since `header()` reads `self._report_meta` / `self._brand`.
    """

    LOGO_MAX_WIDTH_MM = 15

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._report_meta: Dict[str, Any] = {}
        self._brand: BrandConfig = BrandConfig()
        self._logo_ok: Optional[bool] = None  # cached existence check
        self.set_auto_page_break(auto=True, margin=15)
        self.alias_nb_pages()

    # -- sanitization -------------------------------------------------- #

    def _sanitize(self, txt: Any) -> Any:
        """fpdf2's core fonts (helvetica) are latin-1 only. Replace any
        character outside that range instead of raising UnicodeEncodeError
        mid-render, which would otherwise abort the whole export."""
        if txt is None or txt == "":
            return txt
        return str(txt).encode("latin-1", "replace").decode("latin-1")

    def cell(self, w=None, h=None, txt="", border=0, ln=0, align="", fill=False, link=""):
        txt = self._sanitize(txt)
        super().cell(w=w, h=h, txt=txt, border=border, ln=ln, align=align, fill=fill, link=link)

    def multi_cell(self, w, h, txt="", border=0, align="J", fill=False, split_only=False):
        txt = self._sanitize(txt)
        super().multi_cell(w=w, h=h, txt=txt, border=border, align=align, fill=fill, split_only=split_only)

    # -- setup ----------------------------------------------------------- #

    def set_meta(self, metadata: Dict[str, Any]) -> None:
        self._report_meta = metadata or {}
        self._brand = BrandConfig.from_metadata(self._report_meta)

    # -- header / footer --------------------------------------------------- #

    def _draw_logo_or_fallback(self, x: float, y: float) -> float:
        """Draws the logo image if it exists and is readable; otherwise draws
        a text-based monogram badge. Returns the x position where the brand
        name text should start."""
        logo_path = self._brand.logo_path

        if self._logo_ok is None:
            self._logo_ok = bool(logo_path) and os.path.isfile(logo_path)

        if self._logo_ok:
            try:
                self.image(logo_path, x=x, y=y, w=self.LOGO_MAX_WIDTH_MM)
                return x + self.LOGO_MAX_WIDTH_MM + 3
            except Exception:
                # Corrupt file / unsupported format (e.g. webp without Pillow
                # installed) — degrade gracefully instead of failing the export.
                self._logo_ok = False

        # Fallback: draw a simple colored monogram badge
        initials = "".join(w[0] for w in self._brand.company_name.split()[:2]).upper() or "R"
        self.set_fill_color(*Palette.ACCENT)
        self.rect(x, y, 10, 10, "F")
        self.set_font("helvetica", "B", 7)
        self.set_text_color(*Palette.WHITE)
        self.set_xy(x, y + 2.5)
        self.cell(10, 5, initials, align="C")
        return x + 10 + 3

    def header(self):
        # Top accent bar
        self.set_fill_color(*Palette.ACCENT)
        self.rect(0, 0, self.w, 3, "F")

        box_x = self.l_margin
        box_y = 8
        text_x = self._draw_logo_or_fallback(box_x, box_y)

        # Brand name + suffix accent
        self.set_xy(text_x, box_y + 2)
        self.set_font("helvetica", "B", 12)
        self.set_text_color(*Palette.TEXT_PRIMARY)
        self.cell(0, 5, self._brand.company_name, ln=False, align="L")
        if self._brand.company_suffix:
            self.set_text_color(*Palette.ACCENT)
            self.cell(0, 5, self._brand.company_suffix, ln=True, align="L")
        else:
            self.ln(5)

        if self._brand.tagline:
            self.set_x(text_x)
            self.set_font("helvetica", "", 6)
            self.set_text_color(*Palette.TEXT_SECONDARY)
            self.cell(0, 4, self._brand.tagline, ln=True, align="L")

        # Right side: generation date + page number
        right_w = 70
        right_x = self.w - self.r_margin - right_w
        self.set_xy(right_x, 8)
        self.set_font("helvetica", "", 7)
        self.set_text_color(*Palette.TEXT_SECONDARY)
        self.cell(right_w, 4, f"Generated: {self._format_generated_at()}", ln=True, align="R")
        self.set_xy(right_x, 12)
        self.cell(right_w, 4, f"Page {self.page_no()}/{{nb}}", ln=True, align="R")

        # Report title
        self.ln(6)
        self.set_font("helvetica", "B", 14)
        self.set_text_color(*Palette.TEXT_PRIMARY)
        report_type = self._report_meta.get("report_type", "Report")
        self.cell(0, 8, report_type, ln=True, align="L")

        period = self._report_meta.get("period", "")
        if period:
            self.set_font("helvetica", "", 8)
            self.set_text_color(*Palette.TEXT_SECONDARY)
            self.cell(0, 5, period, ln=True, align="L")

        self.ln(2)
        self.set_draw_color(*Palette.BORDER)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(*Palette.BORDER)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
        self.set_font("helvetica", "", 7)
        self.set_text_color(*Palette.TEXT_MUTED)
        self.cell(0, 5, self._brand.footer_text, align="L")
        self.cell(0, 5, f"Confidential | Page {self.page_no()}/{{nb}}", align="R")

    def _format_generated_at(self) -> str:
        gen_at = self._report_meta.get("generated_at", "")
        if gen_at:
            try:
                dt = datetime.datetime.fromisoformat(gen_at)
                return dt.strftime("%B %d, %Y  %H:%M")
            except (ValueError, TypeError):
                return str(gen_at)
        return datetime.datetime.now().strftime("%B %d, %Y  %H:%M")


class BasePDFRenderer:
    """Base class for all PDF renderers. Must be stateless — all per-report
    state lives on the `ProfessionalPDF` instance created in `render()`."""

    def render(self, dataset: Dict[str, Any], context: RenderContext) -> BytesIO:
        pdf = ProfessionalPDF(orientation=context.orientation, unit="mm", format=context.page_size)
        pdf.set_meta(dataset.get("metadata", {}))
        pdf.set_auto_page_break(auto=True, margin=context.margin)
        pdf.add_page()

        self.build_document(pdf, dataset, context)

        pdf_output = pdf.output(dest="S")
        pdf_bytes = pdf_output.encode("latin-1") if isinstance(pdf_output, str) else bytes(pdf_output)
        stream = BytesIO(pdf_bytes)
        stream.seek(0)
        return stream

    def build_document(self, pdf: ProfessionalPDF, dataset: Dict[str, Any], context: RenderContext):
        raise NotImplementedError("Subclasses must implement build_document")

    def render_summary(self, pdf: ProfessionalPDF, summary: Dict[str, Any]) -> None:
        """Renders a boxed key/value summary panel anchored to the right
        third of the page. Width-responsive: works on A4/Letter, portrait
        or landscape, instead of a hardcoded x=150."""
        if not summary:
            return

        panel_w = (pdf.w - pdf.l_margin - pdf.r_margin) * 0.38
        panel_x = pdf.w - pdf.r_margin - panel_w
        label_w = panel_w * 0.45
        value_w = panel_w - label_w

        old_y = pdf.get_y()
        pdf.set_xy(panel_x, old_y)
        pdf.set_font("helvetica", "B", 8)
        pdf.set_text_color(*Palette.TEXT_PRIMARY)
        pdf.cell(panel_w, 5, "Summary Overview", ln=True)

        pdf.set_font("helvetica", "", 8)
        pdf.set_text_color(*Palette.TEXT_SECONDARY)
        for key, value in summary.items():
            pdf.set_x(panel_x)
            pdf.cell(label_w, 5, str(key).replace("_", " ").title())
            pdf.cell(value_w, 5, f": {value}", ln=True)

        y_after = pdf.get_y()
        pdf.set_y(max(y_after, old_y) + 5)

        pdf.set_draw_color(*Palette.BORDER)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(3)