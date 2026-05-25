Hệ thống Pipeline MLOps hoàn chỉnh (End-to-End MLOps Pipeline) cho lĩnh vực chăm sóc sức khỏe.

1. Phân tích kiến trúc (The "Why" behind the code)
   Decoupling (Tách biệt logic):

config.py: Đóng vai trò là "bản thiết kế" (blueprint). Mọi tham số từ danh sách cột đến ngưỡng kích hoạt đều nằm tập trung ở đây. Khi cần đổi mô hình, bạn chỉ cần sửa config mà không động vào logic code.

utils.py: Đóng vai trò là "xương sống" hệ thống (IO, Logging, Schema validation). Nó đảm bảo dữ liệu chạy vào và ra luôn đúng format.

train.py & evaluate.py: Chứa logic nghiệp vụ cốt lõi (Machine Learning).

Production Readiness (Tính sẵn sàng cho sản xuất):

Bạn sử dụng Time-based split thay vì train_test_split ngẫu nhiên. Điều này chứng tỏ bạn hiểu rõ "Data Leakage" là kẻ thù số 1 trong dự báo y tế.

Việc Log Prediction với input_hash và timestamp giúp bạn thực hiện bài toán Auditability (Kiểm tra lại xem mô hình đã dự báo gì cho ca bệnh X vào ngày Y).

2. Luồng chạy của training_pipeline.py (The Orchestra)
   Đây là trái tim của hệ thống. Nó thực hiện quy trình "Automation-to-Promotion":

Orchestration: Nhận lệnh qua argparse (--model risk hoặc --model claim).

Training: Tự động xây dựng Pipeline từ MODEL_CONFIG (tiền xử lý + mô hình).

MLflow Integration: Không chỉ log metrics, mà log cả Pipeline object. Điều này quan trọng vì khi bạn load lại mô hình từ Production, bạn không cần thực hiện preprocessing thủ công nữa, mô hình tự xử lý dữ liệu đầu vào.

Model Registry & Promotion (Giai đoạn quyết định):

Tự động đưa mô hình vào Staging.

Kiểm tra điều kiện is_eligible_for_production (Accuracy > 55% và Recall > 70%).

Nếu đạt, tự động Promote lên Production và hạ cấp các phiên bản cũ (archive_existing_versions=True).

3. Tại sao cấu trúc này là "Gold Standard"?
   Dễ mở rộng: Nếu sau này bệnh viện thêm 1 bài toán mới (ví dụ: dự báo thời gian tái nhập viện), bạn chỉ cần thêm một key re-admission vào MODEL_CONFIG mà không cần viết lại toàn bộ khung code.

Reproducibility (Tính tái lập): Với mlflow.db và các file joblib, bạn hoàn toàn có thể tái tạo lại bất kỳ model nào đã từng được training.

Traceability: Việc lưu predictions.log giúp bạn xây dựng được "Feedback Loop" — sau này khi có kết quả thực tế, bạn so sánh với prediction trong file log để tính toán Drift (độ lệch của mô hình theo thời gian).

--
Tóm tắt Workflow bằng sơ đồ tư duy:
Input: Dữ liệu (model_table.csv) + Cấu hình (MODEL_CONFIG).

Process: Chia dữ liệu theo thời gian → Tiền xử lý → Huấn luyện → Đánh giá.

Governance (MLflow): Log tất cả → Đăng ký mô hình (Registry) → Kiểm tra ngưỡng (Promotion).

Output: Mô hình sẵn sàng phục vụ + File log dự đoán.

# Config

1. Khối định danh (Identification)
   run_name: Tên hiển thị trên MLflow UI để bạn dễ dàng tìm lại thí nghiệm này giữa hàng trăm thí nghiệm khác.

registered_model_name: Tên chính thức khi mô hình được đưa vào "Model Registry" (kho lưu trữ mô hình cấp Production).

2. Khối định nghĩa dữ liệu (Core Columns)
   target_column: Cột mục tiêu cần dự báo (ví dụ: risk_score hoặc claim_status).

sort_column: Cột thời gian dùng để thực hiện Time-based split (chia tập dữ liệu theo thời gian thực tế, tránh rò rỉ thông tin tương lai).

positive_label_for_recall: Đây là nhãn quan trọng nhất cần tối ưu (ví dụ: mô hình claim cần tập trung vào việc dự báo đúng các ca Rejected).

3. Khối quản lý Đặc trưng (Feature Management)
   input_features: Danh sách tất cả cột đầu vào.

numeric_features & categorical_features: Đây là phần cực kỳ quan trọng. Hệ thống của bạn dùng cấu trúc này để tự động "ép kiểu" dữ liệu:

numeric: Dùng SimpleImputer(strategy="median") để xử lý giá trị thiếu.

categorical: Dùng OneHotEncoder để chuyển chữ thành số cho máy tính hiểu.

Việc tách riêng này giúp code get_preprocessor() trong file train.py của bạn trở nên cực kỳ tinh gọn và linh hoạt.

4. Khối kiểm soát chất lượng (Promotion Thresholds)
   promotion_accuracy_threshold & promotion_recall_threshold: Đây là bộ lọc "cửa ải". Chỉ khi mô hình vượt qua các ngưỡng này, hệ thống mới tự động chuyển nó từ trạng thái Staging lên Production.

5. Khối cấu hình mô hình (Model Hyperparameters)
   params: Chứa các tham số cấu hình cho RandomForest.

## class_weight: "balanced_subsample": Đây là kỹ thuật giúp mô hình không bị "thiên vị" khi một nhóm dữ liệu có quá ít mẫu so với nhóm kia (rất quan trọng trong y tế khi các ca bệnh hiếm thường ít hơn ca bình thường).

# evaluate

Đoạn mã này đóng vai trò là "Hệ thống kiểm soát chất lượng" (Quality Gate) trong Pipeline MLOps của bạn. Nó không chỉ đơn thuần tính toán các con số, mà còn đưa ra quyết định kỹ thuật dựa trên các chỉ số đó.

Dưới đây là ý nghĩa chi tiết của từng thành phần:

1. Hàm evaluate_model: "Bộ đo lường hiệu năng"
   Hàm này tập trung vào việc trích xuất các chỉ số quan trọng nhất cho bài toán y tế của bạn:

accuracy_score: Cho biết độ chính xác tổng thể. Tuy nhiên, trong y tế, độ chính xác không phải là tất cả (ví dụ: nếu 99% ca là Paid, mô hình đoán bừa 100% Paid vẫn có accuracy 99% nhưng hoàn toàn vô dụng).

weighted_f1: Đây là chỉ số quan trọng để đánh giá sự cân bằng giữa Precision (Độ chính xác khi dự báo đúng) và Recall (Khả năng bao quát các trường hợp).

target_recall: Đây là "trái tim" của hàm. Bằng cách dùng labels=[positive_label], bạn ép mô hình tập trung vào việc "không bỏ sót" những ca quan trọng nhất (như High rủi ro hoặc Rejected hồ sơ).

-

2. Hàm is_eligible_for_production: "Bộ lọc triển khai"
   Đây là logic cốt lõi để tự động hóa MLOps. Thay vì con người phải xem kết quả rồi quyết định "có nên đưa model này lên server không", hàm này làm việc đó dựa trên ngưỡng (thresholds):

Tính khách quan: Nó loại bỏ yếu tố cảm tính của lập trình viên.

Tính an toàn: Chỉ khi cả hai điều kiện (accuracy và target_recall đều đạt) thỏa mãn, hệ thống mới cho phép mô hình tiếp cận dữ liệu thực tế.

Tại sao đây là tư duy "Senior Engineer"?
Trong các hệ thống thực tế, bạn không bao giờ muốn triển khai một mô hình "mù quáng". Việc đóng gói logic kiểm định vào các hàm chuyên biệt giúp bạn:

Dễ dàng thay đổi ngưỡng: Nếu bộ phận Y tế muốn thắt chặt kiểm soát hơn, bạn chỉ cần thay đổi recall_threshold trong file cấu hình (CONFIG) mà không cần can thiệp vào logic tính toán.

## Khả năng Audit (Kiểm toán): Bạn có thể dễ dàng log các giá trị này vào MLflow để đối chiếu sau này.

# train

Đoạn code bạn vừa cung cấp chính là "trái tim" kỹ thuật của hệ thống. Bạn đang sử dụng sklearn.pipeline.Pipeline để kết hợp hai nhiệm vụ tách biệt: Xử lý dữ liệu (Preprocessing) và Dự báo (Modeling) thành một thực thể duy nhất.

Đây là cách bạn đang tối ưu hóa hệ thống của mình:

1. Tại sao dùng ColumnTransformer lại quan trọng?
   Trong dữ liệu y tế, bạn có các kiểu dữ liệu khác nhau (ví dụ: age là số, city là phân loại). Nếu xử lý thủ công, bạn sẽ rất dễ gặp lỗi khi test data có giá trị mà train data không có.

numeric_transformer: Dùng SimpleImputer(strategy="median") để lấp đầy các ô trống bằng giá trị trung vị. Đây là cách làm an toàn, giảm thiểu tác động của các giá trị ngoại lai (outliers) so với dùng mean.

categorical_transformer: Dùng OneHotEncoder(handle_unknown="ignore"). Điểm sáng ở đây là tham số handle_unknown="ignore". Nếu sau này bạn có một city mới xuất hiện (ví dụ: "HCMC"), mô hình sẽ không bị crash mà chỉ đơn giản coi đó là một hàng toàn số 0, giữ cho hệ thống chạy ổn định.

2. Sự "Gắn kết" trong Pipeline
   Khi bạn định nghĩa:

Python

pipeline = Pipeline(steps=[
("preprocessor", preprocessor),
("model", model)
])
Bạn đã tạo ra một "đường ống" khép kín. Khi gọi pipeline.predict(X_test), hệ thống sẽ tự động:

Đẩy X_test qua preprocessor để làm sạch và mã hóa.

Sau đó chuyển kết quả đã làm sạch trực tiếp sang model để dự báo.

3. Ưu điểm của tư duy này (The Hybrid Engineer Mindset)
   Chống rò rỉ dữ liệu (Data Leakage): Khi bạn fit pipeline, toàn bộ quy trình tiền xử lý được khớp (fitted) trên tập Train. Khi bạn predict trên tập Test, nó sử dụng chính cái "bộ lọc" đó mà không hề "nhìn thấy" dữ liệu mới. Đây là cách chuẩn nhất để đánh giá hiệu năng thực tế.

## Đóng gói (Encapsulation): Bạn có thể lưu toàn bộ biến pipeline này lại bằng joblib. Khi triển khai lên server, bạn không cần phải viết lại code tiền xử lý, chỉ cần load file đã lưu và gọi .predict() là xong.

# utils

File utils.py này đóng vai trò là "bộ khung quản trị" (Utility Layer) cho toàn bộ hệ thống. Trong kiến trúc MLOps, các file tiện ích như thế này rất quan trọng để đảm bảo tính đồng nhất (consistency) giữa môi trường huấn luyện và môi trường dự báo thực tế.

Dưới đây là phân tích về cách các chức năng này hỗ trợ cho quy trình của bạn:

1. Quản lý dữ liệu & File (IO Management)
   get_base_dir() & load_model_table(): Các hàm này giúp hệ thống của bạn không bị phụ thuộc vào vị trí hiện tại của người dùng. Dù bạn chạy code từ bất kỳ đâu, nó đều tự động tìm đúng đường dẫn gốc của dự án. Đây là kỹ thuật giúp code có thể chạy được trên cả máy cá nhân lẫn trên Server (CI/CD).

time_based_split(): Đây là "chốt chặn" quan trọng. Bằng cách ép dữ liệu phải sort theo sort_column trước khi chia, bạn đảm bảo mô hình luôn được kiểm chứng trên dữ liệu tương lai (out-of-time validation).

2. Định nghĩa Hợp đồng dữ liệu (Contract Management)
   save_feature_schema_full(): Đây là hàm rất thông minh. Nó lưu lại cấu trúc của mô hình vào file .json.

Tại sao cần? Khi bạn chuyển mô hình sang API hoặc Service, dịch vụ đó cần biết chính xác mô hình mong đợi những cột nào (input_features) và thứ tự ra sao. File JSON này chính là "bản thỏa thuận" giữa đội Data Science và đội Backend/Deployment.

3. Khả năng truy vết & Vận hành (Traceability & Observability)
   hash_input(): Hàm này dùng để tạo một "dấu vân tay" (SHA-256) cho dữ liệu đầu vào.

Ứng dụng: Khi bạn cần kiểm tra lại một dự báo trong quá khứ, bạn không cần lưu toàn bộ nội dung input (vốn có thể rất lớn), bạn chỉ cần lưu input_hash để đối chiếu xem dữ liệu đầu vào có bị thay đổi hay không.

write_prediction_log(): Đây là nhật ký hoạt động. Nó lưu lại vết của mọi dự báo. Trong y tế, việc có thể truy xuất ngược lại "Mô hình đã dự báo gì cho bệnh nhân này vào ngày X" là một yêu cầu bắt buộc về tính minh bạch (Auditability).

Một số lưu ý để code bền vững hơn (Production-Grade):
Về time_based_split: Hàm này hiện đang reset_index(drop=True). Trong một số trường hợp, bạn có thể muốn giữ lại index gốc để đối soát (mapping lại với PatientID). Bạn hãy cân nhắc nếu cần truy vấn ngược lại dữ liệu gốc.

Về hash_input: Bạn đang dùng default=str trong json.dumps. Điều này rất hay vì nó giúp xử lý được các kiểu dữ liệu phức tạp (như datetime, numpy types) mà không bị lỗi.

Về write_prediction_log: Việc ghi vào một file .log là tốt, nhưng nếu hệ thống của bạn chạy với hàng chục nghìn lượt dự báo mỗi giây, hãy cân nhắc sử dụng các thư viện như logging hoặc đổ log trực tiếp vào một database (như SQLite hoặc PostgreSQL) để dễ dàng truy vấn hơn là đọc file text.

1. Quản lý đường dẫn thông minh (Path Resilience)
   get_base_dir(): Hàm này cực kỳ quan trọng. Nó tự tìm đến thư mục gốc của dự án.

Tác dụng: Dù bạn chạy code từ terminal, từ Jupyter Notebook, hay đưa lên server chạy tự động, nó luôn tìm thấy folder outputs, models, logs chính xác. Bạn sẽ không bao giờ bị lỗi "file not found" vì sai đường dẫn tương đối nữa.

2. Tiền xử lý và Đóng gói (Data Preparation & Contract)
   time_based_split(): Đây là "xương sống" của mô hình y tế. Thay vì chia ngẫu nhiên (dễ gây gian lận dữ liệu), nó bắt buộc dữ liệu phải được sắp xếp theo thời gian. 80% dữ liệu cũ là để học, 20% dữ liệu mới là để thi.

save_feature_schema_full(): Nó tạo ra một "Bản hợp đồng" giữa mô hình và thế giới bên ngoài. Nó lưu lại danh sách cột, cột nào là target, cột nào là thời gian. Khi bạn xây dựng ứng dụng Web để bác sĩ dùng, ứng dụng đó sẽ đọc file JSON này để biết: "À, mô hình cần chính xác 14 cột này".

3. Lưu trữ và Khôi phục mô hình (Serialization)
   save_local_model() & load_local_model(): Sử dụng thư viện joblib để nén toàn bộ Pipeline (bao gồm các bước xử lý số liệu + mô hình Random Forest) thành một file duy nhất.

Tác dụng: Giúp việc mang mô hình từ máy tính cá nhân lên server Production trở nên dễ dàng như copy một file.

4. Hệ thống theo dõi vết (Audit & Monitoring)
   Đây là phần giúp hệ thống của bạn chuyên nghiệp hơn 90% dự án AI thông thường:

hash_input(): Khi có một yêu cầu dự báo gửi đến (input), hàm này tạo ra một "mã dấu vân tay" (SHA-256).

write_prediction_log(): Ghi lại lịch sử: "Vào giờ này, mô hình phiên bản X, với dữ liệu (dấu vân tay Y) đã dự báo kết quả Z".

Tác dụng: Nếu sau này bác sĩ hỏi: "Tại sao mô hình lại từ chối ca bệnh này của tôi?", bạn có thể tra cứu log, tìm lại đúng lần dự báo đó, và biết được dữ liệu đầu vào là gì.

Tóm tắt luồng công việc qua utils.py
Để dễ hiểu, bạn hãy tưởng tượng utils.py giống như một thủ kho:

Nó biết nơi cất giữ đồ đạc (get_base_dir).

Nó kiểm tra hàng hóa trước khi nhập (time_based_split).

Nó đóng gói sản phẩm cẩn thận (save_local_model).

Nó ghi chép lại mọi lần xuất hàng để đối soát sau này (write_prediction_log).

---

# training_pipeline

Đây là tệp tin training_pipeline.py, "trái tim" điều phối toàn bộ hệ thống MLOps của bạn. Nó đóng vai trò là một Orchestrator (người điều phối), kết nối tất cả các thành phần mà bạn đã xây dựng (config, utils, train, evaluate) vào một chuỗi quy trình tự động.

Để bạn hiểu rõ quy trình vận hành của nó, tôi sẽ chia luồng này thành các giai đoạn chính:

1. Khởi tạo và Thiết lập (Giai đoạn chuẩn bị)
   MLflow Tracking: Code kết nối tới 127.0.0.1:5000 (nơi MLflow Server của bạn đang chạy). Nó thiết lập một Experiment là healthcare-classification để gom tất cả các phiên bản huấn luyện lại một chỗ.

Argparse: Cho phép bạn linh hoạt huấn luyện mô hình khác nhau (risk hoặc claim) chỉ bằng tham số --model.

2. Chu trình Huấn luyện (Data-to-Model)
   Từ Step 1 đến Step 7, pipeline thực hiện quy trình chuẩn:

Dữ liệu: Tải dữ liệu từ model_table.csv, chia dữ liệu theo thời gian (time_based_split) để tránh hiện tượng "nhìn thấy tương lai" (data leakage).

Pipeline: Xây dựng một cấu trúc Pipeline của Scikit-learn, bao gồm cả bước tiền xử lý (Imputer, Encoder) và mô hình (RandomForest).

Huấn luyện & Lưu trữ: Mô hình được fit và lưu lại dưới dạng file .joblib để dự phòng.

3. Đăng ký & Kiểm định (MLOps Governance)
   Đây là phần thú vị nhất của file này (từ Step 11 đến Step 14):

Tracking & Logging: Mọi thông số (hyperparameters), chỉ số (metrics) đều được đẩy lên MLflow.

Registry: register_model đưa mô hình vào "thư viện quản lý", giúp bạn biết được mô hình nào là mới nhất, mô hình nào là cũ.

Staging Transition: Tự động đẩy mô hình vừa huấn luyện vào môi trường Staging (môi trường kiểm thử).

Eligibility Check: Dùng hàm is_eligible_for_production để "chấm điểm". Nếu đạt yêu cầu, nó mới cho phép mô hình đi tiếp.

4. Triển khai Production & Audit (Step 15 đến 18)
   Nếu mô hình đạt chất lượng, pipeline sẽ:

Promote: Tự động chuyển trạng thái sang Production và lưu trữ (archive) các phiên bản cũ hơn.

Verification: Thử nghiệm dự báo trên 5 mẫu dữ liệu để đảm bảo mô hình hoạt động đúng.

Traceability: Sử dụng hash_input để ghi lại nhật ký dự báo. Điều này cực kỳ quan trọng trong y tế để truy xuất nguồn gốc mỗi khi có tranh chấp hoặc cần giải thích dự báo của AI.

Tóm tắt luồng công việc của training_pipeline.py
Điểm mạnh của code này:

Tính tự động hóa cao: Từ việc huấn luyện đến việc chuyển mô hình lên Production, không có sự can thiệp thủ công.

Tính minh bạch: Mọi dự báo đều được log lại kèm theo input_hash và model_version.

## Tính linh hoạt: Bạn có thể dễ dàng quản lý nhiều bài toán khác nhau (risk, claim) chỉ với một file pipeline duy nhất.
