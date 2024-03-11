from odoo import fields, models


class Cuisine(models.Model):
    _name ="cuisine.data"
    _description = "Cuisine Data"
    
    
    name = fields.Char("Cuisine Name")
    visitortag_ids = fields.Many2many("visitor.data",string="Visitor")