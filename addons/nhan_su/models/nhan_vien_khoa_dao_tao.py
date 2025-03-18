from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NhanVienKhoaDaoTao(models.Model):
    _name = 'nhan_vien_khoa_dao_tao'
    _description = 'Danh sách nhân viên tham gia khóa đào tạo'
    _rec_name = 'nhan_vien_id' 

    khoa_dao_tao_id = fields.Many2one('khoa_dao_tao', string="Khóa đào tạo", required=True, ondelete="cascade")
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete="cascade")

    ma_nhan_vien = fields.Char(related='nhan_vien_id.ma_dinh_danh', string="Mã nhân viên", store=True)
    ho_va_ten = fields.Char(related='nhan_vien_id.ho_va_ten', string="Họ và tên", store=True)
    email = fields.Char(related='nhan_vien_id.email', string="Email", store=True)
    so_dien_thoai = fields.Char(related='nhan_vien_id.so_dien_thoai', string="Số điện thoại", store=True)
    gioi_tinh = fields.Selection(related='nhan_vien_id.gioi_tinh', string="Giới tính", store=True)
    chuc_vu = fields.Char(related='nhan_vien_id.chuc_vu', string='Chức vụ hiện tại')
    phong_ban = fields.Char(related='nhan_vien_id.phong_ban', string='Phòng ban hiện tại' )
    ngay_dang_ky = fields.Date(string="Ngày đăng ký", default=fields.Date.context_today)
    trang_thai = fields.Selection([
        ('dang_hoc', 'Đang học'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy_bo', 'Hủy bỏ')
    ], string="Trạng thái", default='dang_hoc', required=True)
    

    _sql_constraints = [
        ('unique_nhan_vien_khoa', 'UNIQUE(nhan_vien_id, khoa_dao_tao_id)',
         'Nhân viên đã đăng ký khóa học này rồi!')
    ]

    @api.constrains('nhan_vien_id', 'khoa_dao_tao_id')
    def _check_unique_registration(self):
        """ Đảm bảo nhân viên không đăng ký trùng khóa học """
        for record in self:
            if self.env['nhan_vien_khoa_dao_tao'].search_count([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('khoa_dao_tao_id', '=', record.khoa_dao_tao_id.id)
            ]) > 1:
                raise ValidationError("Nhân viên đã đăng ký khóa học này rồi!")
        
