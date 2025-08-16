# 🤝 StockEdu 기여 가이드

## 🌟 기여하기

StockEdu는 오픈소스 프로젝트입니다. 여러분의 기여를 환영합니다!

## 🚀 시작하기

### 1. 개발 환경 설정
```bash
# 저장소 Fork 후 클론
git clone https://github.com/your-username/stockedu.git
cd stockedu

# 의존성 설치
pip install -r requirements.txt

# 개발용 추가 의존성 설치
pip install -r requirements-dev.txt  # 향후 추가 예정
```

### 2. 브랜치 전략
- `main`: 안정된 릴리스 브랜치
- `develop`: 개발 중인 기능들
- `feature/*`: 새로운 기능 개발
- `bugfix/*`: 버그 수정
- `hotfix/*`: 긴급 수정

## 📝 기여 유형

### 🐛 버그 리포트
- GitHub Issues에 버그 보고
- 재현 가능한 최소 예제 제공
- 환경 정보 (OS, Python 버전) 포함

### ✨ 새로운 기능 제안
- GitHub Discussions에서 먼저 논의
- 기능의 필요성과 구현 방향 설명
- 사용자 경험 개선에 도움이 되는지 확인

### 📚 문서 개선
- 사용자 가이드 업데이트
- 코드 주석 개선
- 예제 및 튜토리얼 추가

### 🎨 UI/UX 개선
- 사용자 인터페이스 개선
- 접근성 향상
- 반응형 디자인 적용

## 🔧 개발 가이드라인

### 코드 스타일
- **PEP 8** Python 스타일 가이드 준수
- **Type Hints** 사용 권장
- **Docstring** 모든 함수/클래스에 추가

```python
def calculate_portfolio_value(positions: Dict[str, Position], 
                            prices: Dict[str, float]) -> float:
    """
    포트폴리오의 총 가치를 계산합니다.
    
    Args:
        positions: 보유 포지션 딕셔너리
        prices: 현재 주가 딕셔너리
        
    Returns:
        포트폴리오 총 가치
    """
    pass
```

### 커밋 메시지
```
feat: 새로운 교육 모듈 추가
fix: 포트폴리오 계산 오류 수정
docs: 사용자 가이드 업데이트
style: 코드 포맷팅 개선
refactor: 거래 엔진 리팩토링
test: 단위 테스트 추가
```

### 테스트
- 새로운 기능에는 테스트 코드 필수
- 기존 테스트가 깨지지 않도록 확인
- 커버리지 80% 이상 유지

## 📋 Pull Request 가이드

### 1. PR 전 체크리스트
- [ ] 코드 스타일 가이드 준수
- [ ] 테스트 코드 작성 및 통과
- [ ] 문서 업데이트
- [ ] 충돌 해결

### 2. PR 템플릿
```markdown
## 📝 변경 사항
- 무엇을 변경했는지 명확히 기술

## 🎯 목적
- 왜 이 변경이 필요한지 설명

## 🧪 테스트
- 어떻게 테스트했는지 설명

## 📷 스크린샷 (UI 변경 시)
- 변경 전/후 비교 이미지

## ✅ 체크리스트
- [ ] 테스트 통과
- [ ] 문서 업데이트
- [ ] 코드 리뷰 요청
```

## 🏗️ 프로젝트 구조 이해

### 핵심 모듈
- `src/education/`: 교육 콘텐츠 모듈
- `src/trading/`: 거래 시뮬레이션 엔진
- `src/analysis/`: AI 분석 및 추천 시스템
- `src/gui/`: 사용자 인터페이스

### 설계 원칙
- **모듈화**: 기능별로 독립적인 모듈 구성
- **확장성**: 새로운 기능 추가가 쉽도록 설계
- **테스트 가능성**: 단위 테스트가 용이한 구조
- **문서화**: 코드와 기능에 대한 명확한 문서

## 🎓 학습 리소스

### Python 개발
- [PEP 8 스타일 가이드](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [tkinter 문서](https://docs.python.org/3/library/tkinter.html)

### 금융 및 투자
- [야후 파이낸스 API](https://pypi.org/project/yfinance/)
- [투자 지표 이해](https://www.investopedia.com/)

## 📞 소통하기

### 커뮤니케이션 채널
- **GitHub Issues**: 버그 리포트, 기능 요청
- **GitHub Discussions**: 일반적인 질문, 아이디어 논의
- **Pull Requests**: 코드 리뷰 및 피드백

### 행동 강령
- 존중과 예의를 갖춘 소통
- 건설적인 피드백 제공
- 다양성과 포용성 존중
- 학습 지향적 태도 유지

## 🎉 기여자 인정

모든 기여자는 프로젝트 README에 기록됩니다:
- 코드 기여자
- 문서 작성자
- 버그 리포터
- 아이디어 제공자

## 📋 릴리스 프로세스

1. **기능 개발** (feature branch)
2. **코드 리뷰** (Pull Request)
3. **테스트 및 검증** (CI/CD)
4. **문서 업데이트**
5. **릴리스 노트 작성**
6. **버전 태깅**

감사합니다! 🙏