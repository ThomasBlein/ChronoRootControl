# ChronoRootControl configuration

After installation, ChronoRootControl application is ready to use on module using selected default.

You can adapt the configuration to your particular setup if you wish. We provided an example user config file that can be used to overwrite the default values.

First, copy the example file `user_config.py.example` to `user_config.py`, and then edit it with your favorite text editor.

```python
"""
Example user configuration file
Copy this file to 'user_config.py' and modify values as needed.
Only include the settings you want to override from default_config.py
"""

class Config(object):
    # Example overrides - uncomment and modify as needed
    
    # Site customization
    # SITE_NAME = "My Custom ChronoRoot"
    # SITE_DESC = "My customized ChronoRoot setup"
    
    # Working directory
    # WORKING_DIR = "/custom/path/to/data"
    
    # Camera configuration
    # CAMS = (1, 2)  # Only use cameras 1 and 2
    # CAM_WARMUP = 5  # Custom warmup time
    
    # Custom camera parameters
    # CAM_PARAMS = {
    #     "format": 'jpg',
    #     'resolution': (1920, 1080),
    #     'brightness': 60,
    #     'contrast': 10,
    #     # ... add any other parameters you want to override
    # }
    
    # Debug settings
    # DEBUG = True
    
    # Hardware configuration
    # SELECTOR_PRESENT = False  # Disable camera multiplexer
```

Noteworthy configuration variables are

* `WORKING_DIR` that defines the root directory where the data are stored (`/srv/ChronoRootData` by default). To use the first USB drive plugged, set it to `/media/usb0`.

* `CAMS` the cameras available to be used with the multiplexer.

* `SELECTOR_PRESENT` that defines if a camera multiplexer is present on the module to be able to control several cameras.

Note that despite being available in the configuration file, the default camera settings are not used at the moment.
