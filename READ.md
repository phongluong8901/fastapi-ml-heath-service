Dự án healthcare-ai-ml-pipeline trên GitHub mà bạn đề cập thường hướng tới việc xây dựng một hệ thống xử lý dữ liệu y tế từ đầu đến cuối (end-to-end) nhằm mục đích ứng dụng Machine Learning (ML) và Trí tuệ nhân tạo (AI) trong lâm sàng hoặc quản lý y tế.

Mặc dù không có quyền truy cập trực tiếp để "chạy" mã nguồn đó ngay lúc này, nhưng dựa trên tên gọi và kiến trúc phổ biến của các kho lưu trữ loại này, tôi có thể giải thích các thành phần cốt lõi mà bạn sẽ gặp trong code:

1. Kiến trúc tổng quát
   Các hệ thống AI trong y tế không chỉ là một thuật toán; đó là một quy trình khép kín:

Data Ingestion (Thu thập dữ liệu): Nhập dữ liệu từ các nguồn như EHR (Hồ sơ sức khỏe điện tử), hình ảnh y tế (DICOM), hoặc dữ liệu cảm biến.

Data Preprocessing/Cleaning (Tiền xử lý): Đây là bước quan trọng nhất trong y tế. Dữ liệu thường không đồng nhất, nhiễu, hoặc thiếu sót. Code sẽ bao gồm các bước chuẩn hóa (standardization) về định dạng (như chuẩn HL7 FHIR), khử nhiễu và gán nhãn dữ liệu.

Model Pipeline (Đường ống mô hình): Huấn luyện các mô hình dự báo (ví dụ: dự đoán nguy cơ bệnh, phân loại hình ảnh X-quang/MRI) và đánh giá độ chính xác (Precision/Recall/F1-score).

Model Serving & Monitoring: Triển khai mô hình thông qua API (thường dùng FastAPI hoặc Flask) để bác sĩ hoặc ứng dụng có thể lấy dự báo theo thời gian thực.

2. Những thách thức đặc thù trong code này
   Khi đọc code này, bạn hãy chú ý đến các phần sau vì chúng là yêu cầu bắt buộc của ngành y tế:

Tính bảo mật & Tuân thủ (Compliance): Kiểm tra xem code có các cơ chế ẩn danh hóa dữ liệu (de-identification) hoặc mã hóa để tuân thủ các quy định như HIPAA hay GDPR hay không.

Tính giải thích được (Explainability): Trong y tế, "hộp đen" (black box) là không thể chấp nhận được. Code có thể sử dụng các thư viện như SHAP hoặc LIME để giúp giải thích tại sao mô hình đưa ra dự đoán đó.

Khả năng kiểm định (Auditability): Mọi thay đổi trong dữ liệu hoặc phiên bản mô hình cần phải được lưu vết để phục vụ kiểm định y tế.

---

Đây là một dự án hệ thống MLOps (Machine Learning Operations) toàn diện trong lĩnh vực chăm sóc sức khỏe, được thiết kế theo tư duy kiến trúc thực tế dành cho doanh nghiệp (Production-first architecture).

Mục tiêu chính của dự án này không chỉ là xây dựng mô hình AI, mà là hướng dẫn cách đưa mô hình từ dữ liệu thô (raw data) lên môi trường sản xuất thực tế trên đám mây (AWS Kubernetes) một cách bài bản, đảm bảo khả năng mở rộng, giám sát và quản trị.

Dưới đây là các khía cạnh chính mà dự án thực hiện:

1. Mục đích kinh doanh của các mô hình AI
   Dự án triển khai hai mô hình học máy chính để giải quyết các bài toán vận hành tại bệnh viện:

Phân loại rủi ro lượt khám (Visit Risk Classifier): Dự đoán mức độ rủi ro (Thấp/Trung bình/Cao) của bệnh nhân dựa trên thông tin cá nhân và dữ liệu thăm khám. Mục tiêu là giúp đội ngũ vận hành bệnh viện chủ động phân loại bệnh nhân và điều phối nhân sự phù hợp.

Dự đoán kết quả yêu cầu thanh toán (Claim Outcome Predictor): Dự đoán trạng thái yêu cầu chi trả bảo hiểm (Đã thanh toán/Đang chờ/Từ chối) dựa trên dữ liệu thanh toán và thăm khám. Mục tiêu là giúp bộ phận tài chính phát hiện các yêu cầu có nguy cơ bị từ chối trước khi gửi đi.

2. Hệ sinh thái MLOps hoàn chỉnh
   Dự án mô phỏng một vòng đời phát triển AI đầy đủ:

Quản lý dữ liệu: Sử dụng DVC (Data Version Control) để quản lý phiên bản dữ liệu và các pipeline huấn luyện.

Quản lý thử nghiệm: Sử dụng MLflow để theo dõi các thí nghiệm, ghi lại các phiên bản mô hình và các thông số kỹ thuật.

Phục vụ mô hình (Serving): Triển khai mô hình thông qua FastAPI và cung cấp giao diện demo bằng Gradio.

Giám sát (Monitoring): Thực hiện giám sát sự trôi dạt dữ liệu (data drift) bằng chỉ số PSI (Population Stability Index) để phát hiện khi nào mô hình bắt đầu hoạt động không hiệu quả và cần huấn luyện lại.

3. Quy trình triển khai trên Cloud (DevOps cho AI)
   Dự án tập trung vào việc tự động hóa và đưa hệ thống lên môi trường thực tế:

CI/CD: Sử dụng GitHub Actions để tự động hóa quy trình kiểm thử và triển khai.

Container hóa: Đóng gói toàn bộ ứng dụng vào Docker.

Triển khai: Đẩy các hình ảnh Docker lên AWS ECR (Elastic Container Registry) và vận hành trên cụm EKS (Amazon Elastic Kubernetes Service) để có khả năng mở rộng.

--
Git: Chỉ nên quản lý các file cấu hình, mã nguồn (.py, .ipynb), và các file .dvc (các file nhỏ chứa thông tin định danh/hash của dữ liệu).

DVC: Sẽ quản lý các tệp dữ liệu thực tế (thường nặng). Khi bạn chạy dvc add, DVC tạo ra file .dvc (file text rất nhẹ) để thay thế. Git sẽ theo dõi file .dvc này, còn dữ liệu thật sẽ được lưu trữ trong thư mục .dvc/cache hoặc trên S3/Cloud Storage của bạn.

-- dvc add
Khi bạn chạy dvc add models/ cho một thư mục, DVC không tạo ra một file .dvc đơn lẻ như khi add một file đơn thuần. Thay vào đó, nó tạo ra một thư mục phiên bản (DVC directory object).

Dưới đây là giải thích chi tiết về các thông số bạn nhìn thấy:

Giải thích các thông số
md5: ... .dir: Đây là mã băm (hash) của toàn bộ nội dung trong thư mục models/. Hậu tố .dir cho biết DVC đang coi đây là một tập hợp nhiều file chứ không phải một file duy nhất.

size: 59779385: Tổng dung lượng (tính bằng byte) của tất cả các file nằm trong thư mục models/.

nfiles: 3: Số lượng file DVC đang theo dõi bên trong thư mục này.

path: models: Đường dẫn mà DVC đang quản lý.

Điều gì đã thực sự xảy ra?
DVC đã "đóng băng" thư mục models/: DVC quét tất cả các file bên trong thư mục models/, tính toán mã băm cho từng file, rồi tạo ra một file mô tả (thường nằm trong .dvc/cache/files/md5/...) chứa danh sách các file đó kèm mã băm tương ứng.

File .dvc được tạo: Trong thư mục gốc của dự án, bạn sẽ thấy một file tên là models.dvc. File này là thứ bạn cần git add và git commit. Nó giống như một "bản đồ chỉ đường" giúp DVC biết cần khôi phục những file nào vào thư mục models/ khi bạn chạy lệnh dvc checkout.

Dữ liệu thật được chuyển vào Cache: Các file thực tế trong models/ đã được chuyển vào thư mục .dvc/cache/. Nếu bạn nhìn vào thư mục models/ hiện tại, bạn sẽ thấy các file đó có thể trông giống như các đường dẫn ảo (symlink hoặc hardlink).

Tại sao lại cần làm vậy?
Hiệu suất: Nếu thư mục models/ của bạn có hàng trăm file (ví dụ: các checkpoint của mô hình), việc quản lý theo kiểu "thư mục" giúp Git không bị quá tải.

Tính nhất quán: Khi bạn cập nhật một file trong thư mục models/ (ví dụ: huấn luyện lại mô hình và lưu đè file .joblib), bạn chỉ cần chạy dvc add models/ một lần, DVC sẽ tự động phát hiện thay đổi trong thư mục và cập nhật file models.dvc.

-- dvc push
Lệnh dvc push đóng vai trò là "cầu nối" để đưa dữ liệu nặng từ máy tính cá nhân của bạn lên kho lưu trữ đám mây (cloud storage) mà DVC quản lý.

Hãy hình dung đơn giản như thế này:

Git quản lý mã nguồn (code) và các file .dvc (file văn bản rất nhẹ chỉ chứa thông tin định danh dữ liệu).

DVC quản lý dữ liệu thực tế (model, bộ dữ liệu lớn, file .joblib nặng).

Khi bạn chạy dvc push, DVC sẽ thực hiện các việc sau:

Kiểm tra: Nó đọc các file .dvc trong dự án của bạn (ví dụ: models.dvc mà bạn vừa tạo) để biết những dữ liệu nào cần phải có trên remote storage.

Đối soát: Nó so sánh dữ liệu hiện có trong thư mục .dvc/cache trên máy bạn với dữ liệu đang nằm trên "Remote" (ví dụ: S3, Google Drive, Azure Blob Storage).

Đẩy dữ liệu (Upload): Những file nào có trong cache nhưng chưa có trên Remote sẽ được upload lên đó.

dvc push: Đẩy dữ liệu từ máy bạn lên Cloud.

dvc pull: Tải dữ liệu từ Cloud về máy bạn (dùng khi bạn vừa clone code về hoặc đồng nghiệp vừa cập nhật model mới).

dvc fetch: Chỉ tải dữ liệu về cache (không tự động copy vào thư mục làm việc của bạn).

--

1. dvc repro (Reproduce - Tái lập)
   Đây là lệnh để chạy toàn bộ pipeline. Khi bạn gõ dvc repro, DVC sẽ kiểm tra trạng thái của toàn bộ hệ thống.

Cách hoạt động: DVC so sánh trạng thái hiện tại của các tệp đầu vào (deps) và các tệp đầu ra (outs) trong dvc.yaml.

Thông minh: Nếu bạn không thay đổi gì cả, DVC sẽ báo: "Pipeline is up to date" (Pipeline đã mới nhất) và không làm gì cả để tiết kiệm thời gian.

Tự động hóa: Nếu bạn thay đổi mã nguồn (src) hoặc dữ liệu đầu vào (model_table.csv), DVC sẽ tự động chỉ chạy lại những bước bị ảnh hưởng. Nó sẽ không chạy lại những phần không thay đổi.

2. dvc dag (Directed Acyclic Graph - Đồ thị có hướng không chu trình)
   Đây là lệnh để trực quan hóa cấu trúc pipeline của bạn. Lệnh này giúp bạn "nhìn thấy" cách các bước trong dự án kết nối với nhau.

Ý nghĩa: Nó hiển thị sơ đồ các giai đoạn (stages) trong dự án. Ví dụ, nó sẽ cho bạn thấy bước train_risk phụ thuộc vào model_table.csv như thế nào.

Tại sao cần dùng: Trong các dự án lớn với nhiều bước huấn luyện phức tạp, dvc dag giúp bạn kiểm tra xem mình đã nối các bước với nhau đúng logic chưa.

---

Tại sao nó "nặng"? Nó không chỉ dừng lại ở việc train một mô hình AI trong Jupyter Notebook rồi thôi. Nó bắt bạn phải làm "bộ tứ quyền lực" của một kỹ sư ML thực thụ: DVC (quản lý dữ liệu), MLflow (quản lý thí nghiệm), FastAPI (phục vụ API), và AWS EKS/Kubernetes (triển khai trên cloud).

---

1. joblib là gì?
   Khi bạn huấn luyện một mô hình (ví dụ: Random Forest), mô hình đó tồn tại trong RAM của máy tính. Nếu bạn tắt máy, mô hình đó sẽ biến mất. Để lưu lại mô hình này, chúng ta cần "đóng gói" (serialize) nó thành một file trên ổ cứng. joblib là thư viện chuyên dụng để làm việc này một cách hiệu quả với các đối tượng chứa nhiều mảng dữ liệu lớn (như numpy arrays có trong các mô hình Scikit-learn).

2. Tại sao lại dùng joblib.load() trong code của bạn?
   Trong đoạn code bạn cung cấp, các hàm load_risk_model() và load_claim_model() có vai trò "đánh thức" mô hình từ ổ cứng:

joblib.load(RISK_MODEL_PATH): Lệnh này lấy file .joblib (vốn là một file nhị phân trên ổ cứng) và "giải mã" nó ngược trở lại thành một đối tượng Python (thường là một pipeline hoàn chỉnh).

Sau khi load: Sau khi lệnh này chạy xong, biến nhận kết quả trả về sẽ là một đối tượng mô hình thực thụ. Bạn có thể gọi model.predict() ngay lập tức để dự đoán dữ liệu mới.

3. Tại sao lại là joblib mà không phải pickle (thư viện gốc của Python)?
   Bạn có thể nghe nói đến pickle — một thư viện mặc định của Python cũng dùng để lưu file. Tuy nhiên, joblib ưu việt hơn trong trường hợp này vì:

Tối ưu cho dữ liệu lớn: Các mô hình ML hiện đại thường chứa rất nhiều dữ liệu dạng số (ma trận, weights). joblib được thiết kế tối ưu để lưu trữ các mảng dữ liệu lớn này một cách nhanh hơn và tiết kiệm dung lượng hơn so với pickle.

Đặc thù của Scikit-learn: Các mô hình trong scikit-learn (như RandomForestClassifier, Pipeline) được khuyến nghị sử dụng joblib để lưu trữ vì tính tương thích rất cao.

Tóm tắt quy trình:
Huấn luyện (Training): Code huấn luyện gọi joblib.dump(model, "path.joblib") để lưu mô hình vào folder models/.

Triển khai (Deployment): Code API của bạn (file bạn vừa gửi) gọi joblib.load("path.joblib") để "tải" mô hình vào bộ nhớ và sẵn sàng nhận dự đoán từ người dùng.

--- training_pipeline.py

1. Kết nối và Thiết lập (Cổng kết nối)
   mlflow.set_tracking_uri & set_registry_uri: Code của bạn đang trỏ đến server MLflow đang chạy tại địa chỉ cục bộ http://127.0.0.1:5000. Đây là nơi chứa cơ sở dữ liệu về các lần chạy thử nghiệm và kho lưu trữ mô hình.

mlflow.set_experiment: Nó tạo hoặc mở một không gian làm việc tên là "healthcare-classification". Mọi kết quả huấn luyện sẽ được gom vào đây để bạn dễ so sánh.

2. Ghi chép nhật ký (Logging)
   Trong Step 11, code thực hiện "nhật ký hóa":

mlflow.log_params: Lưu lại các tham số cấu hình (như n_estimators, max_depth...). Điều này giúp bạn trả lời câu hỏi: "Mô hình tốt nhất được huấn luyện với thông số nào?"

mlflow.log_metric: Lưu lại các chỉ số hiệu suất như accuracy, f1_score, recall.

mlflow.sklearn.log_model: Đây là bước quan trọng nhất. Nó không chỉ lưu file mô hình .joblib mà còn lưu cả các tệp cấu hình đi kèm để MLflow biết cách tải và sử dụng mô hình này sau này.

3. Đăng ký mô hình (Model Registry)
   Trong Step 12, code sử dụng register_model:

Nó đẩy mô hình vừa huấn luyện vào Model Registry. Bạn có thể coi đây là "nhà kho" quản lý các phiên bản mô hình (Version 1, Version 2...).

4. Quản lý trạng thái (Stage Transition)
   Đoạn code này thể hiện quy trình quản lý chất lượng tự động:

client.transition_model_version_stage(..., stage="Staging"): Mọi mô hình sau khi train đều được đưa vào trạng thái "Staging" (chờ duyệt).

Tự động đưa lên Production (Step 15): Nếu mô hình vượt qua ngưỡng (eligible), code tự động dùng transition_model_version_stage để chuyển nó sang trạng thái "Production". Khi đó, nó sẽ tự động lưu trữ (archive) các phiên bản cũ trước đó.

5. Kiểm tra thực tế (Model Verification)
   mlflow.sklearn.load_model: Ở Step 16, code tự tải mô hình vừa lên Production xuống để làm một bài "kiểm tra nhanh" (sample prediction). Nó đảm bảo rằng mô hình không chỉ huấn luyện xong mà còn thực sự hoạt động được trên dữ liệu thực tế.

Tóm tắt luồng đi của dữ liệu qua MLflow:
Tại sao cách làm này chuyên nghiệp?

Tính truy xuất nguồn gốc (Lineage): Bạn luôn biết mô hình đang dùng cho "Production" được sinh ra từ dữ liệu nào, tham số gì, và ai là người huấn luyện.

Giảm thiểu lỗi con người: Không cần phải copy file .joblib thủ công vào folder production. Mọi thứ được quản lý thông qua API của MLflow.

--- logger.py
Đây là một module dùng để lưu nhật ký (log) các dự đoán của mô hình. Trong môi trường Production, việc lưu lại dự đoán giúp bạn biết mô hình đã dự đoán cái gì, từ dữ liệu nào, và khi nào.

Dưới đây là giải thích chi tiết từng dòng:

1. Khai báo thư viện & Cấu hình đường dẫn
   import json, hashlib, logging...: Các thư viện để xử lý dữ liệu JSON, tạo mã băm (hash), và ghi nhật ký.

BASE_DIR = ...: Xác định thư mục gốc của dự án.

LOG_DIR = ...: Tạo một thư mục tên là logs/ (nếu chưa có).

LOG_FILE = ...: Đường dẫn file nhật ký sẽ là logs/predictions.log.

2. Thiết lập Logger
   logger = logging.getLogger("prediction_logger"): Tạo một đối tượng logger riêng biệt.

logger.setLevel(logging.INFO): Chỉ lưu các thông tin ở mức INFO trở lên (bỏ qua các thông tin rác).

if not logger.handlers:: Kiểm tra xem logger đã được cài đặt handler chưa để tránh bị ghi lặp log nhiều lần.

file_handler = logging.FileHandler(...): Chỉ định lưu log vào file predictions.log với encoding utf-8 (để tránh lỗi font).

formatter = logging.Formatter("%(message)s"): Cấu trúc log chỉ là nội dung tin nhắn thuần túy (không kèm timestamp hệ thống vì ta đã tự thêm timestamp riêng).

3. Hàm Hashing (Tạo vân tay dữ liệu)
   json.dumps(input_data, sort_keys=True): Chuyển dữ liệu đầu vào (dict) thành chuỗi JSON. sort_keys=True cực kỳ quan trọng để đảm bảo cùng dữ liệu sẽ luôn ra cùng một chuỗi, kể cả khi thứ tự các key trong dict bị đảo lộn.

hashlib.sha256(...).hexdigest(): Tạo ra một mã chuỗi duy nhất (mã băm) đại diện cho dữ liệu đầu vào đó.

Tại sao cần? Nếu bạn cần truy vết xem dữ liệu này đã từng được dự đoán chưa mà không muốn lưu lại toàn bộ dữ liệu thô (vì dữ liệu thô có thể rất lớn và nhạy cảm), mã hash là giải pháp thay thế hoàn hảo.

4. Hàm Ghi Log
   Đây là hàm bạn gọi mỗi khi mô hình đưa ra dự đoán:

log_entry = { ... }: Xây dựng một bản ghi (dạng Dictionary) gồm:

timestamp: Thời điểm dự đoán (theo múi giờ UTC).

model_name, model_version: Lưu lại phiên bản mô hình nào đã dự đoán (rất quan trọng để debug).

input_hash: Vân tay của dữ liệu đầu vào.

prediction: Kết quả dự đoán.

logger.info(json.dumps(log_entry)): Chuyển bản ghi sang định dạng JSON (thành một dòng văn bản) và đẩy vào file predictions.log.

Tóm tắt ý nghĩa:
Đoạn code này chuyển các dự đoán từ dạng "biến trong bộ nhớ" thành dạng "dữ liệu vĩnh viễn trên đĩa cứng" theo cấu trúc JSON. Việc lưu log dạng này giúp ích cho:

Kiểm toán (Auditing): Biết được mô hình đã trả lời gì cho khách hàng.

Theo dõi dữ liệu (Data Drift): Dựa vào input_hash để biết khi nào dữ liệu đầu vào thay đổi quá nhiều so với lúc train.

Debug: Nếu mô hình dự đoán sai, bạn có thể lấy input_hash để tìm lại dữ liệu gốc và kiểm tra lại.

--- drift_monitoring.py
Đây là module Giám sát sự trôi dạt dữ liệu (Data Drift Monitoring).

Trong MLOps, dữ liệu trong thực tế (Production) có thể thay đổi theo thời gian so với dữ liệu dùng để huấn luyện (Training). Nếu dữ liệu đầu vào thay đổi quá nhiều, mô hình sẽ không còn chính xác nữa. Module này dùng Population Stability Index (PSI) để đo lường mức độ thay đổi đó.

1. Ý nghĩa các khái niệm
   Baseline (Đường cơ sở): Phân phối của dữ liệu tại thời điểm huấn luyện (được lưu trong feature_baseline.json).

PSI (Population Stability Index): Một chỉ số thống kê dùng để đo xem phân phối của dữ liệu hiện tại khác biệt như thế nào so với dữ liệu gốc.

PSI < 0.1: Dữ liệu ổn định.

0.1 <= PSI < 0.2: Dữ liệu có sự thay đổi nhẹ.

PSI >= 0.2: Dữ liệu thay đổi đáng kể, cần huấn luyện lại mô hình.

2. Giải thích chi tiết các hàm
   Nhóm tính toán (Math & Logic)
   calculate_psi: Công thức toán học tính khoảng cách giữa hai phân phối. Nó sử dụng logarit để so sánh tỷ lệ giữa "cái kỳ vọng" (training) và "cái thực tế" (production).

build_actual_distribution: Sử dụng np.histogram để chia dữ liệu thực tế vào các "rổ" (bins) giống y hệt như cách đã chia dữ liệu lúc huấn luyện. Đây là bước quan trọng để đảm bảo việc so sánh là công bằng.

Nhóm truy xuất dữ liệu (Data Loading)
load_baseline: Đọc file cấu hình chứa thông tin phân phối gốc (distribution và bin_edges).

load_prediction_logs: Đọc file predictions.log mà bạn đã tạo ở module trước. Nó lọc lấy dữ liệu thô (input_data) để tính toán lại phân phối hiện tại.

Nhóm thực thi (The Orchestrator)
run_psi_monitor: Đây là hàm chính (giống như "trái tim" của file này):

Lấy thông tin baseline của tính năng cần kiểm tra (ví dụ: length_of_stay_hours).

Đọc toàn bộ lịch sử dự đoán từ file log.

Tính toán phân phối thực tế của dữ liệu mới.

Gọi hàm calculate_psi để lấy kết quả.

Trả về một kết quả JSON chi tiết cho biết: Đang bình thường hay đã đến lúc cần train lại mô hình.

--- claim_schema.py
File này sử dụng thư viện Pydantic để định nghĩa cấu trúc dữ liệu đầu vào (Schema) cho API dự đoán Claim (yêu cầu chi trả bảo hiểm).

Trong FastAPI, đây là "hợp đồng" giữa người dùng và hệ thống. Nếu người dùng gửi dữ liệu thiếu hoặc sai kiểu (ví dụ: gửi chữ vào trường age), Pydantic sẽ tự động báo lỗi ngay lập tức.

Phân tích ý nghĩa từng phần:
BaseModel: Là lớp cơ sở của Pydantic. Mọi class định nghĩa schema đều phải kế thừa từ đây.

Field(..., example=...):

... (Ellipsis): Có nghĩa là trường này là bắt buộc (required). Không có nó, API sẽ trả về lỗi.

example: Cực kỳ quan trọng cho Swagger UI (/docs). Khi bạn mở trình duyệt lên, Swagger sẽ tự động điền sẵn giá trị này vào ô input để bạn test nhanh mà không cần gõ từ đầu.

Kiểu dữ liệu (int, str, float): Pydantic sẽ thực hiện Type Validation. Nếu dữ liệu gửi vào là age: "không biết", Pydantic sẽ báo lỗi 422 Unprocessable Entity vì nó không thể chuyển chuỗi đó thành int.

Vai trò của Schema này trong hệ thống:
Tự động hóa tài liệu API: Nhờ định nghĩa này, FastAPI tự động tạo bảng mô tả request cho bạn trên trang http://127.0.0.1:8000/docs.

Làm sạch dữ liệu: Trước khi vào đến hàm dự đoán (predictor.py), dữ liệu đã được Pydantic kiểm tra tính hợp lệ. Bạn không cần viết code if để check xem age có phải là số không, vì Pydantic đã làm xong việc đó.

Cầu nối dữ liệu:

Trong routers/claim.py, bạn nhận dữ liệu qua biến request: ClaimPredictionRequest.

Sau đó bạn gọi request.model_dump() (đã thấy trong traceback lỗi của bạn) để chuyển toàn bộ dữ liệu này thành một dictionary Python thuần túy để nạp vào mô hình ML.

--- risk_schema.py
Tương tự như claim_schema.py, file risk_schema.py này đóng vai trò là "bộ lọc" cho dữ liệu đầu vào của mô hình Dự đoán rủi ro (Risk Prediction).

Tại sao schema này lại khác với claim_schema?
Nếu bạn so sánh hai file này, bạn sẽ thấy sự khác biệt về danh sách các trường (fields). Điều này là hoàn toàn chính xác và cần thiết:

Tính chuyên biệt: Mỗi mô hình học máy yêu cầu một bộ "đặc trưng" (features) riêng.

Mô hình Risk chỉ cần 14 trường dữ liệu để dự đoán.

Mô hình Claim cần 18 trường (nhiều hơn vì nó cần thêm các thông tin về chi phí như billed_amount hay risk_score làm đầu vào).

Tính nhất quán: Các kiểu dữ liệu (int, str, float) trong schema này phải khớp chính xác với những gì mô hình đã được huấn luyện trong MODEL_CONFIG.

Tầm quan trọng trong hệ thống API của bạn:
Chặn rác: Nếu một người dùng hoặc ứng dụng (Gradio UI) gửi thiếu một trường (ví dụ quên gửi visit_month), FastAPI sẽ chặn lại ngay lập tức với lỗi 422 Unprocessable Entity trước khi nó kịp chạm tới mô hình. Điều này bảo vệ mô hình không bị crash do thiếu dữ liệu đầu vào.

Chuyển đổi kiểu dữ liệu (Type Conversion): Nếu người dùng gửi age: "52" (dạng chuỗi từ URL), Pydantic sẽ tự động chuyển nó thành số 52 (dạng int) để truyền vào hàm dự đoán.

Tài liệu sống: Khi bạn mở Swagger UI (/docs), Pydantic tự động hiển thị mô hình yêu cầu này giúp bạn biết chính xác cần điền những thông tin gì để API hoạt động.

--- model_loader.py
Đây là giải thích chi tiết cho từng dòng code trong services/model_loader.py. File này đóng vai trò là "cây cầu" kết nối ứng dụng của bạn với MLflow Model Registry để lấy mô hình đã huấn luyện.

1. Khởi tạo và Thiết lập (Setup)
   import mlflow, mlflow.pyfunc, MlflowClient: Nhập các thư viện cần thiết để tương tác với server MLflow.

MLFLOW_TRACKING_URI = "http://127.0.0.1:5000": Địa chỉ server MLflow bạn đang chạy.

mlflow.set_tracking_uri(...): Ra lệnh cho MLflow biết cần lấy mô hình từ đâu.

client = MlflowClient(): Tạo một "khách hàng" (client) để gửi yêu cầu đến server (như liệt kê phiên bản, chuyển đổi stage, v.v.).

2. Hàm hỗ trợ: get_model_version
   Hàm này giúp lấy số phiên bản mới nhất của mô hình dựa trên trạng thái (stage):

client.get_latest_versions(...): Gửi yêu cầu đến server để hỏi xem phiên bản mới nhất của model_name trong stage (ví dụ: 'Production') là bao nhiêu.

if not versions: raise Exception(...): Nếu không tìm thấy mô hình (do chưa đăng ký hoặc chưa có model nào ở stage đó), chương trình sẽ dừng lại và báo lỗi.

return versions[0].version: Trả về số phiên bản (ví dụ: '1').

3. Hàm tải mô hình: load_risk_model & load_claim_model
   Hai hàm này có cấu trúc giống nhau, dùng để nạp mô hình vào bộ nhớ:

model_name: Tên mô hình đã được đăng ký trên MLflow (phải trùng khớp với tên khi đăng ký).

stage: Trạng thái mô hình cần lấy ('Production' hoặc 'Staging').

model_uri = f"models:/{model_name}/{stage}": Tạo một địa chỉ định danh (URI) chuẩn của MLflow. Nó cho phép MLflow biết chính xác cần lấy cái gì ở đâu.

model = mlflow.pyfunc.load_model(model_uri): Đây là bước quan trọng nhất. Nó tải toàn bộ mô hình (đã đóng gói) từ server về RAM, sẵn sàng để thực hiện lệnh .predict().

return model, model_name, version: Trả về 3 thông tin để ứng dụng sử dụng:

model: Đối tượng mô hình để dự đoán.

model_name: Tên mô hình (để ghi log).

version: Số phiên bản (để biết chính xác bạn đang dùng model nào).

Tại sao code này lại an toàn và chuyên nghiệp?
Không Hard-code đường dẫn: Bạn không cần trỏ đến file .joblib cụ thể nào cả. Nếu bạn train lại mô hình mới, đăng ký nó lên MLflow với cùng tên đó, code này tự động lấy phiên bản mới nhất mà không cần sửa code.

Tính phân tầng (Stage Separation):

Bạn tách biệt môi trường Production cho các model đã ổn định (Risk).

Bạn tách biệt môi trường Staging cho các model đang thử nghiệm (Claim).

Điều này giúp ứng dụng của bạn luôn chạy ổn định, tránh việc dùng nhầm mô hình chưa đạt yêu cầu.

--- predictor.py
Đây là module Dịch vụ dự đoán (Prediction Service). Nó đóng vai trò là "người trung gian" kết nối giữa API (FastAPI), Mô hình (MLflow), và Bộ phận giám sát (Logger).

Dưới đây là phân tích chi tiết cách vận hành của module này:

1. Luồng xử lý một yêu cầu dự đoán
   Mỗi khi bạn gửi dữ liệu qua API, hàm predict_risk_result hoặc predict_claim_result sẽ thực hiện quy trình 4 bước sau:

Bước 1: Tải mô hình (load\_...\_model): Gọi đến module model_loader để "mượn" mô hình từ MLflow (xử lý việc lấy đúng phiên bản đang ở stage Production/Staging).

Bước 2: Chuẩn bị dữ liệu: pd.DataFrame([data]) chuyển đổi từ từ điển (JSON input) thành định dạng DataFrame mà Scikit-learn yêu cầu.

Bước 3: Dự đoán: model.predict(input_df) chạy mô hình để ra kết quả, sau đó ép kiểu kết quả về dạng chuỗi (prediction_str).

Bước 4: Ghi nhật ký (Logging): Gọi hàm log_prediction từ module giám sát để lưu lại vết của lần dự đoán này vào file predictions.log.

2. Các điểm kỹ thuật nổi bật
   hasattr(model, "predict_proba"): Đây là cách viết code cực kỳ thông minh. Không phải mô hình nào cũng có khả năng đưa ra xác suất (ví dụ: một số mô hình chỉ đưa ra nhãn 0 hoặc 1). Code này kiểm tra xem mô hình có khả năng tính xác suất hay không, nếu có thì nó sẽ lấy xác suất đó (predict_proba) và trả về cho người dùng.

probabilities.tolist(): Kết quả từ predict_proba thường là một mảng numpy (đối tượng máy tính). API cần chuyển nó về danh sách Python (list) để có thể chuyển thành JSON phản hồi cho người dùng.

Khối try-except trong phần xác suất: Giúp API của bạn không bị "sập" (crash) nếu chẳng may mô hình lỗi ở bước tính xác suất. Thay vào đó, nó sẽ trả về thông báo lỗi cho người dùng thay vì làm dừng server.

3. Tại sao cấu trúc này rất tốt cho dự án của bạn?
   Tính tái sử dụng: Bạn có thể gọi predict_risk_result từ bất cứ đâu: từ API, từ script chạy batch, hoặc từ Gradio UI.

Tính an toàn (Resilience): Việc dùng try-except xung quanh các thành phần như predict_proba giúp API của bạn "lì" hơn trước các lỗi nhỏ từ mô hình.

Khả năng giám sát: Việc tích hợp log_prediction trực tiếp trong hàm dự đoán đảm bảo rằng bạn không bao giờ quên ghi log. Mỗi khi có dự đoán, log sẽ được tạo tự động.

--- claim_router.py
Đây là tệp định nghĩa Router trong FastAPI. Nó đóng vai trò là "người tiếp tân" của hệ thống, chuyên nhận yêu cầu từ người dùng và điều phối công việc cho các bộ phận khác.

Giải thích chi tiết các thành phần:
router = APIRouter():

Đây là cách FastAPI chia nhỏ ứng dụng. Thay vì nhét tất cả code vào một file main.py khổng lồ, bạn sử dụng APIRouter để gom nhóm các endpoint liên quan đến claim vào một file riêng.

@router.post("/claim"):

Đây là một Decorator định nghĩa đây là một phương thức POST.

Khi ứng dụng FastAPI của bạn chạy, nó sẽ tạo ra một endpoint có đường dẫn là /claim. Phương thức POST được chọn vì bạn đang gửi dữ liệu (request) lên để mô hình xử lý.

request: ClaimPredictionRequest:

Đây là chỗ "phép thuật" của Pydantic xuất hiện. FastAPI sẽ tự động kiểm tra dữ liệu người dùng gửi lên. Nếu dữ liệu không khớp với cấu trúc đã định nghĩa trong claim_schema.py, hệ thống sẽ tự động trả về lỗi 422 Unprocessable Entity ngay lập tức. Bạn không cần phải viết code kiểm tra kiểu dữ liệu thủ công.

result = predict_claim_result(request.model_dump()):

request.model_dump(): Chuyển đổi dữ liệu từ đối tượng Pydantic sang kiểu dict (dạng dữ liệu Python cơ bản).

Sau đó, nó gọi hàm predict_claim_result từ dịch vụ (predictor.py) để lấy kết quả từ mô hình AI.

return result:

Kết quả từ mô hình sẽ được FastAPI tự động chuyển đổi thành định dạng JSON để gửi ngược lại cho người dùng.

Mối quan hệ trong hệ thống của bạn:
Người dùng gửi dữ liệu đến /claim.

FastAPI kiểm tra tính hợp lệ qua ClaimPredictionRequest.

Router chuyển dữ liệu đó cho predictor.py.

Predictor hỏi model_loader.py để lấy mô hình, dự đoán xong rồi lưu log.

Router nhận kết quả và trả về cho người dùng.

--- gradio_app.py
Gradio App của bạn hiện đang đóng vai trò là Frontend (Giao diện người dùng). Nó hoàn toàn tách biệt với backend FastAPI, giao tiếp thông qua giao thức HTTP.

Dưới đây là một số điểm cần lưu ý để ứng dụng của bạn chạy mượt mà:

1. Luồng hoạt động của UI
   gr.Blocks: Đây là cách xây dựng UI nâng cao trong Gradio, cho phép bạn chia layout thành các cột (gr.Column), hàng (gr.Row) và tab (gr.Tab).

requests.post: Khi bạn nhấn nút "Predict", Gradio gửi toàn bộ dữ liệu từ các ô nhập liệu về FastAPI qua cổng 8000.

Xử lý dữ liệu:

FastAPI nhận dữ liệu -> Kiểm tra Schema Pydantic -> Chuyển vào mô hình ML.

Sau đó FastAPI trả về JSON -> Gradio nhận JSON -> Hiển thị kết quả lên gr.Textbox.

2. Một số lỗi phổ biến cần tránh
   Sai cổng: Đảm bảo FastAPI đang chạy ở cổng 8000 (theo FASTAPI_BASE_URL), còn Gradio chạy ở một cổng khác (mặc định là 7860).

Lỗi định dạng:

Trong hàm predict_risk_ui, dòng return str(result) của bạn đang trả về toàn bộ dictionary dưới dạng chuỗi. Nếu API trả về {"prediction": "High"}, người dùng sẽ thấy {'prediction': 'High'}.

Khuyên dùng: Hãy truy xuất cụ thể trường kết quả như bạn đã làm ở hàm predict_claim_ui:
return result.get("prediction", "No prediction").

3. Tối ưu trải nghiệm (UX)
   Vì các trường nhập liệu của bạn khá nhiều, bạn có thể cân nhắc một vài cải tiến nhỏ:

Sử dụng gr.Slider thay cho gr.Number: Đối với các giá trị có khoảng xác định như visit_month (1-12) hoặc visit_dayofweek (0-6), Slider giúp người dùng không bao giờ nhập sai số.

Thêm gr.JSON: Nếu bạn muốn xem cả xác suất (probabilities) trả về từ mô hình, hãy thêm một ô gr.JSON vào UI để hiển thị cấu trúc dữ liệu rõ ràng hơn thay vì chỉ dùng gr.Textbox.

--- Dockerfile.api
Đây là file Dockerfile cơ bản và hiệu quả cho dự án FastAPI của bạn. Nó được tối ưu hóa để chạy trong môi trường container với hiệu suất tốt và dung lượng nhẹ.

Giải thích chi tiết từng câu lệnh:
FROM python:3.11-slim: Sử dụng phiên bản Python 3.11 với hệ điều hành Debian "slim" (siêu nhẹ). Việc này giúp Docker image của bạn không quá nặng, tiết kiệm tài nguyên khi triển khai lên Cloud.

WORKDIR /app: Thiết lập thư mục làm việc mặc định là /app bên trong container.

ENV ...:

PYTHONDONTWRITEBYTECODE=1: Ngăn không cho Python tạo ra các file .pyc (giúp giữ container sạch).

PYTHONUNBUFFERED=1: Đảm bảo log của Python được hiển thị ngay lập tức trên terminal của Docker, giúp bạn debug dễ dàng hơn.

COPY requirements.txt . & RUN pip install ...: Sao chép file danh sách thư viện và cài đặt chúng. Mẹo: Việc để lệnh copy và cài đặt trước khi copy toàn bộ code giúp tận dụng "Docker Layer Caching" – lần sau nếu bạn sửa code, Docker sẽ không cần cài lại thư viện nữa, giúp build cực nhanh.

COPY ...: Sao chép các thư mục dự án (api, monitoring, models, v.v.) vào bên trong container.

EXPOSE 8000: Thông báo cho Docker rằng container này sẽ lắng nghe ở cổng 8000.

CMD [...]: Lệnh khởi chạy FastAPI khi container bắt đầu hoạt động.

--- docker-compose.yml
Đây là file docker-compose.yml để điều phối toàn bộ hệ thống của bạn. Nó hoạt động như một "người quản lý" giúp kết nối các container lại với nhau mà không cần bạn phải thao tác thủ công nhiều lần.

Giải thích các thành phần trong file Compose:
version: "3.9": Phiên bản cấu trúc của Docker Compose.

services:: Định nghĩa các "thành viên" trong hệ thống của bạn.

api: Định nghĩa container chạy FastAPI.

build: Chỉ định lấy hướng dẫn từ Dockerfile.api.

ports: Ánh xạ cổng 8000 của container ra cổng 8000 trên máy tính thật của bạn.

gradio: Định nghĩa container chạy giao diện UI.

environment: Đây là phần quan trọng nhất. Nó truyền biến FASTAPI_BASE_URL vào bên trong container Gradio. Khi container Gradio chạy, nó sẽ biết rằng API của nó nằm ở địa chỉ http://api:8000 (tên api ở đây được Docker tự hiểu là tên service của container API).

depends_on: Ra lệnh cho Docker phải khởi động api trước khi bật gradio, tránh việc Gradio khởi chạy mà không tìm thấy API để kết nối.

-- mlflow
Câu trả lời ngắn gọn là: Không, các luồng route (đường dẫn API) không chạy trực tiếp qua MLflow.

Để giúp bạn hiểu rõ "ai làm việc gì" trong hệ thống, hãy hình dung các luồng dữ liệu như sau:

1. Luồng dữ liệu "Sống" (Runtime) - KHÔNG qua MLflow
   Khi người dùng tương tác với API (qua Gradio), luồng dữ liệu là:

Gradio → FastAPI (Router: /predict/...) → Predictor (Logic dự đoán).

Tại bước Predictor, nó thực hiện việc Tải mô hình. Chính ở đây, nó mới "gọi điện" sang MLflow Server để lấy mô hình về RAM của FastAPI.

Kết quả: Sau khi có mô hình trong RAM, việc dự đoán diễn ra ngay tại FastAPI.

Tại sao lại như vậy? Nếu luồng dữ liệu (request) phải chạy qua MLflow Server mỗi khi dự đoán, hệ thống sẽ cực kỳ chậm. MLflow được thiết kế để quản lý mô hình, không phải để làm "cầu nối" cho dữ liệu request hàng ngày.

2. Luồng MLflow "Bắt tay" với API (Model Loading)
   MLflow chỉ xuất hiện ở bước khởi tạo hoặc cập nhật mô hình:

Khi FastAPI khởi động: Nó kết nối tới MLflow để tải mô hình.

Khi mô hình được nâng cấp: Nếu bạn chuyển một mô hình từ Staging lên Production trên giao diện MLflow, FastAPI sẽ nhận biết được sự thay đổi đó (thông qua model_uri) và cập nhật mô hình mới vào RAM.

--- ci.yaml cd.yaml
Trong thế giới MLOps và phát triển phần mềm, CI và CD là hai thành phần cốt lõi của quy trình tự động hóa. Khi bạn thấy các file ci.yaml và cd.yaml, đó chính là "bản kế hoạch" (pipeline script) mà bạn cung cấp cho hệ thống (như GitHub Actions, GitLab CI, hay Jenkins) để chúng tự động thực hiện các công việc lặp đi lặp lại.

1. CI (Continuous Integration - Tích hợp liên tục)
   File ci.yaml chứa các bước để đảm bảo code mới viết ra không làm hỏng hệ thống.

Mục tiêu: Kiểm tra lỗi, đảm bảo code sạch và chạy đúng.

Các công việc thường thấy trong file:

Linting: Kiểm tra định dạng code (có đúng chuẩn PEP8 không?).

Unit Testing: Chạy pytest để kiểm tra các hàm trong api/services/predictor.py hoặc các logic của mô hình.

Schema Validation: Kiểm tra xem claim_schema.py có khớp với dữ liệu đầu vào không.

Security Scan: Kiểm tra các lỗ hổng bảo mật trong thư viện.

Khi nào chạy: Mỗi khi bạn "push" code lên nhánh main hoặc tạo "Pull Request".

2. CD (Continuous Deployment/Delivery - Triển khai liên tục)
   File cd.yaml chứa các bước để đưa sản phẩm lên môi trường thực tế (Production) một cách tự động.

Mục tiêu: Chuyển code đã kiểm duyệt thành sản phẩm phục vụ người dùng mà không cần can thiệp thủ công.

Các công việc thường thấy trong file:

Docker Build: Xây dựng image từ Dockerfile.api.

Push Image: Đẩy image lên kho lưu trữ (như Docker Hub, AWS ECR).

Deployment: Cập nhật container trên server (ví dụ: SSH vào server để chạy docker-compose pull và up).

Model Transition: Tự động chuyển trạng thái mô hình trên MLflow từ Staging sang Production nếu tất cả các bài kiểm tra đều đạt yêu cầu.

Khi nào chạy: Chỉ khi file ci.yaml đã chạy thành công và code đã được merge vào nhánh chính.
