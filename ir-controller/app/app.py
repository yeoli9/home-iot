from fastapi import FastAPI, HTTPException, BackgroundTasks
import json
import pigpio
import time
import atexit

# 1) 설정
IR_JSON     = "app/airConditioner.json"
TX_PIN      = 14          # BCM 14 (IR LED 연결 핀)
CARRIER_HZ  = 38000       # 38 kHz
HALF_PERIOD = int(1_000_000 / CARRIER_HZ / 2)  # ≈13µs

# 2) pigpio 초기화
pi = pigpio.pi("127.0.0.1", 8888)
if not pi.connected:
    raise SystemExit("pigpio 데몬 연결 실패")
pi.set_mode(TX_PIN, pigpio.OUTPUT)

# 3) JSON 불러오기
with open(IR_JSON, "r") as f:
    ir_codes = json.load(f)

app = FastAPI(title="IR Remote API")


def send_ir(pulses: list[int]):
    """
    µs 단위 펄스 리스트를
    - ON 구간엔 38kHz 캐리어를 비트뱅(bit-bang)
    - OFF 구간엔 LED 완전 꺼짐
    으로 재생합니다.
    """
    pi.wave_clear()
    wave = []
    level = 1  # 1=ON, 0=OFF

    for pulse in pulses:
        if level:
            # ON 구간: 38 kHz 캐리어 비트뱅
            cycles = int(pulse / (HALF_PERIOD * 2))
            for _ in range(cycles):
                wave.append(pigpio.pulse(1 << TX_PIN, 0, HALF_PERIOD))
                wave.append(pigpio.pulse(0, 1 << TX_PIN, HALF_PERIOD))
        else:
            # OFF 구간: LED 완전 OFF
            wave.append(pigpio.pulse(0, 1 << TX_PIN, pulse))
        level ^= 1

    pi.wave_add_generic(wave)
    wid = pi.wave_create()
    if wid >= 0:
        pi.wave_send_once(wid)
        while pi.wave_tx_busy():
            time.sleep(0.01)
        pi.wave_delete(wid)
    # 끝나고는 LED 끄기
    pi.write(TX_PIN, 0)


@app.get("/keys")
async def list_keys():
    """
    저장된 IR 코드 키 목록을 반환합니다.
    """
    return {"keys": list(ir_codes.keys())}

@app.get("/{action}")
async def ir_action(action: str, background_tasks: BackgroundTasks):
    """
    예) GET /turn_on → 비동기로 IR 송신을 트리거하고 즉시 응답
    """
    pulses = ir_codes.get(action)
    if pulses is None:
        raise HTTPException(status_code=404, detail=f"지원하지 않는 액션: {action}")
    background_tasks.add_task(send_ir, pulses)
    return {"status": "accepted", "action": action}


@atexit.register

def cleanup():
    pi.stop()
