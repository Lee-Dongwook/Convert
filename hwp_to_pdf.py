#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP to PDF Converter
한글 문서(HWP)를 PDF로 변환하는 도구
"""

import os
import sys
import click
from pathlib import Path
from hwp5.dataio import ParseError
from hwp5.xmlmodel import Hwp5File
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HwpToPdfConverter:
    """HWP 파일을 PDF로 변환하는 클래스"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # 한글 폰트 설정 (시스템에 따라 경로 조정 필요)
        self.setup_korean_font()
    
    def setup_korean_font(self):
        """한글 폰트 설정"""
        try:
            # macOS에서 기본 한글 폰트 경로
            font_paths = [
                "/System/Library/Fonts/AppleGothic.ttc",
                "/System/Library/Fonts/STHeiti Light.ttc",
                "/System/Library/Fonts/STHeiti Medium.ttc"
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('Korean', font_path))
                    logger.info(f"한글 폰트 등록 성공: {font_path}")
                    break
            else:
                logger.warning("한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        except Exception as e:
            logger.warning(f"폰트 등록 실패: {e}")
    
    def extract_text_from_hwp(self, hwp_file_path):
        """HWP 파일에서 텍스트 추출"""
        try:
            hwp = Hwp5File(hwp_file_path)
            text_content = []
            
            # 문서의 모든 섹션을 순회하며 텍스트 추출
            for section in hwp.bodytext.sections:
                for paragraph in section.paragraphs:
                    for char in paragraph.chars:
                        if hasattr(char, 'text'):
                            text_content.append(char.text)
                    text_content.append('\n')
            
            return ''.join(text_content)
            
        except ParseError as e:
            logger.error(f"HWP 파일 파싱 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"텍스트 추출 중 오류 발생: {e}")
            raise
    
    def create_pdf(self, text_content, output_path):
        """추출된 텍스트로 PDF 생성"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # 제목 스타일
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # 중앙 정렬
            )
            
            # 본문 스타일
            body_style = ParagraphStyle(
                'CustomBody',
                parent=self.styles['Normal'],
                fontSize=12,
                spaceAfter=12,
                leading=18
            )
            
            # 제목 추가
            story.append(Paragraph("HWP 변환 문서", title_style))
            story.append(Spacer(1, 20))
            
            # 텍스트를 줄 단위로 분리하여 PDF에 추가
            lines = text_content.split('\n')
            for line in lines:
                if line.strip():  # 빈 줄 제외
                    story.append(Paragraph(line, body_style))
                else:
                    story.append(Spacer(1, 12))
            
            doc.build(story)
            logger.info(f"PDF 생성 완료: {output_path}")
            
        except Exception as e:
            logger.error(f"PDF 생성 중 오류 발생: {e}")
            raise
    
    def convert(self, input_path, output_path=None):
        """HWP 파일을 PDF로 변환"""
        try:
            input_path = Path(input_path)
            
            if not input_path.exists():
                raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {input_path}")
            
            if not input_path.suffix.lower() == '.hwp':
                raise ValueError("입력 파일은 HWP 파일이어야 합니다.")
            
            # 출력 파일 경로 설정
            if output_path is None:
                output_path = input_path.with_suffix('.pdf')
            
            logger.info(f"HWP 파일 읽는 중: {input_path}")
            text_content = self.extract_text_from_hwp(input_path)
            
            logger.info(f"PDF 생성 중: {output_path}")
            self.create_pdf(text_content, output_path)
            
            logger.info("변환 완료!")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"변환 실패: {e}")
            raise

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file', type=click.Path(), help='출력 PDF 파일 경로')
@click.option('-v', '--verbose', is_flag=True, help='상세 로그 출력')
def main(input_file, output_file, verbose):
    """HWP 파일을 PDF로 변환하는 CLI 도구"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        converter = HwpToPdfConverter()
        result = converter.convert(input_file, output_file)
        click.echo(f"변환 완료: {result}")
    except Exception as e:
        click.echo(f"오류 발생: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
