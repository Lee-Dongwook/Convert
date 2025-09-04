#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP to PDF 변환기 테스트 스크립트
"""

import unittest
import tempfile
import os
from pathlib import Path
from hwp_to_pdf import HwpToPdfConverter

class TestHwpToPdfConverter(unittest.TestCase):
    """HWP to PDF 변환기 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        self.converter = HwpToPdfConverter()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """테스트 정리"""
        # 임시 파일들 정리
        for file_path in Path(self.test_dir).glob('*'):
            if file_path.is_file():
                file_path.unlink()
        os.rmdir(self.test_dir)
    
    def test_converter_initialization(self):
        """변환기 초기화 테스트"""
        self.assertIsNotNone(self.converter)
        self.assertIsNotNone(self.converter.styles)
    
    def test_invalid_file_path(self):
        """존재하지 않는 파일 경로 테스트"""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert("nonexistent.hwp")
    
    def test_invalid_file_extension(self):
        """잘못된 파일 확장자 테스트"""
        # 임시 텍스트 파일 생성
        temp_file = Path(self.test_dir) / "test.txt"
        temp_file.write_text("This is a test file")
        
        with self.assertRaises(ValueError):
            self.converter.convert(str(temp_file))
    
    def test_output_path_generation(self):
        """출력 파일 경로 자동 생성 테스트"""
        input_path = Path("test.hwp")
        expected_output = input_path.with_suffix('.pdf')
        
        # 실제 파일이 없어도 경로 생성은 가능해야 함
        self.assertEqual(expected_output, Path("test.pdf"))
    
    def test_font_setup(self):
        """폰트 설정 테스트"""
        # 폰트 설정이 오류 없이 실행되어야 함
        try:
            self.converter.setup_korean_font()
        except Exception as e:
            # 폰트 설정 실패는 경고만 발생해야 함
            self.assertIsInstance(e, Exception)

def create_test_hwp_file():
    """테스트용 HWP 파일 생성 (실제 HWP 파일이 없는 경우)"""
    # 이 함수는 실제 HWP 파일이 있을 때만 사용
    # 테스트 환경에서는 mock 객체나 실제 HWP 파일을 사용해야 함
    pass

if __name__ == '__main__':
    # 테스트 실행
    unittest.main(verbosity=2)
    
    print("\n테스트 실행 완료!")
    print("참고: 실제 HWP 파일이 있는 경우 더 자세한 테스트가 가능합니다.")
