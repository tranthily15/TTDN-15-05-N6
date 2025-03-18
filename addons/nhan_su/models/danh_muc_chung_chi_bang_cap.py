from odoo import models, fields, api


class DanhMucChungChiBangCap(models.Model):
    _name = 'danh_muc_chung_chi_bang_cap'
    _description = 'Bảng chưa thông tin danh mục chứng chỉ bằng cấp'

    nhan_vien_chung_chi_bang_cap_id = fields.One2many("nhan_vien_chung_chi_bang_cap",
                                            inverse_name="danh_muc_chung_chi_bang_cap_id",
                                            string="Danh sách nhân viên chứng chỉ bằng cấp")

    ma_chung_chi = fields.Char("Mã chứng chỉ", required=True)                                         
    ten_chung_chi = fields.Char("Tên chứng chỉ", required=True)
    mo_ta = fields.Char("Mô tả")
    
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.ma_chung_chi} - {record.ten_chung_chi}"
            result.append((record.id, name))
        return result
   