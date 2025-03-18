from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class KhoaDaoTao(models.Model):
    _name = "khoa_dao_tao"
    _description = "Quản lý khóa đào tạo"
    _order = "id desc"

    name = fields.Char(string="Tên khóa đào tạo", required=True)
    ma_khoa_dao_tao = fields.Char(string="Mã khóa đào tạo", required=True, copy=False, readonly=True, index=True, default="New")
    mo_ta = fields.Text(string="Mô tả khóa đào tạo")
    ngay_dao_tao = fields.Date(string="Ngày đào tạo")
    dia_diem = fields.Char(string="Địa điểm tổ chức")
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban tổ chức", required=True)
    ghi_chu = fields.Text(string="Ghi chú bổ sung")

    gio_bat_dau = fields.Float(string="Giờ bắt đầu", required=True)
    gio_ket_thuc = fields.Float(string="Giờ kết thúc", required=True)
    tong_so_gio = fields.Float(string="Tổng số giờ đào tạo", compute="_compute_tong_so_gio", store=True)

    danh_sach_nhan_vien_ids = fields.One2many('nhan_vien_khoa_dao_tao', 
                                              inverse_name='khoa_dao_tao_id',
                                              string="Danh sách nhân viên học khóa học")

    @api.model
    def create(self, vals):
        if vals.get('ma_khoa_dao_tao', 'New') == 'New':
            nam_hien_tai = datetime.now().year
            sequence_code = f'KDT{nam_hien_tai}'
            new_code = self.env['ir.sequence'].next_by_code(sequence_code) or '00001'
            vals['ma_khoa_dao_tao'] = f"{sequence_code}{new_code}"
        return super(KhoaDaoTao, self).create(vals)

    @api.constrains("gio_bat_dau", "gio_ket_thuc")
    def _check_time(self):
        for record in self:
            if record.gio_bat_dau >= record.gio_ket_thuc:
                raise ValidationError("Giờ bắt đầu phải nhỏ hơn giờ kết thúc.")

    @api.depends("gio_bat_dau", "gio_ket_thuc")
    def _compute_tong_so_gio(self):
        for record in self:
            record.tong_so_gio = record.gio_ket_thuc - record.gio_bat_dau

    _sql_constraints = [
        ('ma_khoa_dao_tao_uniq', 'UNIQUE(ma_khoa_dao_tao)', "Mã khóa đào tạo phải là duy nhất."),
    ]

