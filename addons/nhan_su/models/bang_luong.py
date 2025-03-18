from odoo import models, fields, api

class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương'

    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    thang = fields.Integer(string='Tháng', required=True)
    nam = fields.Integer(string='Năm', required=True)
    so_ngay_cong = fields.Integer(string='Số ngày công', required=True)
    thuong = fields.Float(string='Thưởng', required=True)
    tien_phat = fields.Float(string='Tiền phạt', required=True)
    ngay_tra = fields.Date(string='Ngày trả lương', required=True)
    ghi_chu = fields.Text(string='Ghi chú')

    luong_co_ban = fields.Float(string="Lương cơ bản", compute="_compute_luong_co_ban", store=True, readonly=True)
    phu_cap = fields.Float(string="Phụ cấp", compute="_compute_phu_cap", store=True, readonly=True)

    luong_thuc_nhan = fields.Float(string='Lương thực nhận', compute='_compute_luong_thuc_nhan', store=True)

    @api.depends('nhan_vien_id')
    def _compute_luong_co_ban(self):
        """ Lấy lương cơ bản từ hợp đồng mới nhất của nhân viên """
        for record in self:
            if record.nhan_vien_id:
                hop_dong = self.env['hop_dong_lao_dong'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id)
                ], order="ngay_ky desc", limit=1)
                record.luong_co_ban = hop_dong.luong_co_ban if hop_dong else 0.0

    @api.depends('nhan_vien_id')
    def _compute_phu_cap(self):
        """ Lấy phụ cấp từ hợp đồng mới nhất của nhân viên """
        for record in self:
            if record.nhan_vien_id:
                hop_dong = self.env['hop_dong_lao_dong'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id)
                ], order="ngay_ky desc", limit=1)
                record.phu_cap = hop_dong.phu_cap if hop_dong else 0.0

    @api.depends('luong_co_ban', 'so_ngay_cong', 'thuong', 'phu_cap', 'tien_phat')
    def _compute_luong_thuc_nhan(self):
        """ Tính lương thực nhận dựa trên các thông số """
        for record in self:
            if record.luong_co_ban > 0:
                luong_theo_ngay = record.luong_co_ban / 26 
                luong_tinh = luong_theo_ngay * record.so_ngay_cong
                record.luong_thuc_nhan = luong_tinh + record.thuong + record.phu_cap - record.tien_phat
            else:
                record.luong_thuc_nhan = 0.0