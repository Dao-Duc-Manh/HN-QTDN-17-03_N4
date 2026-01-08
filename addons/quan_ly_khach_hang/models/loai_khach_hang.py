from odoo import models, fields, api


class LoaiKhachHang(models.Model):
    _name = 'loai_khach_hang'
    _description = 'Bảng chứa thông tin loại khách hàng'
    _rec_name = "loai_khach_hang"
    
    id = fields.Integer("ID", required=True)
    loai_khach_hang = fields.Char("Loại khách hàng", required=True)
    mo_ta = fields.Text("Mô tả")
    khach_hang_ids = fields.One2many('khach_hang', 'id_loai_khach_hang', string="Khách hàng")

