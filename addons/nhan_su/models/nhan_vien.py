from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")

    lich_su_cong_tac_ids = fields.One2many ("lich_su_cong_tac", inverse_name="nhan_vien_id", string="Lịch sử công tác")

    #@api.depends
    ho_ten_dem = fields.Char("Họ tên đệm", required= True)
    ten = fields.Char("Tên", required= True)
    ho_va_ten = fields.Char("Họ và tên", compute = "_compute_ho_va_ten", store = True)

    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = record.ho_ten_dem + ' ' + record.ten

    #@api.onchange
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