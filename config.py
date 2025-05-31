"""
The running configuration that is based on default settings
"""
import os
from default_config import Config

def load_user_config():
    """
    Load user configuration file to override default settings.
    Looks for 'user_config.py' in the same directory as this file.
    """
    try:
        user_config_path = os.path.join(os.path.dirname(__file__), 'user_config.py')
        
        if os.path.exists(user_config_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location("user_config", user_config_path)
            user_config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(user_config)
            
            # Override Config class attributes with user config values
            if hasattr(user_config, 'Config'):
                for attr in dir(user_config.Config):
                    if not attr.startswith('_'):
                        setattr(Config, attr, getattr(user_config.Config, attr))
            
            print(f"User configuration loaded from {user_config_path}")
            return True
    except Exception as e:
        print(f"Warning: Failed to load user configuration: {e}")
    
    return False

# Load user configuration if available
load_user_config()

