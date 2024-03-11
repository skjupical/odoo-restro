from odoo import fields, models,api
from odoo.exceptions import ValidationError

class Visitor(models.Model):
    _name ="visitor.data"
    _description = "Visitor Data"
    
    @api.constrains("name","surname")
    def _check_value(self):
        for rec in self:
            if rec.name == rec.surname:
                raise ValidationError("Visitor surname and name cannot be same")

    name = fields.Char("Vistor Name",required = "1")
    surname = fields.Char("Vistor Surname")
    mobile = fields.Char("Vistor Mobile")
    email = fields.Html(string = "email")
    restaurant_id = fields.Many2one("restaurant.data",string="Restaurant", domain=[('rating','>',4)])
    sr_no = fields.Char("Sr.NO")
    Visiting_date = fields.Date("Visited Date")
    tag_ids = fields.Many2many("cuisine.data",string="Tags")
    restaurant_mobile = fields.Char(related = "restaurant_id.mobile",store=True)
    ordered_items = fields.Integer("Ordered Items")