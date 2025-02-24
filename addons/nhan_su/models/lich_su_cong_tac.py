from odoo import models, fields, api


class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin lich su cong tac'
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban", required=True)
    chuc_vu_id = fields.Many2one("chuc_vu", string="Chức vụ", required=True)
    loai_chuc_vu = fields.Selection(
        [
            ("Chính", "Chính"),
            ("Kiêm nhiệm ", "Kiêm nhiệm"),
        ],
        string= "Loại chức vụ", default="Chính"
    )