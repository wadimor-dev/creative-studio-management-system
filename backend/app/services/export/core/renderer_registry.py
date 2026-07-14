from typing import Dict, Any, Type
from app.services.export.core.enums import RendererType

class RendererRegistry:
    """Plugin-based registry for Renderers."""
    
    def __init__(self):
        self._renderers: Dict[str, Dict[RendererType, Any]] = {
            "pdf": {},
            "excel": {}
        }
        
    def register(self, format_type: str, renderer_type: RendererType, renderer_instance: Any):
        if format_type not in self._renderers:
            self._renderers[format_type] = {}
        self._renderers[format_type][renderer_type] = renderer_instance
        
    def unregister(self, format_type: str, renderer_type: RendererType):
        if format_type in self._renderers and renderer_type in self._renderers[format_type]:
            del self._renderers[format_type][renderer_type]
            
    def get(self, format_type: str, renderer_type: RendererType) -> Any:
        try:
            return self._renderers[format_type][renderer_type]
        except KeyError:
            raise ValueError(f"Renderer for format '{format_type}' and type '{renderer_type.value}' is not registered.")
            
    def list(self) -> dict:
        return {
            fmt: [rt.value for rt in types.keys()] 
            for fmt, types in self._renderers.items()
        }

renderer_registry = RendererRegistry()
