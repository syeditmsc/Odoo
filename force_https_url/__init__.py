from . import models

def post_init_hook(cr, registry):
    """
    Post-installation hook to ensure the patch is applied.
    This is called after the module is installed.
    """
    try:
        from .models.patch_urlroot import patch_request_url_root
        patch_request_url_root()
    except Exception as e:
        import logging
        _logger = logging.getLogger(__name__)
        _logger.error(f"Error applying HTTPS URL patch: {e}") 