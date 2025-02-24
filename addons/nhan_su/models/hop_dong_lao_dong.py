from odoo import models, fields, api


class HopDongLaoDong(models.Model):
    _name = 'hop_dong_lao_dong'
    _description = 'Bảng chứa thông tin hợp đồng lao động'
    
    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    trang_thai = fields.Selection(
        [
            ('hieu_luc', 'Hiệu lực'),
            ('sap_het_han', 'Sắp hết hạn'),
            ('het_han', 'Hết hạn')
        ],
        string= "Trạng thái", default="Chính"
    )