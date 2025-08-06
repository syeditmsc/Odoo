# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models
from odoo.http import request

_logger = logging.getLogger(__name__)


def patch_request_url_root():
    """
    Monkey patch the request object to force HTTPS URLs.
    This function patches the httprequest property to always return HTTPS URLs.
    """
    if not hasattr(request, '_original_httprequest'):
        # Store the original property to avoid double patching
        request._original_httprequest = request.__class__.__dict__.get('httprequest')
        
        # Create a property that forces HTTPS
        def https_url_root_property(self):
            """Property that forces HTTPS URLs"""
            try:
                original_request = request._original_httprequest.__get__(self, self.__class__)
                if original_request and hasattr(original_request, 'url_root'):
                    url_root = original_request.url_root
                    if url_root and url_root.startswith('http://'):
                        # Replace http:// with https://
                        url_root = url_root.replace('http://', 'https://', 1)
                        # Update the original request's url_root
                        original_request.url_root = url_root
                        _logger.debug(f"Forced HTTPS URL: {url_root}")
                    return original_request
                return original_request
            except Exception as e:
                _logger.error(f"Error in HTTPS URL patch: {e}")
                # Fallback to original behavior
                return request._original_httprequest.__get__(self, self.__class__)
        
        # Apply the patch
        request.__class__.httprequest = property(https_url_root_property)
        _logger.info("Successfully patched request.httprequest to force HTTPS URLs")


def unpatch_request_url_root():
    """
    Remove the monkey patch and restore the original behavior.
    """
    if hasattr(request, '_original_httprequest'):
        try:
            # Restore the original property
            request.__class__.httprequest = request._original_httprequest
            delattr(request, '_original_httprequest')
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