#!/usr/bin/env python3
"""
賓果遊戲客戶端啟動腳本
ZMQ Bingo Game Client Launcher

簡化的客戶端啟動介面，提供預設配置和互動式設定
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加主程式到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from importlib import import_module
    # 動態導入主程式模組
    bingo_module = import_module('zmq_bingo')
    client = bingo_module.client
except ImportError as e:
    print(f"錯誤：無法載入主程式模組 - {e}")
    sys.exit(1)

def load_config():
    """載入配置檔案"""
    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"警告：配置檔案格式錯誤 - {e}")
            return {}
    return {}

def interactive_setup():
    """互動式設定"""
    print("=== 賓果遊戲客戶端設定 ===")
    print()
    
    # 載入預設配置
    config = load_config()
    client_config = config.get('client', {})
    
    # 伺服器地址設定
    default_server = client_config.get('default_server', 'localhost')
    server = input(f"請輸入伺服器地址 (預設: {default_server}): ").strip()
    if not server:
        server = default_server
    
    # 埠號設定
    default_port = client_config.get('default_port', 1060)
    while True:
        port_input = input(f"請輸入伺服器埠號 (預設: {default_port}): ").strip()
        if not port_input:
            port = default_port
            break
        try:
            port = int(port_input)
            if 1 <= port <= 65535:
                break
            else:
                print("埠號必須在 1-65535 範圍內")
        except ValueError:
            print("請輸入有效的數字")
    
    return server, port

def show_game_instructions():
    """顯示遊戲說明"""
    print()
    print("=== 賓果遊戲說明 ===")
    print("1. 輸入您的姓名，然後輸入25個不重複的數字 (1-25)")
    print("2. 格式：姓名,數字1,數字2,...,數字25")
    print("3. 範例：Alice,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25")
    print("4. 等待遊戲開始，標記抽中的數字")
    print("5. 當您達成賓果時，遊戲會自動檢測並宣布")
    print()
    print("勝利條件：達成5條線 (橫線、豎線、對角線)")
    print("=" * 50)

def validate_bingo_input(bingo_input):
    """驗證賓果輸入格式"""
    parts = bingo_input.split(',')
    if len(parts) != 26:
        return False, "必須輸入姓名 + 25個數字"
    
    name = parts[0].strip()
    if not name:
        return False, "姓名不能為空"
    
    try:
        numbers = [int(x.strip()) for x in parts[1:]]
    except ValueError:
        return False, "所有數字必須是整數"
    
    if len(set(numbers)) != 25:
        return False, "25個數字必須都不相同"
    
    if not all(1 <= n <= 25 for n in numbers):
        return False, "所有數字必須在 1-25 範圍內"
    
    return True, "格式正確"

def interactive_bingo_setup():
    """互動式賓果卡設定"""
    print("=== 設定您的賓果卡 ===")
    print()
    
    while True:
        name = input("請輸入您的姓名: ").strip()
        if name:
            break
        print("姓名不能為空，請重新輸入")
    
    print()
    print("現在請設定您的賓果卡數字 (1-25，不重複):")
    print("您可以選擇以下方式之一：")
    print("1. 手動輸入25個數字 (用逗號分隔)")
    print("2. 使用隨機生成")
    
    while True:
        choice = input("請選擇 (1/2): ").strip()
        if choice in ['1', '2']:
            break
        print("請輸入 1 或 2")
    
    if choice == '1':
        # 手動輸入
        while True:
            print(f"\n請輸入25個數字 (1-25，用逗號分隔):")
            numbers_input = input("數字: ").strip()
            
            try:
                numbers = [int(x.strip()) for x in numbers_input.split(',')]
                if len(numbers) != 25:
                    print(f"需要輸入25個數字，您輸入了{len(numbers)}個")
                    continue
                
                if len(set(numbers)) != 25:
                    print("數字不能重複")
                    continue
                
                if not all(1 <= n <= 25 for n in numbers):
                    print("所有數字必須在 1-25 範圍內")
                    continue
                
                break
            except ValueError:
                print("請輸入有效的數字，用逗號分隔")
    
    else:
        # 隨機生成
        import random
        numbers = list(range(1, 26))
        random.shuffle(numbers)
        print(f"隨機生成的數字: {','.join(map(str, numbers))}")
    
    # 組合最終輸入
    bingo_input = f"{name},{','.join(map(str, numbers))}"
    
    # 顯示賓果卡預覽
    print(f"\n您的賓果卡：")
    print(f"玩家：{name}")
    for i in range(5):
        row = numbers[i*5:(i+1)*5]
        print(' '.join(f'{n:2d}' for n in row))
    
    return bingo_input

def main():
    parser = argparse.ArgumentParser(
        description='賓果遊戲客戶端啟動工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python run_client.py                      # 互動式設定
  python run_client.py localhost            # 連接到 localhost，使用預設埠號
  python run_client.py 192.168.1.100 -p 8080  # 指定伺服器和埠號
  python run_client.py -i                   # 強制互動式設定
        """
    )
    
    parser.add_argument('server', nargs='?',
                       help='伺服器地址 (例如: localhost, 192.168.1.100)')
    parser.add_argument('-p', '--port', type=int, metavar='PORT',
                       help='伺服器埠號 (預設: 1060)')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='使用互動式設定模式')
    parser.add_argument('-c', '--config', metavar='FILE',
                       help='指定配置檔案路徑')
    parser.add_argument('--help-game', action='store_true',
                       help='顯示遊戲規則說明')
    
    args = parser.parse_args()
    
    if args.help_game:
        show_game_instructions()
        return
    
    # 載入配置
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"錯誤：無法載入配置檔案 {args.config} - {e}")
            sys.exit(1)
    else:
        config = load_config()
    
    client_config = config.get('client', {})
    
    # 決定使用的參數
    if args.interactive or (not args.server and not args.port):
        server_addr, port = interactive_setup()
    else:
        server_addr = args.server or client_config.get('default_server', 'localhost')
        port = args.port or client_config.get('default_port', 1060)
    
    show_game_instructions()
    
    print()
    print("=== 連接到賓果遊戲伺服器 ===")
    print(f"伺服器地址: {server_addr}")
    print(f"連接埠號: {port}")
    print()
    print("按 Ctrl+C 退出遊戲")
    print("=" * 40)
    
    try:
        # 啟動客戶端
        client(server_addr, port)
    except KeyboardInterrupt:
        print("\n已退出遊戲")
    except Exception as e:
        print(f"客戶端錯誤: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()