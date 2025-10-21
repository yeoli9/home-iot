# home-iot

라즈베리파이 기반 스마트홈 IoT 제어 시스템

## 📋 프로젝트 소개

**home-iot**는 라즈베리파이에서 동작하는 Python 기반의 스마트홈 제어 시스템입니다. 온습도 센서를 통한 환경 모니터링과 적외선(IR) 통신을 이용한 가전제품 제어 기능을 제공합니다.

### 주요 기능

- 🌡️ **온습도 모니터링**: DHT22 센서를 통한 실시간 온도/습도 측정
- 📊 **Prometheus 통합**: 센서 데이터 메트릭 수집 및 시계열 저장
- 📡 **IR 리모컨 제어**: 에어컨 등 IR 기반 가전제품 원격 제어
- 🎯 **REST API**: FastAPI 기반의 간단하고 빠른 API
- 🐳 **Docker 컨테이너화**: 손쉬운 배포 및 관리

## 🏗️ 시스템 아키텍처

```
┌──────────────┐      ┌──────────────┐
│ DHT22 센서   │      │ IR 리모컨     │
│ (온습도)     │      │ (에어컨 제어)│
└──────┬───────┘      └──────┬───────┘
       │                     │
       │ GPIO 24             │ GPIO 14/15
       │                     │
┌──────▼─────────────────────▼───────┐
│      Raspberry Pi / GPIO           │
├────────────────────────────────────┤
│  Docker Containers                 │
│  ├─ DHT22 Service      :8000       │
│  ├─ IR Controller      :8000       │
│  └─ Prometheus         :9090       │
└────────────────────────────────────┘
```

## 🔧 시스템 요구사항

### 하드웨어
- Raspberry Pi (GPIO 지원 모델)
- DHT22 온습도 센서
- IR LED (적외선 송신)
- IR 리시버 (적외선 수신, 선택사항)

### 소프트웨어
- Docker
- Docker Compose
- pigpio 데몬 (IR 제어용)

### GPIO 핀 구성
- GPIO 24: DHT22 센서 데이터 핀
- GPIO 14: IR LED 송신 핀
- GPIO 15: IR 리시버 수신 핀 (선택사항)

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/yeoli9/home-iot.git
cd home-iot
```

### 2. pigpio 데몬 설치 및 실행

```bash
sudo apt-get update
sudo apt-get install pigpio
sudo pigpiod
```

### 3. DHT22 센서 서비스 시작

```bash
cd dht22
./run.sh
```

서비스 확인:
- DHT22 API: http://localhost:8000
- Prometheus: http://localhost:9090

### 4. IR 컨트롤러 서비스 시작

```bash
cd ir-controller
./run.sh
```

IR Controller API: http://localhost:8000

## 📖 사용법

### DHT22 온습도 센서

#### 센서 데이터 조회

```bash
curl http://localhost:8000/
```

#### Prometheus 메트릭 조회

```bash
curl http://localhost:8000/metrics
```

**메트릭 항목:**
- `dht22_temperature_celsius`: 온도 (섭씨)
- `dht22_humidity_percent`: 습도 (%)

### IR 컨트롤러

#### 사용 가능한 명령어 확인

```bash
curl http://localhost:8000/keys
```

응답 예시:
```json
{
  "keys": ["turn_on", "turn_off", "mode_cool", "mode_dehumid"]
}
```

#### 에어컨 제어

```bash
# 에어컨 켜기
curl http://localhost:8000/turn_on

# 에어컨 끄기
curl http://localhost:8000/turn_off

# 냉방 모드
curl http://localhost:8000/mode_cool

# 제습 모드
curl http://localhost:8000/mode_dehumid
```

### 새로운 IR 코드 학습

리모컨 버튼의 IR 코드를 캡처하려면:

```bash
cd ir-controller/app
python ir_capture.py
```

리모컨 버튼을 누르면 5초간 IR 신호를 캡처하여 JSON 파일로 저장합니다.

## ⚙️ 환경 설정

### DHT22 센서 GPIO 핀 변경

`dht22/docker-compose.yaml` 파일에서 환경변수 수정:

```yaml
environment:
  - DHT_GPIO_PIN=24  # 원하는 GPIO 핀 번호로 변경
```

### Prometheus 수집 주기 변경

`dht22/prometheus.yaml` 파일에서 `scrape_interval` 수정:

```yaml
scrape_configs:
  - job_name: 'dht22'
    scrape_interval: 15s  # 원하는 주기로 변경
```

### IR 코드 추가

`ir-controller/app/airConditioner.json` 파일에 새로운 IR 코드 추가:

```json
{
  "turn_on": [3125, 9750, 536, ...],
  "your_new_command": [3146, 9745, ...]
}
```

## 📂 프로젝트 구조

```
home-iot/
├── README.md
├── dht22/                        # 온습도 센서 모듈
│   ├── app/
│   │   └── app.py               # FastAPI 서버
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   ├── prometheus.yaml          # Prometheus 설정
│   ├── requirements.txt
│   └── run.sh
│
└── ir-controller/               # IR 리모컨 모듈
    ├── app/
    │   ├── app.py              # FastAPI 서버
    │   ├── ir_capture.py       # IR 코드 캡처 유틸리티
    │   └── airConditioner.json # IR 코드 데이터
    ├── Dockerfile
    ├── docker-compose.yaml
    ├── requirements.txt
    └── run.sh
```

## 🔍 API 문서

### DHT22 서비스 (Port: 8000)

| 메소드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | / | 서비스 정보 조회 |
| GET | /metrics | Prometheus 메트릭 조회 |

### IR 컨트롤러 (Port: 8000)

| 메소드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| GET | /keys | 사용 가능한 IR 명령어 목록 |
| GET | /{action} | IR 코드 전송 (예: /turn_on) |

## 🛠️ 기술 스택

- **언어**: Python 3.11-3.13
- **웹 프레임워크**: FastAPI
- **ASGI 서버**: Uvicorn
- **GPIO 제어**:
  - Adafruit CircuitPython DHT
  - Adafruit Blinka
  - pigpio
- **모니터링**: Prometheus
- **컨테이너화**: Docker, Docker Compose

## 🐛 문제 해결

### pigpio 데몬 연결 실패

```bash
# pigpio 데몬 상태 확인
sudo systemctl status pigpiod

# 수동으로 시작
sudo pigpiod
```

### DHT22 센서 읽기 오류

- 센서 연결 상태 확인 (VCC, GND, DATA)
- GPIO 핀 번호가 올바른지 확인
- 센서와 라즈베리파이 사이에 10K 풀업 저항 연결 권장

### Docker 권한 오류

GPIO 접근을 위해 privileged 모드 필요:

```yaml
privileged: true
```

### 컨테이너 로그 확인

```bash
# DHT22 서비스
cd dht22
docker compose logs -f

# IR 컨트롤러
cd ir-controller
docker compose logs -f
```

## 🔮 향후 계획

- [ ] 자동화 로직: 온도 기반 에어컨 자동 제어
- [ ] 웹 대시보드: 실시간 모니터링 UI
- [ ] 데이터베이스 연동: 센서 데이터 장기 보관
- [ ] 알림 기능: 임계값 초과 시 알림
- [ ] 다양한 IR 기기 지원 확장

## 📄 라이선스

This project is open source.

## 👨‍💻 기여자

- yeoli9
- kyungyeol gu

## 📞 문의

프로젝트에 대한 문의사항이나 버그 리포트는 GitHub Issues를 이용해 주세요.
