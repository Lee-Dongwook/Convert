#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HWP to PDF Web Application
웹 브라우저를 통해 HWP 파일을 PDF로 변환할 수 있는 웹 애플리케이션
"""

import os
import tempfile
from pathlib import Path
from flask import Flask, request, render_template, send_file, jsonify, flash
from werkzeug.utils import secure_filename
from hwp_to_pdf import HwpToPdfConverter
import logging

# Flask 앱 설정
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 실제 배포시 변경 필요
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 최대 파일 크기

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {'hwp'}

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """허용된 파일 확장자인지 확인"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    """파일 변환 처리"""
    try:
        # 파일이 요청에 포함되어 있는지 확인
        if 'file' not in request.files:
            return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
        
        file = request.files['file']
        
        # 파일명이 비어있는지 확인
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
        
        # 허용된 파일인지 확인
        if not allowed_file(file.filename):
            return jsonify({'error': 'HWP 파일만 업로드 가능합니다.'}), 400
        
        # 파일명 보안 처리
        filename = secure_filename(file.filename)
        
        # 임시 디렉토리에 파일 저장
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_input_path = os.path.join(temp_dir, filename)
            file.save(temp_input_path)
            
            # 출력 파일 경로 설정
            output_filename = filename.rsplit('.', 1)[0] + '.pdf'
            temp_output_path = os.path.join(temp_dir, output_filename)
            
            # 변환 실행
            converter = HwpToPdfConverter()
            result_path = converter.convert(temp_input_path, temp_output_path)
            
            # 변환된 PDF 파일을 클라이언트에게 전송
            return send_file(
                result_path,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/pdf'
            )
    
    except Exception as e:
        logger.error(f"변환 중 오류 발생: {e}")
        return jsonify({'error': f'변환 실패: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """헬스 체크 엔드포인트"""
    return jsonify({'status': 'healthy', 'service': 'hwp-to-pdf-converter'})

if __name__ == '__main__':
    # 개발 서버 실행
    app.run(debug=True, host='0.0.0.0', port=5000)
