from . import models

def post_init_hook(cr, registry):
    """
    Post-installation hook to ensure the patch is applied.
    This is called after the module is installed.
    """
    from .models.patch_urlroot import patch_request_url_root
    patch_request_url_root() 