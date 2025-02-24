from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _order = 'ten asc, ngay_sinh desc'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_ten_dem = fields.Char("Họ tên đệm", required= True)
    ten = fields.Char("Tên", required= True)
    ho_va_ten = fields.Char("Họ và tên", compute = "_compute_ho_va_ten", store = True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    so_luong_cung_ten = fields.Char("Số lượng cùng tên", compute = "_compute_so_luong_cung_ten", store = True) 
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    anh = fields.Binary("Hình ảnh")
    gioi_tinh = fields.Selection(
        [
            ('nam', 'Nam'),
            ('nu', 'Nữ'),
            ('khac', 'Khác'),
        ],
        string="Giới tính",
        required=True,
        default='nam',
    )

    lich_su_cong_tac_ids = fields.One2many ("lich_su_cong_tac", 
                                            inverse_name="nhan_vien_id", 
                                            string="Lịch sử công tác")
    
    hop_dong_lao_dong_ids = fields.One2many ("hop_dong_lao_dong", 
                                             inverse_name="nhan_vien_id", 
                                             string="Hợp đồng lao động")
    chung_chi_bang_cap_ids = fields.One2many("chung_chi_bang_cap",
                                            inverse_name="nhan_vien_id",
                                            string="Danh sách chứng chỉ bằng cấp"
    )



    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = record.ho_ten_dem + ' ' + record.ten

    @api.onchange("ten", "ho_ten_dem")
    def _default_ma_dinh_danh (self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                chu_cai_dau = ''.join([tu[0][0] for tu in record.ho_ten_dem.lower().split()])
                record.ma_dinh_danh = record.ten.lower() + chu_cai_dau

   
    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        today = date.today()
        for record in self:
            if record.ngay_sinh:
                record.tuoi = today.year - record.ngay_sinh.year - (
                    (today.month, today.day) < (record.ngay_sinh.month, record.ngay_sinh.day)
                )
            else:
                record.tuoi = 0

    @api.constrains('ngay_sinh')
    def _check_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                tuoi = date.today().year - record.ngay_sinh.year - (
                    (date.today().month, date.today().day) < (record.ngay_sinh.month, record.ngay_sinh.day)
                )
                if tuoi < 18:
                    raise ValidationError("Nhân viên phải từ 18 tuổi trở lên.")

    #_sql_constrains
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất')
    ]

    @api.depends('ho_va_ten')
    def _compute_so_luong_cung_ten(self):
        for record in self:
            records = self.env['nhan_vien'].search([
                ('ho_va_ten', '=', 'Lê Tuấn Anh'),
                ('id', '!=', record.id),
            ])
            record.so_luong_cung_ten = len(records)



