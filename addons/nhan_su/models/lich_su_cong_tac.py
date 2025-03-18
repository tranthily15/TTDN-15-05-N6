from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import date

class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin lịch sử công tác'
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    so_dien_thoai = fields.Char(string="Số điện thoại", related="nhan_vien_id.so_dien_thoai", store=True, readonly=True)

    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban", required=True)
    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ", required=True)
    
    loai_chuc_vu = fields.Selection(
        [
            ("Chính", "Chính"),
            ("Kiêm nhiệm", "Kiêm nhiệm"),
        ],
        string="Loại chức vụ", default="Chính"
    )
    
    trang_thai = fields.Selection(
        [
            ("dang_lam", "Đang làm"),
            ("tam_nghi", "Tạm nghỉ"),
            ("chuyen_cong_tac", "Chuyển công tác"),
            ("da_ket_thuc", "Đã kết thúc"),
            ("thoi_viec", "Thôi việc"),
        ],
        string="Trạng thái", default="dang_lam"
    )

    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True, default=fields.Date.today)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc")

    is_active = fields.Boolean(string="Đang làm việc", compute="_compute_is_active", store=True)

    @api.depends("trang_thai")
    def _compute_is_active(self):
        for record in self:
            record.is_active = record.trang_thai == "dang_lam"

    @api.onchange("trang_thai")
    def _onchange_trang_thai(self):
        for record in self:
            if record.trang_thai in ["da_ket_thuc", "thoi_viec", "chuyen_cong_tac"]:
                record.ngay_ket_thuc = date.today()
            else:
                record.ngay_ket_thuc = False

    @api.constrains("nhan_vien_id", "loai_chuc_vu", "trang_thai")
    def _check_nhan_vien_cong_tac(self):
        for record in self:
            if record.nhan_vien_id and record.loai_chuc_vu == "Chính" and record.trang_thai == "dang_lam":
                existing_job = self.env["lich_su_cong_tac"].search([
                    ("nhan_vien_id", "=", record.nhan_vien_id.id),
                    ("loai_chuc_vu", "=", "Chính"),
                    ("trang_thai", "=", "dang_lam"),
                    ("id", "!=", record.id)  
                ])
                if existing_job:
                    raise ValidationError("Nhân viên này đã có một công tác 'Chính' đang làm. Vui lòng kết thúc công tác cũ trước khi tạo mới.")
