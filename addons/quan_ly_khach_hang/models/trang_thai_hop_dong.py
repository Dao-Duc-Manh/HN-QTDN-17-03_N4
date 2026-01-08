from odoo import models, fields, api


class TrangThaiHopDong(models.Model):
    _name = 'trang_thai_hop_dong'
    _description = 'Trạng thái hợp đồng'
    _rec_name = "ten_trang_thai"

    ten_trang_thai = fields.Char("Tên trạng thái", required=True)
    mo_ta = fields.Text("Mô tả")

