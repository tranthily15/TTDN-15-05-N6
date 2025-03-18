from odoo import models, fields, api


class NghiPhep(models.Model):
    _name = 'nghi_phep'
    _description = 'Bảng chứa thông tin nghỉ phép'
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)

    loai_nghi_phep = fields.Selection(
        [
            ('nam', 'Năm'),
            ('om', 'Ốm'),
            ('khong_luong', 'Không lương'),
            ('khac', 'Khác'),
        ],
        string="Loại nghỉ phép", default="om"
    ) 
    ngay_bat_dau = fields.Date("Ngày bắt đầu")
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    so_ngay = fields.Float(string="Số Ngày Nghỉ", compute="_compute_so_ngay", store=True)
    ly_do = fields.Char("Lý do")
    trang_thai = fields.Selection([
            ('cho_duyet', 'Chờ duyệt'),
            ('da_duyet', 'Đã duyệt'),
            ('tu_choi', 'Từ chối')
    ], string="Trạng thái", default='cho_duyet', readonly=True)

    @api.depends("ngay_bat_dau", "ngay_ket_thuc")
    def _compute_so_ngay(self):
        for record in self:
            if record.ngay_bat_dau and record.ngay_ket_thuc:
                record.so_ngay = (record.ngay_ket_thuc - record.ngay_bat_dau).days + 1
            else:
                record.so_ngay = 0

    def action_duyet(self):
        
        self.trang_thai = 'da_duyet'

    def action_tu_choi(self):
        self.trang_thai = 'tu_choi'
