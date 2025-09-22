from pathlib import Path
import importlib
from types import ModuleType
from typing import Tuple, Optional

def get_scrape_pipeline(project_root: Path) -> Tuple[Optional[ModuleType], Optional[str]]:
    try:
        module = importlib.import_module("src.pipelines.run_scrape")
        return module, None
    except Exception as e:
        return None, str(e)
