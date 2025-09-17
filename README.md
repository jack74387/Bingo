# ZMQ賓果遊戲 (ZMQ Bingo Game)

一個基於ZeroMQ (ZMQ) 實現的多人線上賓果遊戲系統。這個專案展示了如何使用ZMQ的REQ-REP和PUB-SUB模式來建立客戶端-伺服器架構的遊戲。

## 📋 專案描述

這是一個經典的賓果遊戲，玩家可以通過網路連接到遊戲伺服器進行多人遊戲。遊戲使用5×5的賓果卡，玩家需要在自己的卡片上標記服務器隨機抽取的數字，最先連成5條線的玩家獲勝。

### 🎮 遊戲特色

- **多人線上遊戲**：支援多個玩家同時參與
- **即時通訊**：使用ZMQ實現低延遲的網路通訊
- **自定義賓果卡**：玩家可以自己選擇1-25的數字排列
- **即時勝利檢測**：自動檢測賓果線並宣布獲勝者
- **視覺化介面**：終端中彩色顯示已標記的數字

## 🚀 快速開始

### 系統需求

- Python 3.6+
- ZeroMQ library
- Windows/Linux/macOS

### 安裝

1. **複製專案**
   ```bash
   git clone https://github.com/jack74387/Bingo.git
   cd bingo
   ```

2. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

3. **或者手動安裝ZMQ**
   ```bash
   pip install pyzmq
   ```

### 使用方法

#### 啟動遊戲伺服器

```bash
python zmq_bingo.py server <interface> -p <port>
```

**參數說明：**
- `interface`: 伺服器監聽的網路介面 (例如：`localhost` 或 `0.0.0.0`)
- `port`: 伺服器監聽的埠號 (預設: 1060)

**範例：**
```bash
# 在本地啟動伺服器
python zmq_bingo.py server localhost -p 1060

# 在所有網路介面啟動伺服器
python zmq_bingo.py server 0.0.0.0 -p 1060
```

#### 連接為客戶端

```bash
python zmq_bingo.py client <server_address> -p <port>
```

**參數說明：**
- `server_address`: 伺服器的IP地址或主機名
- `port`: 伺服器的埠號

**範例：**
```bash
# 連接到本地伺服器
python zmq_bingo.py client localhost -p 1060

# 連接到遠端伺服器
python zmq_bingo.py client 192.168.1.100 -p 1060
```

## 🎯 遊戲規則

### 賓果卡設置
1. 每個玩家需要輸入自己的名字
2. 選擇25個不重複的數字 (1-25)
3. 這些數字會排列成5×5的賓果卡

### 遊戲流程
1. **等待階段**：玩家加入遊戲後，等待其他玩家或超時開始
2. **遊戲開始**：伺服器隨機抽取1-25的數字
3. **標記數字**：玩家在自己的卡片上標記相符的數字
4. **宣布勝利**：當玩家達成賓果條件時可以宣布勝利
5. **驗證勝利**：伺服器驗證勝利條件並宣布獲勝者

### 勝利條件
達成以下任一條件即可宣布賓果：
- **橫線**：任意一行的5個數字都被標記
- **豎線**：任意一列的5個數字都被標記  
- **對角線**：主對角線或副對角線的5個數字都被標記

**注意**：需要至少達成5條線才能獲勝！

## 🛠️ 技術架構

### 網路通訊模式

1. **REQ-REP模式**：
   - 客戶端請求加入遊戲
   - 客戶端宣布賓果
   - 伺服器回應狀態訊息

2. **PUB-SUB模式**：
   - 伺服器廣播遊戲開始訊息
   - 伺服器廣播抽取的數字
   - 伺服器廣播遊戲結果

### 埠號使用
- **主埠號**：REQ-REP通訊
- **主埠號+1**：PUB-SUB通訊

### 核心演算法

#### 賓果檢測演算法
```python
def checkBingo(clientList, currentList):
    # 檢查橫線、豎線、對角線
    # 返回True如果達成≥5條線
```

## 📁 專案結構

```
bingo/
├── zmq_bingo.py    # 主程式
├── README.md                 # 專案說明
├── requirements.txt          # 依賴列表
├── config.json              # 配置檔案範例
├── run_server.py            # 伺服器啟動腳本
├── run_client.py            # 客戶端啟動腳本
├── setup.py                 # 安裝腳本
├── pyproject.toml           # 專案配置
├── LICENSE                  # 授權檔案
└── .gitignore              # Git忽略檔案
```

## 🎮 使用範例

### 完整遊戲流程範例

1. **啟動伺服器**
   ```bash
   python zmq_bingo.py server localhost -p 1060
   ```
   輸出：`Server start ...`

2. **玩家1加入**
   ```bash
   python zmq_bingo.py client localhost -p 1060
   ```
   輸入：`Alice,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25`

3. **玩家2加入**
   ```bash
   python zmq_bingo.py client localhost -p 1060
   ```
   輸入：`Bob,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1`

4. **遊戲自動開始**，伺服器開始廣播隨機數字

5. **玩家達成賓果**時輸入賓果指令，伺服器驗證並宣布獲勝者

**享受賓果遊戲的樂趣！** 🎉