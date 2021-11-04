import sys
import os

def resource_path(relative_path, production=False):
    """
    
    params:
    relative_path => path to can be modified
    production => activate this function just when copiles, default False
    return => path for finding chrome when copiles
    """
    if production:
        try:
            base_path = sys._MEIPASS
        
        except Exception:
            base_path = os.path.dirname(__file__)
        
        return os.path.join(base_path, relative_path)

    else:
        return relative_path