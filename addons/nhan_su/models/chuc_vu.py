from odoo import models, fields, api

class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin chức vụvụ'

    ma_chuc_vu = fields.Char("Mã chức vụ", required=True)
    ten_chuc_vu = fields.Char("Tên chức vụ", required=True)
    mo_ta = fields.Text("Mô tả")
    
    lich_su_cong_tac_ids = fields.One2many ("lich_su_cong_tac",
                                            inverse_name="chuc_vu_id",
                                            string="Lịch sử công tác")
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.ma_chuc_vu} - {record.ten_chuc_vu}"
            result.append((record.id, name))
        return result