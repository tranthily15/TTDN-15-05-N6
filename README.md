![image](https://github.com/user-attachments/assets/b31dbfb1-7c7d-45c4-b06a-8caa5464ce3f)---
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)



# 1. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 1.1. Clone project.
```
git clone https://gitlab.com/anhlta/odoo-fitdnu.git
```
```
git checkout cntt15_05
```


## 1.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
## 1.3. khởi tạo môi trường ảo.

`python3.10 -m venv ./venv`
Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu

```
source venv/bin/activate
pip3 install -r requirements.txt
```

# 2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.

`docker-compose up -d`

# 3. Setup tham số chạy cho hệ thống

## 3.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5435
xmlrpc_port = 8069
```
Có thể kế thừa từ **odoo.conf.template**


# 4. Chạy hệ thống và cài đặt các ứng dụng cần thiết
Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```

Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.
# 5. cài đặt module quản lý nhân sự
Tìm kiếm 
```
nhan_su 
```
và cài đặt.
#6. Các chức năng chính của module nhân sự 
- Quản lý nhân viên: Lưu trữ thông tin cá nhân, hợp đồng lao động, lịch sử công tác, đào tạo, nghỉ phép, bảo hiểm, và chế độ đãi ngộ.
- Quản lý phòng ban và chức vụ: Xây dựng hệ thống phân cấp phòng ban, vị trí công tác và quan hệ báo cáo.
- Quản lý bảng lương: Tính toán lương theo hợp đồng, phụ cấp, thuế, bảo hiểm và các khoản khấu trừ khác.
![image](https://github.com/user-attachments/assets/af289a64-f4a8-4d56-8988-129e8829cea1)
- Quản lý nghỉ phép: Theo dõi ngày nghỉ của nhân viên.
- Báo cáo nhân sự: Xây dựng các báo cáo tổng hợp về nhân sự
- Quản lý chứng chỉ bằng cấp: Cập nhật chứng chỉ bằng cấp của từng nhân viên
- quản lý khóa đào tạo: xây dựng những khóa đào tạo đồng thời quản lý số giờ tham gia khóa đào tạo của nhân viên
Hoàn tất

    
