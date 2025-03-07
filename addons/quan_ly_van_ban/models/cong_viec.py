from odoo import models, fields, api
from datetime import date
import logging
_logger = logging.getLogger(__name__)
class CongViec(models.Model):
    _name = 'cong_viec'
    _description = 'Bảng chứa thông tin công việc'
    _rec_name = "ten_cong_viec"

    ten_cong_viec = fields.Char("Tên công việc", required=True)
    yeu_cau = fields.Text("Yêu cầu xử lý", required=True)
    ngay_tao = fields.Date("Ngày tạo", required=True)
    han_xu_ly = fields.Date("Hạn xử lý", required=True)
    ngay_hoan_thanh = fields.Date("Ngày hoàn thành")
    
    tinh_trang = fields.Selection([
        ('da_nhan', 'Đã nhận'),
        ('huy', 'Huỷ'),
    ], string='Tình trạng')

    trang_thai = fields.Many2one('trang_thai', string='Trạng thái', compute="_compute_trang_thai", store=True , readonly = False)
    
    chi_dao = fields.Many2one('nhan_vien', string="Chỉ đạo")
    chu_tri_giai_quyet = fields.Many2one('nhan_vien', string="Chủ trì giải quyết")
    van_ban_den_ids = fields.Many2one('van_ban_den', string="Văn bản xử lý")


    @api.depends('ngay_hoan_thanh', 'han_xu_ly', 'tinh_trang')
    def _compute_trang_thai(self):
        _logger.info("### COMPUTE TRẠNG THÁI ĐƯỢC GỌI ###")
    
        hoan_thanh = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Hoàn thành')], limit=1) or False
        hoan_thanh_qua_han = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Hoàn thành quá hạn')], limit=1) or False
        huy = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Huỷ')], limit=1) or False
        da_nhan = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đã nhận')], limit=1) or False
        dang_xu_ly = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đang xử lý')], limit=1) or False  # Thêm trạng thái mới

        today = date.today()  # Lấy ngày hiện tại

        for record in self:
            _logger.info(f"Đang tính trạng thái cho công việc ID: {record.id}")
        
            if record.ngay_hoan_thanh:
                if record.han_xu_ly and record.ngay_hoan_thanh > record.han_xu_ly:
                    record.trang_thai = hoan_thanh_qua_han.id if hoan_thanh_qua_han else False
                else:
                    record.trang_thai = hoan_thanh.id if hoan_thanh else False
            elif record.tinh_trang == 'huy':
                record.trang_thai = huy.id if huy else False
            elif record.tinh_trang == 'da_nhan':
                if record.han_xu_ly and today < record.han_xu_ly:
                    record.trang_thai = dang_xu_ly.id if dang_xu_ly else False  # Gán "Đang xử lý" nếu chưa đến hạn
                else:
                    record.trang_thai = da_nhan.id if da_nhan else False  # Nếu hết hạn vẫn chưa hoàn thành
            else:
                record.trang_thai = False  # Nếu không thuộc trường hợp nào