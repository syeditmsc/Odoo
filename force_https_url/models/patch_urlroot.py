# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models
from odoo.http import request, WebRequest

_logger = logging.getLogger(__name__)


def patch_request_url_root():
    """
    Monkey patch the request object to force HTTPS URLs.
    This function patches the WebRequest.__init__ method to force HTTPS URLs.
    """
    if not hasattr(WebRequest, '_original_init'):
        # Store the original __init__ method
        WebRequest._original_init = WebRequest.__init__
        
        def https_init(self, httprequest):
            """Modified __init__ that forces HTTPS URLs"""
            # Call the original __init__
            WebRequest._original_init(self, httprequest)
            
            # Force HTTPS on the httprequest's url_root
            if hasattr(self, 'httprequest') and self.httprequest:
                if hasattr(self.httprequest, 'url_root'):
                    url_root = self.httprequest.url_root
                    if url_root and url_root.startswith('http://'):
                        # Replace http:// with https://
                        url_root = url_root.replace('http://', 'https://', 1)
                        # Update the original request's url_root
                        self.httprequest.url_root = url_root
                        _logger.debug(f"Forced HTTPS URL: {url_root}")
        
        # Apply the patch
        WebRequest.__init__ = https_init
        _logger.info("Successfully patched WebRequest.__init__ to force HTTPS URLs")


def unpatch_request_url_root():
    """
    Remove the monkey patch and restore the original behavior.
    """
    if hasattr(WebRequest, '_original_init'):
        try:
            # Restore the original __init__ method
            WebRequest.__init__ = WebRequest._original_init
            delattr(WebRequest, '_original_init')
            _logger.info("Successfully removed HTTPS URL patch")
        except Exception as e:
            _logger.error(f"Error removing HTTPS URL patch: {e}")


class ForceHttpsUrlPatch(models.AbstractModel):
    """
    Abstract model to handle the monkey patching of request URLs.
    This model doesn't create any database tables.
    """
    _name = 'force.https.url.patch'
    _description = 'Force HTTPS URL Patch'
    
    @api.model
    def _patch_url_root(self):
        """Method to apply the patch (called during module installation)"""
        patch_request_url_root()
        return True
    
    @api.model
    def _unpatch_url_root(self):
        """Method to remove the patch (called during module uninstallation)"""
        unpatch_request_url_root()
        return True


# Apply the patch immediately when this module is imported
patch_request_url_root() 