from flask import Blueprint
from typing import List

from .api import api_bp
from .apps import apps_bp
from .auth import auth_bp
from .root import root_bp
from .test import test_bp

blueprints: List[Blueprint] = [
    api_bp,
    apps_bp,
    auth_bp,
    root_bp,
    test_bp,
]

import importlib
import importlib.util
from pathlib import Path
from flask import Blueprint

# Create the main apps blueprint
apps_bp = Blueprint('apps', __name__, url_prefix='/apps')

def discover_and_register_apps(apps_path=None):
    """
    Discover all app folders and register their blueprints to apps_bp
    
    Args:
        apps_path: Path to folder containing app subfolders
                  Defaults to 'apps' in project root
    """
    if apps_path is None:
        # Assuming apps folder is at the same level as your application folder
        apps_path = Path(__file__).parent.parent.parent / 'apps'
    else:
        apps_path = Path(apps_path)

    if not apps_path.exists():
        print(f"Apps folder not found at: {apps_path}")
        return
    
    # Iterate through each subfolder in apps directory
    for app_folder in apps_path.iterdir():
        if not app_folder.is_dir():
            continue
        
        # Check for __init__.py file
        init_file = app_folder / '__init__.py'
        if not init_file.exists():
            print(f"Skipping {app_folder.name}: no __init__.py found")
            continue
        
        try:
            # Dynamic import of the app module
            module_name = f"external_apps_{app_folder.name}"
            spec = importlib.util.spec_from_file_location(module_name, init_file)
            if not spec:
                continue

            module = importlib.util.module_from_spec(spec)

            if not spec.loader:
                continue

            spec.loader.exec_module(module)

            # Register the blueprint
            if hasattr(module, 'bp'):
                apps_bp.register_blueprint(module.bp)
                print(f"✓ Registered blueprint from: {app_folder.name}")

            elif hasattr(module, 'blueprint'):
                apps_bp.register_blueprint(module.blueprint)
                print(f"✓ Registered blueprint from: {app_folder.name}")

            else:
                print(f"⚠ No 'bp' or 'blueprint' attribute found in {app_folder.name}")
                
        except Exception as e:
            print(f"✗ Error loading {app_folder.name}: {e}")

# Auto-discover when this module is imported
discover_and_register_apps('extensions')
print(apps_bp._blueprints)

__all__ = ['apps_bp']

__all__ = ['blueprints']