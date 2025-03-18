from odoo import models, fields, api


class HopDongLaoDong(models.Model):
    _name = 'hop_dong_lao_dong'
    _description = 'Bảng chứa thông tin hợp đồng lao động'
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)

    so_hop_dong = fields.Char("Số hợp đồng")
    ngay_ky = fields.Date("Ngày ký hợp đồng")
    ngay_bat_dau = fields.Date("Ngày bắt đầu hiệu lực")
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    luong_co_ban = fields.Integer("Lương cơ bản")
    phu_cap = fields.Integer("Phụ cấp")
    dieu_khoan = fields.Char("Điều khoản")

    loai_hop_dong = fields.Selection(
        [
            ('co_thoi_han', 'Xác định thời hạn'),
            ('khong_thoi_han', 'Không xác định thời hạn'),
            ('thu_viec', 'Thử việc'),
            ('thoi_vu', 'thoi_vu'),
        ],
        string= "Loại hợp đồng", default="co_thoi_han"
    ) 

    trang_thai = fields.Selection(
        [
            ('hieu_luc', 'Hiệu lực'),
            ('sap_het_han', 'Sắp hết hạn'),
            ('het_han', 'Hết hạn')
        ],
        string= "Trạng thái", default="hieu_luc"
    )