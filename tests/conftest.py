import pytest
import os
import json
from pathlib import Path

@pytest.fixture(scope="session", autouse=True)
def create_mock_baseline():
    """Tự động tạo file baseline giả cho các bài test monitoring."""
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    baseline_file = output_dir / "feature_baseline.json"
    
    # Tạo nội dung giả lập (chỉ cần cấu trúc đơn giản để code không bị lỗi)
    mock_data = {
        "age": {"mean": 50, "std": 10},
        "billed_amount": {"mean": 50000, "std": 5000}
    }
    
    with open(baseline_file, "w") as f:
        json.dump(mock_data, f)
    
    yield  # Test sẽ chạy ở đây
    
    # Dọn dẹp sau khi chạy test xong
    if baseline_file.exists():
        os.remove(baseline_file)