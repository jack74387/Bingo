#!/usr/bin/env python3
"""
賓果遊戲伺服器啟動腳本
ZMQ Bingo Game Server Launcher

簡化的伺服器啟動介面，提供預設配置和互動式設定
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
    server = bingo_module.server
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
    print("=== 賓果遊戲伺服器設定 ===")
    print()
    
    # 載入預設配置
    config = load_config()
    server_config = config.get('server', {})
    
    # 網路介面設定
    default_interface = server_config.get('default_interface', 'localhost')
    interface = input(f"請輸入伺服器監聽介面 (預設: {default_interface}): ").strip()
    if not interface:
        interface = default_interface
    
    # 埠號設定
    default_port = server_config.get('default_port', 1060)
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
    
    return interface, port

def main():
    parser = argparse.ArgumentParser(
        description='賓果遊戲伺服器啟動工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python run_server.py                     # 互動式設定
  python run_server.py localhost           # 指定介面，使用預設埠號
  python run_server.py localhost -p 8080   # 指定介面和埠號
  python run_server.py -i                  # 強制互動式設定
        """
    )
    
    parser.add_argument('interface', nargs='?', 
                       help='伺服器監聽的網路介面 (例如: localhost, 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int, metavar='PORT',
                       help='伺服器監聽的埠號 (預設: 1060)')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='使用互動式設定模式')
    parser.add_argument('-c', '--config', metavar='FILE',
                       help='指定配置檔案路徑')
    
    args = parser.parse_args()
    
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
    
    server_config = config.get('server', {})
    
    # 決定使用的參數
    if args.interactive or (not args.interface and not args.port):
        interface, port = interactive_setup()
    else:
        interface = args.interface or server_config.get('default_interface', 'localhost')
        port = args.port or server_config.get('default_port', 1060)
    
    print()
    print("=== 啟動賓果遊戲伺服器 ===")
    print(f"監聽介面: {interface}")
    print(f"監聽埠號: {port}")
    print(f"REQ-REP 埠號: {port}")
    print(f"PUB-SUB 埠號: {port + 1}")
    print()
    print("按 Ctrl+C 停止伺服器")
    print("=" * 40)
    print()
    
    try:
        # 啟動伺服器
        server(interface, port)
    except KeyboardInterrupt:
        print("\n伺服器已停止")
    except Exception as e:
        print(f"伺服器錯誤: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()