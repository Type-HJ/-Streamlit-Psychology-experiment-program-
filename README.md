# 심리학 실험 프로그램 - Streamlit 사용

Streamlit을 사용한 심리학 실험 프로그램이다. 스트룹 과제와 클릭 반응 테스트를 수행할 수 있고, 실시간 데이터 분석과 시각화 제공
##  설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/Type-HJ/-Streamlit-Psychology-experiment-program-.git
cd -Streamlit-Psychology-experiment-program-
```

### 2. 가상 환경 생성 (선택사항이지만 권장)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 앱 실행
```bash
streamlit run app.py
```

앱이 자동으로 브라우저에서 열립니다. (기본: http://localhost:8501)

## 프로그램 기능

### 실험 수행
- **스트룹 과제** (Stroop Task): 글자 색상을 단어의 의미와 상관없이 선택
- **클릭 반응 테스트** (Click Reaction Test): 화면이 녹색으로 변할 때 최대한 빠르게 클릭

### 데이터 수집
- 참가자 정보 (ID, 나이, 성별)
- 각 시도의 반응시간
- 정확도 및 오류율
- 난이도 및 보상 여부

### 데이터 분석
- 반응시간 추이 차트
- 정확도 분석
- 참가자별 비교 분석
- 실험 유형별 성능 비교

### 데이터 관리
- 자동 CSV 저장 (data/ 폴더)
- 필터링 및 다운로드
- 다중 세션 지원

## 사용 방법

1. **실험 시작** → 참가자 정보 입력
2. **실험 선택** → 스트룹 또는 클릭 반응 테스트
3. **설정 조정** → 난이도, 보상, 시도 횟수
4. **실험 수행** → 자극에 반응
5. **결과 확인** → 통계 및 차트 보기
6. **데이터 다운로드** → CSV 형식으로 저장

## 파일 구조

```
-Streamlit-Psychology-experiment-program-/
├── app.py                 # 메인 Streamlit 앱
├── requirements.txt       # Python 의존성
├── README.md             # 이 문서
└── data/                 # 자동 생성 (실험 데이터 저장)
    └── experiment_*.csv
```

## 기술 스택

- **Streamlit** - 웹 프레임워크
- **Pandas** - 데이터 분석
- **NumPy** - 수치 계산
- **Plotly** - 데이터 시각화

## 난이도 설정

### Easy (쉬움)
- 일치 조건 70%
- 반응시간 제한 긴 편

### Normal (보통)
- 일치 조건 50%
- 일반적인 난이도

### Hard (어려움)
- 불일치 조건만 100%
- 매우 도전적

## 데이터 형식

CSV 파일에는 다음 정보가 포함된다:
- participant_id: 참가자 ID
- age: 나이
- gender: 성별
- date: 실험 날짜/시간
- experiment_type: 실험 유형 (Stroop/Click Reaction)
- trial_number: 시도 번호
- stimulus_word: 자극 단어 (스트룹만)
- stimulus_color: 자극 색상
- correct_color: 정답 색상
- response_color: 응답 색상
- reaction_time_ms: 반응시간 (밀리초)
- accuracy: 정확도 (1=정답, 0=오답)
- difficulty: 난이도
- reward: 보상 여부

## 주의사항

1. **Python 버전**: Python 3.8 이상 권장
2. **브라우저**: 최신 버전의 Chrome, Firefox, Safari, Edge 권장
3. **데이터 백업**: 중요한 데이터는 정기적으로 백업하세요
4. **첫 실행**: 첫 실행 시 라이브러리 로딩에 약간의 시간이 소요됩니다

## 문제 해결

### Streamlit이 실행되지 않을 때
```bash
pip install --upgrade streamlit
```

### 의존성 오류 문제
```bash
pip install -r requirements.txt --upgrade
```

### 데이터가 저장되지 않을 때
- `data/` 폴더가 쓰기 권한이 있는지 확인하세요

## 라이선스

MIT License 사용

## 개발자

Type-HJ

---

*웹 버전은 개발자의 다른 repository인 [Psychology-experiment-program](https://github.com/Type-HJ/Psychology-experiment-program) 저장소를 참고*
