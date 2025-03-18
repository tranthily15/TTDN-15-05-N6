from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, datetime

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _order = 'ten asc, ngay_sinh desc'

    lich_su_cong_tac_ids = fields.One2many ("lich_su_cong_tac", 
                                            inverse_name="nhan_vien_id", 
                                            string="Lịch sử công tác")
    
    hop_dong_lao_dong_ids = fields.One2many ("hop_dong_lao_dong", 
                                             inverse_name="nhan_vien_id", 
                                             string="Hợp đồng lao động")
    nhan_vien_chung_chi_bang_cap_ids = fields.One2many("nhan_vien_chung_chi_bang_cap",
                                            inverse_name="nhan_vien_id",
                                            string="Danh sách nhân viên chứng chỉ bằng cấp")
    khoa_dao_tao_ids  = fields.One2many('nhan_vien_khoa_dao_tao', 
                                              inverse_name='nhan_vien_id',
                                              string="Danh sách nhân viên học khóa học")
    nghi_phep_ids = fields.One2many ("nghi_phep", 
                                     inverse_name="nhan_vien_id", 
                                     string="Nghỉ phép")

    bang_luong_ids = fields.One2many ("bang_luong", 
                                      inverse_name="nhan_vien_id", 
                                      string="Bảng lương")

    ma_dinh_danh = fields.Char("Mã nhân viên", required=True)
    ho_ten_dem = fields.Char("Họ tên đệm", required= True)
    ten = fields.Char("Tên", required= True)
    ho_va_ten = fields.Char("Họ và tên", compute = "_compute_ho_va_ten", store = True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    dia_chi = fields.Char("Địa chỉ")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    so_cccd = fields.Char("Số căn cước công dân")
    so_bao_hiem = fields.Char("Số bảo hiểm")
    ngay_vao_con_ty = fields.Date("Ngày vào công ty")
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    songaynghi = fields.Integer("Số ngày nghỉ", default=14, compute="_compute_so_ngay_nghi", store=True)
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

    chuc_vu = fields.Char("Chức vụ hiện tại", compute="_compute_chuc_vu_phong_ban", store=True)
    phong_ban = fields.Char("Phòng ban hiện tại", compute="_compute_chuc_vu_phong_ban", store=True)
    so_ngay_nghi_du_no = fields.Integer("Số ngày nghỉ âm năm trước", default=0)
    nam_thong_ke = fields.Selection(
        [(str(y), str(y)) for y in range(2003, 2040)],  
        string="Năm thống kê",
        default=str(fields.Date.today().year)
    )
    tong_so_gio_dao_tao_nam = fields.Float(
        string="Tổng số giờ đào tạo trong năm",
        compute="_compute_tong_so_gio_dao_tao_nam", 
        store=True
    )
    @api.depends("khoa_dao_tao_ids.khoa_dao_tao_id.tong_so_gio", 
             "khoa_dao_tao_ids.khoa_dao_tao_id.ngay_dao_tao",
             "khoa_dao_tao_ids.trang_thai",
             "nam_thong_ke")
    def _compute_tong_so_gio_dao_tao_nam(self):
        for record in self:
            try:
                nam_chon = int(record.nam_thong_ke) if record.nam_thong_ke else datetime.now().year
                total_hours = sum(
                    khoa.khoa_dao_tao_id.tong_so_gio
                    for khoa in record.khoa_dao_tao_ids
                    if khoa.khoa_dao_tao_id.ngay_dao_tao and  
                    khoa.trang_thai == "hoan_thanh" and
                    khoa.khoa_dao_tao_id.ngay_dao_tao.year == nam_chon
                )
                record.tong_so_gio_dao_tao_nam = total_hours
            except Exception as e:
                record.tong_so_gio_dao_tao_nam = 0
                _logger.error(f"Lỗi tính tổng giờ đào tạo: {str(e)}") 
    
    trang_thai_dao_tao = fields.Selection(
        [
            ('da_dat', 'Đã đạt'),
            ('chua_dat', 'Chưa đạt'),
        ],
        string="Trạng thái đào tạo",
        compute="_compute_trang_thai_dao_tao",
        store=True
    )

    @api.depends('tong_so_gio_dao_tao_nam')
    def _compute_trang_thai_dao_tao(self):
        for record in self:
            record.trang_thai_dao_tao = 'da_dat' if record.tong_so_gio_dao_tao_nam >= 25 else 'chua_dat'

    @api.depends("nghi_phep_ids.trang_thai", "nghi_phep_ids.loai_nghi_phep", "nghi_phep_ids.so_ngay")
    def _compute_so_ngay_nghi(self):
        for record in self:
            ngay_phep_mac_dinh = 14  
            nam_hien_tai = date.today().year

            tong_ngay_da_nghi = 0
            for nghi_phep in record.nghi_phep_ids:
                if nghi_phep.trang_thai == "da_duyet" and nghi_phep.loai_nghi_phep in ["nam", "om"] and nghi_phep.ngay_bat_dau.year == nam_hien_tai:
                    tong_ngay_da_nghi = tong_ngay_da_nghi + nghi_phep.so_ngay

            so_ngay_phep_nam_nay = ngay_phep_mac_dinh + record.so_ngay_nghi_du_no

            ngay_nghi_du_no_moi = so_ngay_phep_nam_nay - tong_ngay_da_nghi
            if ngay_nghi_du_no_moi < 0:
                record.so_ngay_nghi_du_no = ngay_nghi_du_no_moi  
                record.songaynghi = 0  
            else:
                record.so_ngay_nghi_du_no = 0  
                record.songaynghi = ngay_nghi_du_no_moi



    @api.depends("lich_su_cong_tac_ids.trang_thai", "lich_su_cong_tac_ids.chuc_vu_id", "lich_su_cong_tac_ids.phong_ban_id")
    def _compute_chuc_vu_phong_ban(self):
        for record in self:
            lich_su = record.lich_su_cong_tac_ids.filtered(lambda r: r.trang_thai == "dang_lam")
            if lich_su:
                record.chuc_vu = lich_su[0].chuc_vu_id.ten_chuc_vu if lich_su[0].chuc_vu_id else False
                record.phong_ban = lich_su[0].phong_ban_id.ten_phong_ban if lich_su[0].phong_ban_id else False
            else:
                record.chuc_vu = False
                record.phong_ban = False

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.ma_dinh_danh} - {record.ho_va_ten}"
            result.append((record.id, name))
        return result

    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = record.ho_ten_dem + ' ' + record.ten

    

    @api.onchange("ten", "ho_ten_dem")
    def _default_ma_dinh_danh(self):
        for record in self:
            if not record.ma_dinh_danh:
                year = date.today().year
                existing_records = self.env["nhan_vien"].search([("ma_dinh_danh", "like", f"{year}%")])
                next_number = len(existing_records) + 1
                record.ma_dinh_danh = f"{year}{str(next_number).zfill(5)}"
   
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