from odoo import fields, models, api,_
from odoo.exceptions import ValidationError
from datetime import datetime
class Restaurant(models.Model):
    _name ="restaurant.data"
    _description = "Restaurant Data"
    _sql_constraints = [('key_uniq','unique(name)','This restaurant already exist')]


    name = fields.Char("Restaurant Name") 
    mobile = fields.Char("Restaurant Mobile")
    rating = fields.Integer("Restaurant Rating")
    join_date = fields.Date("Join date")
    leave_date = fields.Date("Leave date")
    price = fields.Float("Food Price", default=499)
    description = fields.Text("Description")
    image = fields.Binary(string="restroimg")
    state = fields.Selection(           
    [('yes', 'Yes'), ('no', 'No')],
    string='BestSeller')
    restro_seq_id = fields.Char("Restro Sequence",copy=False)
    visitor_ids = fields.One2many("visitor.data","restaurant_id")
    visitor_count = fields.Integer(compute = "get_visitor_count",store = True)
    history_count = fields.Integer(compute = "get_history_count")
    total_ordered_items = fields.Integer(compute = "get_total_food_items",string="Total Ordered Items" )
    
    
    # Smart Button
    @api.depends("visitor_ids")
    def get_visitor_count(self):
        for rec in self:
            rec.visitor_count = len(rec.visitor_ids)
            
    def action_view_visitor(self):
        visitor_ids =[]
        return{
            'type':"ir.actions.act_window",
            'view_mode':'tree',
            'res_model':'visitor.data',
            'target':'current',
            'domain':[('id','in',self.visitor_ids.ids)]
        }
        
    # Total sum of ordered items 
    @api.depends("visitor_ids.ordered_items")
    def get_total_food_items(self):
        for rec in self:
            total = 0
            for line in rec.visitor_ids:
                total += line.ordered_items
                total += line.ordered_items
            rec.total_ordered_items = total
    
    
    #Gives the difference of days between the join date and today 
    # def days_difference(self):
    #     for rec in self:
    #         if rec.join_date:
    #             join_date = fields.Date.from_string(rec.join_date)
    #             today_date = datetime.now().date()

    #             difference = today_date - join_date

    #         years_difference = difference.days // 365
    #         remaining_days = difference.days % 365
    #         months_difference = remaining_days // 30
    #         remaining_days %= 30
    #         weeks_difference = difference.days // 7
    #         days_difference = difference.days

    #         diff_str = ""
    #         if years_difference:
    #             diff_str += f"{years_difference} year(s) "
    #         if months_difference:
    #             diff_str += f"{months_difference} month(s) "
    #         if weeks_difference:
    #             diff_str += f"{weeks_difference} week(s) "
    #         diff_str += f"{days_difference} day(s)"

    #         rec.date_difference = diff_str
    
    # @api.onchange("mobile")
    # def onchange_mobile(self):
    #     mobile_len = len(self.mobile)
    #     if mobile_len != 10:
    #         raise ValidationError(_('Mobile number must be of 10 digits'))
    
    
    def name_get(self):
        result = []
        print("self ::::::::::::::::::::::::::: ", self)
        for rest in self:
            name = ""
            if rest.restro_seq_id:
                name += rest.restro_seq_id
            
            if rest.name:
                name += ' ' + rest.name
            result.append((rest.id, name))
        return result
    
   
    # @api.model
    def default_get(self, fields):
        print("Valuessssss :::::::::::::::::::::: ", fields, type(fields))
        res = super(Restaurant, self).default_get(fields)
        print("Result :::::::::::::::::::::::::: ", res)
        res.update({'price':299})
        print("result after update ::::::::::::::::::: ", res)
        return res
   
    # @api.model
    # def default_get(self, fields):
    #     seq = self.env['ir.sequence'].next_by_code('restro.sequence')
    #     res = super(Restaurant, self).default_get(fields)
    #     res.update({'restro_seq_id':seq})
    #     return res
    
   
   
#   ORM create method
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('restro.sequence')
        result = super(Restaurant, self).create(vals)
        print("values",vals)
        result.restro_seq_id = seq
        return result
    
    
    
#   ORM write method 
    def write(self, vals):
        result = super(Restaurant, self).write(vals)
        res_history_obj = self.env['restro.history']
        # history_ids = res_history_obj.search(['|', ('name','=', self.name),('','=', self.name)])
        # history_id = res_history_obj.browse([1,3])
        # history_res = res_history_obj.search_read([('name', '=', self.name)],['name'])
        # print("history result ::::::::::::::::::::::::: ", history_res, type(history_res))
        if self.price == vals.get("price"):
            res_history_obj.create({
                'name':self.name,
                'history_desc':'Price Changed' + str(self.price),
            })
            
        return result
    
  
    
    
    def searches(self):
        search = self.env['restaurant.data'].search([('rating','=',5)])
        print("Searches",search)
        for rec in self:
            print("name",rec.name)
            print("sequence",rec.restro_seq_id)
        
        
    @api.depends("price")        
    def get_history_count(self):
        for rec in self:
           history_count = self.env['restro.history'].search_count([('name','=',rec.name)])
           rec.history_count = history_count 
           
    def action_view_history(self):
        history_recs = self.env['restro.history'].search(['|',('name','=',self.name),('price','=',self.price)])
        return {
            'type':"ir.actions.act_window",
            'view_mode':'tree',
            'res_model':'restro.history',
            'target':'current',
            'domain':[('id','in',history_recs.ids)]
        }
        
        
        
class ActivityViewExample(models.Model):
        _name = 'activity.example'
        _inherit = ['mail.thread', 'mail.activity.mixin']
        _description = 'Add Activity view'
        
        name = fields.Char(string="Name")