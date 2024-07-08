# -*- coding: utf-8 -*-
from . import models
import json, os
from odoo import api, SUPERUSER_ID

def _create_tax_components_setup(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.company'].search([])._create_tax_components_setup()