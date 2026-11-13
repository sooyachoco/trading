# COLLECTIVE ALPHA API 발급 및 연결 가이드

현재 KIS / KRX / DART 모두 미신청 상태다. 따라서 시스템은 DEVELOPMENT 모드로 실행되며, 실데이터가 없다는 사실을 결과에 명시한다. 인증키가 없는 상태에서 LIVE 데이터라고 표시하지 않는다.

## 1. KIS Developers
1. 한국투자증권 계좌 및 온라인 ID 등록 상태를 확인한다.
2. KIS Developers 이용안내에서 Open API 서비스를 신청한다.
3. 개발자 포털에서 모의투자용 App Key / App Secret을 발급받는다.
4. 국내주식 현재가 및 기간별 시세 API 문서와 테스트베드에서 요청 파라미터를 확인한다.
5. 로컬 `.env`에 `KIS_APP_KEY`, `KIS_APP_SECRET`을 설정한다.
6. 기본 호스트는 모의투자 호스트다. 실전 호스트·실전 키는 V1.0에서 사용하지 않는다.

공식 안내: https://apiportal.koreainvestment.com/about-howto

## 2. KRX Data Marketplace
1. Data Marketplace 회원가입 및 로그인.
2. 인증키 신청 후 관리자 승인 대기.
3. 서비스 목록에서 필요한 데이터셋을 선택한다. 1차 후보는 유가증권/코스닥 일별매매정보 및 지수 일별시세정보다.
4. 각 서비스의 명세서에서 base URL, endpoint, 인증 파라미터, 날짜/시장 파라미터, 응답 형식을 확인한다.
5. 해당 서비스 활용 신청 및 승인을 확인한다.
6. 승인된 명세에 맞춰 `KRX_BASE_URL`, `KRX_ENDPOINT`, `KRX_AUTH_KEY`와 필요 파라미터를 설정한다.

KRX API는 모든 서비스가 동일한 endpoint나 파라미터를 쓰지 않는다. 명세를 확인하지 않고 endpoint를 추측해 넣지 않는다.

공식 안내: https://openapi.krx.co.kr/contents/OPP/INFO/OPPINFO003.jsp
서비스 목록: https://openapi.krx.co.kr/contents/OPP/INFO/service/OPPINFO004.cmd

## 3. OpenDART
1. OpenDART 회원가입 및 인증키 신청.
2. 개인/기업 신청 유형에 필요한 정보를 입력한다.
3. 인증키 관리 화면에서 발급 상태를 확인한다.
4. `DART_API_KEY`에 설정한다.
5. SKC 종목코드 011790으로 corp-code ZIP에서 8자리 corp_code를 찾아 공시 목록을 조회한다.

공식 신청: https://opendart.fss.or.kr/uss/umt/EgovMberInsertView.do
개발자 페이지: https://opendart.fss.or.kr/

## 4. 로컬 실행

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
# .env는 로컬에서만 편집한다.
pytest -q
collective-alpha-mcp
```

MCP 도구 `provider_status`로 세 공급자 상태를 확인한다. `mock_skc_snapshot`은 응답 스키마 확인용이며 현재가/과거가를 포함하지 않는다. 실제 시세가 필요한 경우 KIS 키가 구성된 뒤 `kis_quote` / `kis_daily_prices`를 호출한다.

## 5. 보안
- .env를 Git에 올리지 않는다.
- 채팅, 이슈, PR, 스크린샷에 키를 붙여넣지 않는다.
- 키가 노출되면 즉시 폐기/재발급한다.
- MCP 서버는 로컬 PC에서 신뢰할 수 있는 사용자만 접근하도록 실행한다.
- V1.0은 조회 및 모의투자 전용이며 실전 주문 기능을 추가하지 않는다.
