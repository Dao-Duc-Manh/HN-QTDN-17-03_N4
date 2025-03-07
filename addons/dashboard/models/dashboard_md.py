from odoo import models, fields, api
from odoo.tools import html_escape


class DashboardMD(models.Model):
    _name = 'dashboard_md'
    _description = 'Dashboard Management'

    # Tổng số liệu
    total_van_ban_den = fields.Integer(string="Tổng số văn bản đến", compute="_compute_total_van_ban_den")
    total_van_ban_di = fields.Integer(string="Tổng số văn bản đi", compute="_compute_total_van_ban_di")
    total_nhan_su = fields.Integer(string="Tổng số nhân sự", compute="_compute_total_nhan_su")
    
    # Danh sách văn bản đi
    van_ban_di_list = fields.Many2many('van_ban_di',compute="_compute_van_ban_di_list", string="Danh sách văn bản đi", default=[])
    van_ban_di_text = fields.Text(string="Danh sách văn bản đi", compute="_compute_van_ban_di_text")
    
    # Danh sách văn bản đến
    van_ban_den_list = fields.Many2many('van_ban_den', compute="_compute_van_ban_den_list", string="Danh sách văn bản đến", default=[])
    van_ban_den_text = fields.Text(string="Danh sách văn bản đến", compute="_compute_van_ban_den_text")

    # Danh sách nhân viên
    nhan_vien_list = fields.Many2many('nhan_vien', compute="_compute_nhan_vien_list", string="Danh sách nhân viên", default=[])
    nhan_vien_text = fields.Text(string="Danh sách nhân viên", compute="_compute_nhan_vien_text")
    
    # Công việc đang xử lý
    cong_viec_dang_xu_ly_list = fields.Many2many('cong_viec', compute="_compute_cong_viec_dang_xu_ly_list", string="Công việc đang xử lý", default=[])
    cong_viec_dang_xu_ly_text = fields.Text(string="Danh sách công việc đang xử lý", compute="_compute_cong_viec_dang_xu_ly_text")

    # Công việc đã hoàn thành
    cong_viec_hoan_thanh_list = fields.Many2many('cong_viec', compute="_compute_cong_viec_hoan_thanh_list", string="Công việc đã hoàn thành", default=[])
    cong_viec_hoan_thanh_text = fields.Text(string="Danh sách công việc đã hoàn thành", compute="_compute_cong_viec_hoan_thanh_text")


    # ===== Tính tổng số liệu =====
    @api.depends()
    def _compute_total_van_ban_den(self):
        for record in self:
            record.total_van_ban_den = self.env['van_ban_den'].search_count([])

    @api.depends()
    def _compute_total_van_ban_di(self):
        for record in self:
            record.total_van_ban_di = self.env['van_ban_di'].search_count([])
            
    @api.depends()
    def _compute_total_nhan_su(self):
        for record in self:
            record.total_nhan_su = self.env['nhan_vien'].search_count([])
            
    # ===== Lấy danh sách văn bản đi =====        
    @api.depends()
    def _compute_van_ban_di_list(self):
        for record in self:
            record.van_ban_di_list = self.env['van_ban_di'].search([], order="ngay_di desc", limit=5)  # Lấy 5 văn bản mới nhất
    @api.depends()
    def _compute_van_ban_di_text(self):
        for record in self:
            van_ban_list = self.env['van_ban_di'].search([], order="ngay_di desc", limit=5)
            if van_ban_list:
                text_lines = [f"📄 {vb.id} | {vb.ngay_di} | {vb.so_hieu} | {vb.id_nguoi_phat_hanh.ho_ten} | {vb.id_loai_van_ban.id} | {vb.id_nam.nam}" for vb in van_ban_list]
                record.van_ban_di_text = "<br/>".join(text_lines)  # Ghép với ký tự xuống dòng
            else:
                record.van_ban_di_text = "Không có văn bản đi nào"
                
    # ===== Lấy danh sách văn bản đến =====
    @api.depends()
    def _compute_van_ban_den_list(self):
        for record in self:
            record.van_ban_den_list = self.env['van_ban_den'].search([], order="ngay_den desc", limit=5)

    @api.depends()
    def _compute_van_ban_den_text(self):
        for record in self:
            van_ban_list = self.env['van_ban_den'].search([], order="ngay_den desc", limit=5)
            if van_ban_list:
                text_lines = [f"📄 {vb.id} | {vb.ngay_den} | {vb.so_hieu} | {vb.co_quan_ban_hanh} | {vb.id_loai_van_ban.id} | {vb.id_nam.nam}" for vb in van_ban_list]
                record.van_ban_den_text = "<br/>".join(text_lines)
            else:
                record.van_ban_den_text = "Không có văn bản đến nào"

    # ===== Lấy danh sách nhân viên =====
    @api.depends()
    def _compute_nhan_vien_list(self):
        for record in self:
            record.nhan_vien_list = self.env['nhan_vien'].search([], order="ngay_sinh desc", limit=5)

    @api.depends()
    def _compute_nhan_vien_text(self):
        for record in self:
            nhan_vien_list = self.env['nhan_vien'].search([], order="ngay_sinh desc", limit=5)
            if nhan_vien_list:
                text_lines = [f"👤 {nv.ma_dinh_danh} | {nv.ho_ten} | {nv.ngay_sinh}" for nv in nhan_vien_list]
                record.nhan_vien_text = "<br/>".join(text_lines)
            else:
                record.nhan_vien_text = "Không có nhân viên nào"
    # ===== Lấy danh sách công việc đang xử lý =====
    @api.depends()
    def _compute_cong_viec_dang_xu_ly_list(self):
        for record in self:
            record.cong_viec_dang_xu_ly_list = self.env['cong_viec'].search([('trang_thai.ten_trang_thai', '=', 'Đang xử lý')], order="han_xu_ly asc", limit=5)

    @api.depends()
    def _compute_cong_viec_dang_xu_ly_text(self):
        for record in self:
            cong_viec_list = self.env['cong_viec'].search([('trang_thai.ten_trang_thai', '=', 'Đang xử lý')], order="han_xu_ly asc", limit=5)
            if cong_viec_list:
                text_lines = [f"🛠️ {cv.id} | {cv.ten_cong_viec} | Hạn: {cv.han_xu_ly} | Chủ trì: {cv.chu_tri_giai_quyet.ho_ten}" for cv in cong_viec_list]
                record.cong_viec_dang_xu_ly_text = "\n".join(text_lines)
            else:
                record.cong_viec_dang_xu_ly_text = "Không có công việc đang xử lý"

    # ===== Lấy danh sách công việc đã hoàn thành =====
    @api.depends()
    def _compute_cong_viec_hoan_thanh_list(self):
        for record in self:
            record.cong_viec_hoan_thanh_list = self.env['cong_viec'].search([('trang_thai.ten_trang_thai', 'in', ['Hoàn thành', 'Hoàn thành quá hạn'])], order="ngay_hoan_thanh desc", limit=5)

    @api.depends()
    def _compute_cong_viec_hoan_thanh_text(self):
        for record in self:
            cong_viec_list = self.env['cong_viec'].search([('trang_thai.ten_trang_thai', 'in', ['Hoàn thành', 'Hoàn thành quá hạn'])], order="ngay_hoan_thanh desc", limit=5)
            if cong_viec_list:
                text_lines = [f"✅ {cv.id} | {cv.ten_cong_viec} | Hoàn thành: {cv.ngay_hoan_thanh} | Chủ trì: {cv.chu_tri_giai_quyet.ho_ten}" for cv in cong_viec_list]
                record.cong_viec_hoan_thanh_text = "\n".join(text_lines)
            else:
                record.cong_viec_hoan_thanh_text = "Không có công việc đã hoàn thành"
