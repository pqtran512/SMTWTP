# SMTWTP - Bài toán lập lịch với tổng trọng số thời gian trễ

## Giới thiệu bài toán
SMTWTP (Single Machine Total Weighted Tardiness Problem) là bài toán lập lịch cho một máy đơn với mục tiêu tối thiểu hóa tổng trọng số thời gian trễ. Trong bài toán này:- Có n công việc cần được xử lý trên một máy
- Mỗi công việc j có:  
    - Thời gian xử lý pj
    - Hạn chót dj  
    - Trọng số wj
- Mục tiêu: Tìm thứ tự xử lý các công việc để tối thiểu hóa tổng trọng số thời gian trễ

## Cấu trúc dự án
### File chính
- `aco.py`: Cài đặt thuật toán Ant Colony Optimization (ACO)
- `local_search.py`: Cài đặt thuật toán tìm kiếm cục bộ
- `simulated_annealing.py`: Cài đặt thuật toán Simulated Annealing
- `utils.py`: Các hàm tiện ích, bao gồm hàm tính tổng trọng số thời gian trễ và hàm tính heuristic
- `data.py`: Dữ liệu đầu vào của bài toán
### File kiểm thử và phân tích
- `test_algorithm.py`: So sánh hiệu suất giữa các thuật toán (ACO, ACO + LS, ACO + SA)
- `test_param.py`: Thử nghiệm các tham số khác nhau của thuật toán ACO
- `plot_convergence.py`: Vẽ đồ thị hội tụ của các thuật toán
- `plot_heatmap.py`: Vẽ bản đồ nhiệt để phân tích ảnh hưởng của các tham số

## Hướng dẫn sử dụng
### Cài đặt```bash
pip install numpy matplotlib seaborn pandas tqdm```
### Chạy thuật toán
```bashpython main.py
```
### Thử nghiệm và so sánh các thuật toán```bash
python test_algorithm.py```
Kết quả sẽ được lưu trong thư mục `results/test_algorithm.csv` và `results/test_summary.csv`
### Thử nghiệm các tham số```bash
python test_param.py```
Kết quả sẽ được lưu trong thư mục `results/test_param.csv` và các file hội tụ trong `results/convergence/`
### Vẽ đồ thị hội tụ```bash
python plot_convergence.py```
Đồ thị sẽ được lưu trong thư mục `results/plots/`
### Vẽ bản đồ nhiệt```bash
python plot_heatmap.py```
Bản đồ nhiệt sẽ được lưu trong thư mục `results/heatmaps/`

## Kết quả thử nghiệm
Dựa trên kết quả thử nghiệm, thuật toán ACO kết hợp với tìm kiếm cục bộ (ACO + LS) cho kết quả tốt nhất với TWT = 102353, nhưng tốn thời gian chạy nhiều nhất (trung bình 17.91s). Thuật toán ACO kết hợp với mô phỏng luyện kim (ACO + SA) cũng cho kết quả tốt (TWT = 102978) với thời gian chạy trung bình là 8.83s.
Các tham số tối ưu cho thuật toán ACO:
- Số kiến (m): 50
- Số vòng lặp (T): 50
- Hệ số khai thác (q0): 0.9
- Hệ số beta: 3




































# SMTWTP
