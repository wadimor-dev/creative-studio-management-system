from io import BytesIO
from app.services.export.core.renderer_registry import renderer_registry
from app.services.export.core.enums import RendererType
from app.services.export.core.render_context import RenderContext

class ExportManager:
    """Coordinator / Facade for managing export processes."""
    
    def __init__(self, registry=renderer_registry):
        self.registry = registry

    def export(self, format_type: str, dataset: dict, renderer_type: RendererType, context: RenderContext = None) -> BytesIO:
        """
        Coordinates the export process.
        - format_type: "pdf", "excel", etc.
        - dataset: The final dataset from Report Engine
        - renderer_type: RendererType.TABLE, RendererType.BLOCK, etc.
        - context: RenderContext with layout/theme settings
        """
        if context is None:
            context = RenderContext()
            
        # Get the appropriate renderer
        renderer = self.registry.get(format_type, renderer_type)
        
        # Render the document (Renderer handles storage resolving inside)
        # We pass context for orientation, margins, etc.
        stream = renderer.render(dataset, context)
        
        # Stream is a BytesIO object containing the final file
        return stream

export_manager = ExportManager()
