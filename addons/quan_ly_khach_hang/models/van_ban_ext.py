from odoo import models, fields


class VanBanDiCustomer(models.Model):
    _inherit = 'van_ban_di'

    id_khach_hang = fields.Many2one('khach_hang', string='Khách hàng liên quan')


class VanBanDenCustomer(models.Model):
    _inherit = 'van_ban_den'

    id_khach_hang = fields.Many2one('khach_hang', string='Khách hàng liên quan')

