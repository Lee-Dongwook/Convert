# HWP to PDF 변환기

한글 문서(HWP)를 PDF로 변환하는 Python 기반 도구입니다. CLI와 웹 인터페이스를 모두 제공합니다.

## 🚀 주요 기능

- **HWP 파일 지원**: 한글 문서(.hwp) 파일을 PDF로 변환
- **CLI 도구**: 명령줄에서 빠른 변환
- **웹 인터페이스**: 사용자 친화적인 웹 애플리케이션
- **드래그 앤 드롭**: 파일을 쉽게 업로드
- **한글 폰트 지원**: macOS 기본 한글 폰트 자동 감지
- **반응형 디자인**: 모바일과 데스크톱 모두 지원

## 📋 요구사항

- Python 3.7+
- macOS (한글 폰트 지원)
- HWP 파일

## 🛠️ 설치 방법

1. **저장소 클론**
```bash
git clone <repository-url>
cd convert
```

2. **가상환경 생성 및 활성화**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

## 🎯 사용법

### CLI 도구 사용

```bash
# 기본 사용법
python hwp_to_pdf.py document.hwp

# 출력 파일 지정
python hwp_to_pdf.py document.hwp -o output.pdf

# 상세 로그 출력
python hwp_to_pdf.py document.hwp -v

# 도움말
python hwp_to_pdf.py --help
```

### 웹 애플리케이션 실행

```bash
python web_app.py
```

브라우저에서 `http://localhost:5000`으로 접속하여 웹 인터페이스를 사용할 수 있습니다.

## 🌐 웹 인터페이스 기능

- **파일 업로드**: 클릭하거나 드래그 앤 드롭으로 HWP 파일 선택
- **실시간 변환**: 진행률 표시와 함께 변환 진행
- **자동 다운로드**: 변환 완료 시 PDF 파일 자동 다운로드
- **오류 처리**: 상세한 오류 메시지와 재시도 기능
- **키보드 단축키**: Enter(변환), Escape(취소) 등

## 📁 프로젝트 구조

```
convert/
├── hwp_to_pdf.py          # 메인 변환 로직
├── web_app.py             # Flask 웹 애플리케이션
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
├── templates/            # HTML 템플릿
│   └── index.html       # 메인 페이지
└── static/              # 정적 파일
    ├── css/
    │   └── style.css    # 스타일시트
    └── js/
        └── app.js       # JavaScript 로직
```

## 🔧 기술 스택

- **Backend**: Python, Flask
- **HWP 처리**: python-hwp
- **PDF 생성**: ReportLab
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI/UX**: Font Awesome, 반응형 디자인

## ⚠️ 제한사항

- **파일 크기**: 최대 16MB
- **지원 형식**: HWP 파일만 지원
- **폰트**: macOS 기본 한글 폰트에 최적화
- **복잡한 서식**: 일부 복잡한 서식은 단순화될 수 있음

## 🐛 문제 해결

### 일반적인 오류

1. **폰트 오류**
   - macOS에서 기본 한글 폰트가 설치되어 있는지 확인
   - 시스템 폰트 경로 확인

2. **HWP 파일 읽기 오류**
   - 파일이 손상되지 않았는지 확인
   - 파일 형식이 올바른지 확인

3. **메모리 부족**
   - 파일 크기가 너무 큰 경우 더 작은 파일로 테스트

### 로그 확인

```bash
# 상세 로그로 실행
python hwp_to_pdf.py document.hwp -v

# 웹 애플리케이션 로그
python web_app.py
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

- [python-hwp](https://github.com/mete0r/python-hwp) - HWP 파일 파싱 라이브러리
- [ReportLab](https://www.reportlab.com/) - PDF 생성 라이브러리
- [Flask](https://flask.palletsprojects.com/) - 웹 프레임워크

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해 주세요.

---

**참고**: 이 도구는 교육 및 개인 사용 목적으로 제작되었습니다. 상업적 사용 시에는 해당 라이선스를 확인하시기 바랍니다.
