from odoo import models, fields, api

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    lich_su_cong_tac_ids = fields.One2many ("lich_su_cong_tac", inverse_name="phong_ban_id", string="Lịch sử công tác")
