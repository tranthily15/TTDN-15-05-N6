from odoo import models, fields, api

class DaoTaoNhanVien(models.Model):
    _name = "dao_tao_nhan_vien"
    _description = "Thống kê đào tạo nhân viên"
    _auto = False  # Không tạo bảng trong database, chỉ dùng để hiển thị

    nhan_vien_id = fields.Many2one("nhan_vien", string="Nhân viên", readonly=True)
    ho_va_ten= fields.Char("Họ và tên", related="nhan_vien_id.ho_va_ten")
    chuc_vu = fields.Char("Chức vụ hiện tại", related="nhan_vien_id.chuc_vu")
    phong_ban = fields.Char("Phòng ban hiện tại", related="nhan_vien_id.phong_ban")
    nam_thong_ke = fields.Selection(
        [(str(y), str(y)) for y in range(2003, 2040)],  
        string="Năm thống kê",
        default=str(fields.Date.today().year)
    )
    tong_so_gio_dao_tao_nam = fields.Float(string="Tổng số giờ đào tạo", readonly=True)
    trang_thai_dao_tao = fields.Selection(
        [('da_dat', 'Đã đạt'), ('chua_dat', 'Chưa đạt')],
        string="Trạng thái đào tạo",
        readonly=True
    )

    def init(self):
        """Tạo view SQL để lấy dữ liệu từ bảng nhân viên"""
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW dao_tao_nhan_vien AS (
                SELECT 
                    row_number() OVER () AS id,
                    n.id AS nhan_vien_id,
                    n.ho_va_ten,
                    n.chuc_vu,
                    n.phong_ban,
                    n.nam_thong_ke,
                    n.tong_so_gio_dao_tao_nam,
                    n.trang_thai_dao_tao
                FROM nhan_vien n
            )
        """)
