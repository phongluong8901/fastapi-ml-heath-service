# Cấu trúc Dữ liệu Hệ thống Y tế (Healthcare Data Dictionary)

Dự án này sử dụng 3 bảng dữ liệu chính để phân tích hành vi bệnh nhân, hiệu quả lâm sàng và quản trị tài chính.

## 1. Bảng PATIENTS (Thông tin Nhân khẩu học)

Mô tả thông tin định danh và đặc điểm của bệnh nhân.

| Cột                  | Mô tả                                                |
| :------------------- | :--------------------------------------------------- |
| `patient_id`         | Khóa chính, định danh duy nhất của bệnh nhân.        |
| `age`                | Độ tuổi của bệnh nhân (dùng để phân tích nhóm tuổi). |
| `gender`             | Giới tính (M/F).                                     |
| `city`               | Thành phố nơi bệnh nhân sinh sống.                   |
| `insurance_provider` | Công ty bảo hiểm cung cấp dịch vụ.                   |
| `chronic_flag`       | Cờ bệnh mãn tính (1: Có, 0: Không).                  |
| `registration_date`  | Ngày bệnh nhân bắt đầu đăng ký vào hệ thống.         |

## 2. Bảng VISITS (Thông tin Lâm sàng)

Mô tả chi tiết về các lần khám và tình trạng bệnh lý.

| Cột                    | Mô tả                                         |
| :--------------------- | :-------------------------------------------- |
| `visit_id`             | Khóa chính, định danh lượt khám.              |
| `patient_id`           | Khóa ngoại, liên kết với bảng PATIENTS.       |
| `visit_date`           | Ngày xảy ra lượt khám.                        |
| `department`           | Khoa/Phòng ban thực hiện khám.                |
| `visit_type`           | Loại hình khám (ER: Cấp cứu, OPD: Ngoại trú). |
| `length_of_stay_hours` | Thời gian nằm viện tính bằng giờ.             |
| `risk_score`           | Mức độ rủi ro (Low/High) - Chỉ số AI dự báo.  |
| `doctor_id`            | Mã định danh bác sĩ điều trị.                 |

## 3. Bảng BILLING (Thông tin Tài chính)

Mô tả quá trình thanh toán và trạng thái xử lý hồ sơ bảo hiểm.

| Cột               | Mô tả                                      |
| :---------------- | :----------------------------------------- |
| `bill_id`         | Khóa chính, định danh hóa đơn.             |
| `visit_id`        | Khóa ngoại, liên kết với bảng VISITS.      |
| `billed_amount`   | Số tiền yêu cầu thanh toán (Tổng chi phí). |
| `approved_amount` | Số tiền được bảo hiểm phê duyệt chi trả.   |
| `claim_status`    | Kết quả thanh toán (Paid/Rejected).        |
| `payment_days`    | Số ngày chờ xử lý thanh toán.              |
| `billing_date`    | Ngày lập hóa đơn.                          |
