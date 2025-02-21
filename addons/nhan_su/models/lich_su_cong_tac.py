from odoo import models, fields, api


class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin lịch sử công tác'

    nhan_vien_id = fields.Many2one("nhan_vien", string = "Nhân viên" , required = True)
    phong_ban_id = fields.Many2one("phong_ban", string="phòng ban", required=True)
    chuc_vu_id = fields.Many2one("chuc_vu", string="chức vụ", required=True)
    loai_chuc_vu = fields.Selection(
        [
            ("Chính", "Chính"),
            ("Kiêm nhiệm ", "Kiêm nhiệm"),
        ],
        string= "Loại chức vụ", default="Chính"
    )
    
    # ma_dinh_danh = fields.Char("Mã định danh", required=True)
    # ngay_sinh = fields.Date("Ngày sinh")
    # que_quan = fields.Char("Quê quán")
    # email = fields.Char("Email")
    # so_dien_thoai = fields.Char("Số điện thoại")
