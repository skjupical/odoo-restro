from odoo import fields, models

class RestroHistory(models.Model):
    _name = "restro.history"
    _description = "Restro. History"
    
    name = fields.Char()
    price = fields.Char()
    history_desc = fields.Char("Description")