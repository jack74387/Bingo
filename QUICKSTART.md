# 快速入門指南 (Quick Start Guide)

## 🚀 立即開始遊戲

### 方法一：使用批次檔案 (Windows)
```bash
# 雙擊執行 start_game.bat 或在命令提示字元中執行：
start_game.bat
```

### 方法二：使用 Python 腳本

#### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

#### 2. 啟動伺服器
```bash
# 互動式設定
python run_server.py

# 或直接指定參數
python run_server.py localhost -p 1060
```

#### 3. 啟動客戶端（新終端）
```bash
# 互動式設定
python run_client.py

# 或直接指定參數
python run_client.py localhost -p 1060
```

### 方法三：使用原始檔案
```bash
# 啟動伺服器
python zmq_bingo.py server localhost -p 1060

# 啟動客戶端
python zmq_bingo.py client localhost -p 1060
```

## 🎮 遊戲操作流程

1. **啟動伺服器**：選擇一個終端作為伺服器
2. **連接客戶端**：在其他終端啟動客戶端
3. **輸入賓果卡**：格式為 `姓名,數字1,數字2,...,數字25`
   ```
   範例：Alice,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25
   ```
4. **等待遊戲開始**：當所有玩家準備好或超時後，遊戲自動開始
5. **標記數字**：伺服器會廣播隨機數字，客戶端自動標記
6. **宣布勝利**：達成賓果時，遊戲會自動檢測並宣布獲勝者

## 🔧 系統檢測

執行系統測試來確保環境正確：
```bash
python test_system.py
```

## 📁 檔案說明

| 檔案 | 用途 |
|------|------|
| `zmq_bingo.py` | 主程式檔案 |
| `run_server.py` | 伺服器啟動腳本 |
| `run_client.py` | 客戶端啟動腳本 |
| `start_game.bat` | Windows 批次啟動檔案 |
| `test_system.py` | 系統測試腳本 |
| `config.json` | 主要配置檔案 |
| `config_dev.json` | 開發/測試配置檔案 |
| `requirements.txt` | Python 依賴列表 |

## 🛠️ 常見問題

**Q: 埠號被占用怎麼辦？**
A: 更改埠號參數，例如：`-p 8080`

**Q: 無法連接到伺服器？**
A: 檢查伺服器IP地址和埠號是否正確

**Q: 輸入格式錯誤？**
A: 確保格式為：`姓名,25個不重複的1-25數字`

**Q: 想要更快的遊戲節奏？**
A: 使用 `config_dev.json` 配置檔案（等待時間更短）

## 🎯 進階設定

### 使用自定義配置
```bash
python run_server.py -c config_dev.json
python run_client.py -c config_dev.json
```

### 網路遊戲設定
```bash
# 伺服器（允許外部連接）
python run_server.py 0.0.0.0 -p 1060

# 客戶端（連接到遠端伺服器）
python run_client.py 192.168.1.100 -p 1060
```

---
**享受遊戲樂趣！** 🎉