#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT Mediator 테스트 파일
"""

from gpt_mediator import run_datapcr
import os

def auto_detect_and_process():
    """입력 자동 감지 및 처리"""
    print("=== GPT Mediator 자동 감지 테스트 ===")
    print("텍스트 또는 파일 경로를 입력하세요:")
    print("예시:")
    print("- 텍스트: 오늘 날씨가 좋네요")
    print("- 파일 경로: my_schedule.txt 또는 C:/path/to/file.txt")
    print("(입력 완료 후 Enter 두 번)")
    
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    input_data = "\n".join(lines).strip()
    
    if not input_data:
        print("입력이 없습니다.")
        return
    
    print(f"\n입력된 내용:\n{input_data}")
    print("\n처리 결과:")
    
    # 파일 경로인지 확인
    if os.path.exists(input_data):
        print("파일로 감지되어 파일 처리 모드로 실행합니다.")
        try:
            result = run_datapcr(input_data, is_file=True)
            print(f"결과: {result}")
        except Exception as e:
            print(f"오류: {e}")
    else:
        print("텍스트로 감지되어 텍스트 처리 모드로 실행합니다.")
        try:
            result = run_datapcr(input_data, is_file=False)
            print(f"결과: {result}")
        except Exception as e:
            print(f"오류: {e}")

def main():
    """메인 테스트 함수"""
    print("=== GPT Mediator 테스트 ===")
    
    while True:
        print("\n테스트 옵션을 선택하세요:")
        print("1. 자동 감지 테스트 (텍스트/파일 자동 판단)")
        print("2. 종료")
        
        try:
            choice = input("\n선택 (1-2): ").strip()
            
            if choice == "1":
                auto_detect_and_process()
            elif choice == "2":
                print("테스트를 종료합니다.")
                break
            else:
                print("1, 2 중에서 선택해주세요.")
                
        except KeyboardInterrupt:
            print("\n\n테스트를 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 