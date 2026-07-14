#!/usr/bin/env python3
"""teacher 스킬 HWP 자동화 환경 점검 + 자동 복구.

새 PC(예: 다른 교사 컴퓨터)에서 처음 HWP 작업을 하기 전에 1회 실행한다.
이미 정상 설정된 PC에서 다시 실행해도 아무것도 변경하지 않는다(멱등).

점검/복구 항목:
  1. Python 실행 환경 (실제 경로 출력)
  2. pywin32 (win32com import)
  3. 한글 COM ProgID (HWPFrame.HwpObject) 등록 여부
  4. HWP 자동화 보안모듈:
       HKCU\\Software\\HNC\\HwpAutomation\\Modules 의 FilePathCheckerModule 값이
       실제 존재하는 DLL을 가리키면 PASS(변경 없음).
       아니면 스킬 동봉 scripts/FilePathCheckerModule.dll 을
       %LOCALAPPDATA%\\FilePathCheckerModule\\ 로 복사하고 레지스트리에 등록(FIXED).
       구버전 한글 호환을 위해 HwpUserAction\\Modules 에도 같이 등록한다.
       이 등록이 없으면 한글이 자동화 파일 접근마다 보안 승인창을 띄우고,
       무인 실행은 그 창에서 멈춘다.
  5. 실제 한글 COM 기동 후 RegisterModule 반환값 True 확인 (--no-com-test 로 생략)

사용법:
    python setup_env.py               # 점검 + 자동 복구 + COM 검증
    python setup_env.py --check-only  # 변경 없이 점검만
    python setup_env.py --no-com-test # 한글 기동 검증 생략
"""

import argparse
import os
import shutil
import sys

RESULTS = []

REG_KEYS = (
    r"Software\HNC\HwpAutomation\Modules",
    r"Software\HNC\HwpUserAction\Modules",  # 구버전 한글 호환
)
VALUE_NAME = "FilePathCheckerModule"


def report(status, name, detail=""):
    RESULTS.append(status)
    line = f"[{status}] {name}"
    if detail:
        line += f" - {detail}"
    print(line)


def check_python():
    exe = sys.executable
    ver = ".".join(map(str, sys.version_info[:3]))
    if "WindowsApps" in exe:
        report("WARN", "Python", f"{exe} (스토어 스텁 경유 - 실제 설치 경로 사용 권장)")
    else:
        report("PASS", "Python", f"{ver} @ {exe}")


def check_pywin32():
    try:
        import win32com.client  # noqa: F401

        report("PASS", "pywin32", "win32com import OK")
        return True
    except ImportError:
        report("FAIL", "pywin32", "미설치 - 실행: python -m pip install pywin32")
        return False


def check_hwp_com():
    import winreg

    try:
        winreg.CloseKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "HWPFrame.HwpObject"))
        report("PASS", "한글 COM", "HWPFrame.HwpObject 등록됨")
        return True
    except OSError:
        report("FAIL", "한글 COM", "HWPFrame.HwpObject 없음 - 한글(한컴오피스) 설치 필요")
        return False


def _read_module_value():
    import winreg

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEYS[0]) as key:
            val, _ = winreg.QueryValueEx(key, VALUE_NAME)
            return val
    except OSError:
        return None


def check_security_module(fix):
    import winreg

    current = _read_module_value()
    if current and os.path.isfile(current):
        report("PASS", "보안모듈", f"등록됨: {current}")
        return True

    detail = "레지스트리 값 없음" if not current else f"등록된 DLL 파일이 없음: {current}"
    if not fix:
        report("FAIL", "보안모듈", f"{detail} - 자동 복구는 --check-only 없이 실행")
        return False

    bundled = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "FilePathCheckerModule.dll"
    )
    if not os.path.isfile(bundled):
        report("FAIL", "보안모듈", f"동봉 DLL 없음: {bundled} (스킬 복사가 불완전한지 확인)")
        return False

    stable_dir = os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "FilePathCheckerModule"
    )
    stable_dll = os.path.join(stable_dir, "FilePathCheckerModule.dll")
    os.makedirs(stable_dir, exist_ok=True)
    if not os.path.isfile(stable_dll) or os.path.getsize(stable_dll) != os.path.getsize(bundled):
        shutil.copy2(bundled, stable_dll)

    for subkey in REG_KEYS:
        key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_SZ, stable_dll)
        winreg.CloseKey(key)

    report("FIXED", "보안모듈", f"{detail} -> 동봉 DLL 등록: {stable_dll}")
    return True


def com_register_test():
    import win32com.client as win32

    hwp = None
    ok = False
    try:
        hwp = win32.Dispatch("HWPFrame.HwpObject")
        ok = bool(hwp.RegisterModule("FilePathCheckDLL", VALUE_NAME))
    except Exception as e:
        report("FAIL", "COM 검증", f"한글 기동 실패: {e}")
        return False
    finally:
        if hwp is not None:
            try:
                hwp.Quit()
            except Exception:
                pass
    if ok:
        report("PASS", "COM 검증", "RegisterModule=True (보안 승인창 없이 자동화 가능)")
    else:
        report("FAIL", "COM 검증", "RegisterModule=False - 레지스트리/DLL 경로 확인 필요")
    return ok


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    ap = argparse.ArgumentParser(description="teacher 스킬 HWP 자동화 환경 점검/복구")
    ap.add_argument("--check-only", action="store_true", help="변경 없이 점검만")
    ap.add_argument("--no-com-test", action="store_true", help="한글 기동 검증 생략")
    args = ap.parse_args()

    check_python()
    has_pywin32 = check_pywin32()
    has_hwp = check_hwp_com()
    module_ok = check_security_module(fix=not args.check_only)

    if args.no_com_test:
        pass
    elif not (has_pywin32 and has_hwp):
        report("SKIP", "COM 검증", "선행 조건 FAIL로 생략")
    elif not module_ok:
        report("SKIP", "COM 검증", "보안모듈 미해결로 생략(변환 시 승인창이 뜰 수 있음)")
    else:
        com_register_test()

    fails = RESULTS.count("FAIL")
    print()
    if fails == 0:
        print("환경 점검 완료: 모든 항목 정상")
        return 0
    print(f"환경 점검 실패: FAIL {fails}건 - 위 안내를 따라 조치 후 재실행")
    return 1


if __name__ == "__main__":
    sys.exit(main())
