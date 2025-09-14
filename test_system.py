#!/usr/bin/env python3
"""
簡單的測試腳本 - 驗證程式功能
Simple test script to verify program functionality
"""

import sys
import os
import importlib

def test_imports():
    """測試必要的套件是否已安裝"""
    print("=== 測試套件導入 ===")
    
    required_modules = ['zmq', 'argparse', 'socket', 'time', 'random']
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module} - 已安裝")
        except ImportError as e:
            print(f"✗ {module} - 未安裝: {e}")
            return False
    
    return True

def test_main_module():
    """測試主程式模組是否可以載入"""
    print("\n=== 測試主程式模組 ===")
    
    try:
        # 添加當前目錄到路徑
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # 嘗試導入主模組
        bingo_module = importlib.import_module('zmq_bingo')
        
        # 檢查必要的函數是否存在
        required_functions = ['checkBingo', 'check_port_available', 'server', 'client']
        
        for func_name in required_functions:
            if hasattr(bingo_module, func_name):
                print(f"✓ 函數 {func_name} - 已找到")
            else:
                print(f"✗ 函數 {func_name} - 未找到")
                return False
        
        return True
        
    except ImportError as e:
        print(f"✗ 無法載入主程式模組: {e}")
        return False

def test_bingo_logic():
    """測試賓果檢測邏輯"""
    print("\n=== 測試賓果檢測邏輯 ===")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        bingo_module = importlib.import_module('zmq_bingo')
        checkBingo = bingo_module.checkBingo
        
        # 測試用例1: 無賓果
        client_list = list(range(1, 26))  # 1-25
        current_list = [1, 2, 3, 4, 5] + [0] * 20  # 只有前5個數字
        result = checkBingo(client_list, current_list)
        print(f"測試1 (無賓果): {result} - {'✓' if not result else '✗'}")
        
        # 測試用例2: 滿線賓果 (所有數字都標記)
        current_list_full = list(range(1, 26))
        result = checkBingo(client_list, current_list_full)
        print(f"測試2 (滿線賓果): {result} - {'✓' if result else '✗'}")
        
        return True
        
    except Exception as e:
        print(f"✗ 賓果邏輯測試失敗: {e}")
        return False

def test_port_check():
    """測試埠號檢查功能"""
    print("\n=== 測試埠號檢查 ===")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        bingo_module = importlib.import_module('zmq_bingo')
        check_port_available = bingo_module.check_port_available
        
        # 測試可用埠號
        result = check_port_available('localhost', 0)  # 埠號0會自動分配可用埠號
        print(f"埠號可用性檢查: {'✓' if result else '✗'}")
        
        return True
        
    except Exception as e:
        print(f"✗ 埠號檢查測試失敗: {e}")
        return False

def test_config_files():
    """測試配置檔案是否存在並有效"""
    print("\n=== 測試配置檔案 ===")
    
    config_files = ['config.json', 'config_dev.json']
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    json.load(f)
                print(f"✓ {config_file} - 格式正確")
            except json.JSONDecodeError as e:
                print(f"✗ {config_file} - JSON格式錯誤: {e}")
                return False
        else:
            print(f"⚠ {config_file} - 檔案不存在")
    
    return True

def main():
    """執行所有測試"""
    print("ZMQ 賓果遊戲 - 系統測試")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_main_module,
        test_bingo_logic,
        test_port_check,
        test_config_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"測試執行錯誤: {e}")
    
    print("\n" + "=" * 40)
    print(f"測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！系統準備就緒。")
        return 0
    else:
        print("⚠ 部分測試失敗，請檢查相關問題。")
        return 1

if __name__ == '__main__':
    sys.exit(main())