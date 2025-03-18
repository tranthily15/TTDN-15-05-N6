from odoo import models, fields, api


class NhanVienChungChiBangCap(models.Model):
    _name = 'nhan_vien_chung_chi_bang_cap'
    _description = 'Bảng chứa thông tin chứng chỉ bằng cấp'

    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", required=True)
    tuoi = fields.Integer("Tuổi" , related = 'nhan_vien_id.tuoi')

    danh_muc_chung_chi_bang_cap_id = fields.Many2one("danh_muc_chung_chi_bang_cap", string="Danh muc chứng chỉ bằng cấp", required=True)
    ma_chung_chi = fields.Char("Mã chứng chỉ", related = 'danh_muc_chung_chi_bang_cap_id.ma_chung_chi')
    ten_chung_chi = fields.Char("Tên chứng chỉ", related = 'danh_muc_chung_chi_bang_cap_id.ten_chung_chi')
    anh = fields.Binary("Ảnh chứng chỉ")
    loai_chung_chi = fields.Char("Loại chứng chỉ", required=True)
    cap_do = fields.Selection(
        [
            ("so_cap", "Sơ cấp"),
            ("trung_cap", "Trung cấp"),
            ("cao_dang", "Cao đẳng"),
            ("dai_hoc", "Đại học"),
            ("cao_hoc", "Cao học"),
            ("khac", "Khác"),
        ],
        string="Cấp độ",
        required=True
    )
    ngay_cap = fields.Date(string="Ngày cấp")
    ngay_het_han = fields.Date(string="Ngày hết hạn")
    noi_cap = fields.Char(string="Nơi cấp")
    trang_thai = fields.Selection(
        [
            ("hieu_luc", "Hiệu lực"),
            ("het_han", "Hết hạn"),
            ("dang_cho_duyet", "Đang chờ duyệt"),
        ],
        string="Trạng thái",
        default="hieu_luc",
        compute="_compute_trang_thai",
        store=True
    )
    ghi_chu = fields.Text(string="Ghi chú")

    @api.depends('ngay_het_han')
    def _compute_trang_thai(self):
        for record in self:
            if record.ngay_het_han and record.ngay_het_han < fields.Date.today():
                record.trang_thai = "het_han"

   
