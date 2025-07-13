import pigpio, time, json, sys

if len(sys.argv)!=2:
    print("사용법: python3 capture_ir.py 저장할_파일.json")
    sys.exit(1)

INPUT_PIN = 15   # BCM 15
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio 데몬에 연결 실패")

pi.set_mode(INPUT_PIN, pigpio.INPUT)

timestamps = []  # (level, tick) 리스트

def _cb(gpio, level, tick):
    # level: 0(LOW) or 1(HIGH)
    timestamps.append((level, tick))

cb = pi.callback(INPUT_PIN, pigpio.EITHER_EDGE, _cb)

print("리모컨 버튼을 눌러 펄스를 캡처하세요... (5초 대기)")
time.sleep(5)

cb.cancel()
pi.stop()

# tick 차이를 마이크로초 단위 펄스로 변환
pulses = []
for i in range(1, len(timestamps)):
    dt = timestamps[i][1] - timestamps[i-1][1]
    pulses.append(dt)

# JSON으로 저장
with open(sys.argv[1], 'w') as f:
    json.dump(pulses, f, indent=2)

print(f"펄스 {len(pulses)}개 저장 완료: {sys.argv[1]}")

