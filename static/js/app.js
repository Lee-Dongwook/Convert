// 전역 변수
let selectedFile = null;
let isConverting = false;

// DOM 요소들
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const fileInfo = document.getElementById("fileInfo");
const fileName = document.getElementById("fileName");
const convertBtn = document.getElementById("convertBtn");
const progressSection = document.getElementById("progressSection");
const resultSection = document.getElementById("resultSection");
const errorSection = document.getElementById("errorSection");
const errorText = document.getElementById("errorText");
const downloadBtn = document.getElementById("downloadBtn");

// 이벤트 리스너 등록
document.addEventListener("DOMContentLoaded", function () {
  setupEventListeners();
});

function setupEventListeners() {
  // 파일 입력 변경 이벤트
  fileInput.addEventListener("change", handleFileSelect);

  // 드래그 앤 드롭 이벤트
  uploadArea.addEventListener("dragover", handleDragOver);
  uploadArea.addEventListener("dragleave", handleDragLeave);
  uploadArea.addEventListener("drop", handleDrop);

  // 업로드 영역 클릭 이벤트
  uploadArea.addEventListener("click", () => fileInput.click());
}

// 파일 선택 처리
function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    processSelectedFile(file);
  }
}

// 드래그 오버 처리
function handleDragOver(event) {
  event.preventDefault();
  uploadArea.classList.add("dragover");
}

// 드래그 리브 처리
function handleDragLeave(event) {
  event.preventDefault();
  uploadArea.classList.remove("dragover");
}

// 드롭 처리
function handleDrop(event) {
  event.preventDefault();
  uploadArea.classList.remove("dragover");

  const files = event.dataTransfer.files;
  if (files.length > 0) {
    const file = files[0];
    if (
      file.type === "application/x-hwp" ||
      file.name.toLowerCase().endsWith(".hwp")
    ) {
      processSelectedFile(file);
    } else {
      showError("HWP 파일만 업로드 가능합니다.");
    }
  }
}

// 선택된 파일 처리
function processSelectedFile(file) {
  // 파일 크기 검증 (16MB)
  if (file.size > 16 * 1024 * 1024) {
    showError("파일 크기는 16MB 이하여야 합니다.");
    return;
  }

  selectedFile = file;
  fileName.textContent = file.name;

  // UI 업데이트
  uploadArea.style.display = "none";
  fileInfo.style.display = "block";
  fileInfo.classList.add("slide-up");

  // 다른 섹션들 숨기기
  hideAllSections();
}

// 파일 제거
function removeFile() {
  selectedFile = null;
  fileInput.value = "";

  // UI 초기화
  fileInfo.style.display = "none";
  uploadArea.style.display = "block";
  hideAllSections();
}

// 파일 변환
async function convertFile() {
  if (!selectedFile || isConverting) return;

  isConverting = true;
  convertBtn.disabled = true;
  convertBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 변환 중...';

  // 진행률 표시
  showProgress();

  try {
    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await fetch("/convert", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      // PDF 다운로드
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      // 다운로드 링크 생성
      const a = document.createElement("a");
      a.href = url;
      a.download = selectedFile.name.replace(".hwp", ".pdf");
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      showSuccess();
    } else {
      const errorData = await response.json();
      throw new Error(errorData.error || "변환에 실패했습니다.");
    }
  } catch (error) {
    console.error("변환 오류:", error);
    showError(error.message || "변환 중 오류가 발생했습니다.");
  } finally {
    isConverting = false;
    convertBtn.disabled = false;
    convertBtn.innerHTML = '<i class="fas fa-sync-alt"></i> PDF로 변환';
  }
}

// 진행률 표시
function showProgress() {
  hideAllSections();
  progressSection.style.display = "block";
  progressSection.classList.add("fade-in");
}

// 성공 메시지 표시
function showSuccess() {
  hideAllSections();
  resultSection.style.display = "block";
  resultSection.classList.add("fade-in");
}

// 오류 메시지 표시
function showError(message) {
  hideAllSections();
  errorText.textContent = message;
  errorSection.style.display = "block";
  errorSection.classList.add("fade-in");
}

// 모든 섹션 숨기기
function hideAllSections() {
  progressSection.style.display = "none";
  resultSection.style.display = "none";
  errorSection.style.display = "none";
}

// 다시 시도
function retryConversion() {
  hideAllSections();
  if (selectedFile) {
    convertFile();
  }
}

// 유틸리티 함수들
function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

// 키보드 단축키
document.addEventListener("keydown", function (event) {
  // Ctrl/Cmd + V로 파일 붙여넣기 (지원하는 브라우저에서)
  if ((event.ctrlKey || event.metaKey) && event.key === "v") {
    navigator.clipboard
      .read()
      .then((data) => {
        for (let item of data) {
          if (item.types.includes("Files")) {
            item.getType("Files").then((file) => {
              if (
                file.type === "application/x-hwp" ||
                file.name.toLowerCase().endsWith(".hwp")
              ) {
                processSelectedFile(file);
              }
            });
          }
        }
      })
      .catch((err) => {
        // 클립보드 접근이 지원되지 않는 경우 무시
      });
  }

  // Enter 키로 변환 시작
  if (event.key === "Enter" && selectedFile && !isConverting) {
    convertFile();
  }

  // Escape 키로 파일 선택 취소
  if (event.key === "Escape") {
    removeFile();
  }
});

// 페이지 로드 시 애니메이션
window.addEventListener("load", function () {
  document.body.classList.add("fade-in");
});
