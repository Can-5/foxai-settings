"""pkexec üzerinden yetki gerektiren işlemler.

Kullanıcının parolasını sormak yerine polkit'in grafiksel penceresi açılır;
parola bu uygulamaya hiçbir zaman uğramaz. Salt-okunur komutlar (dnf repolist,
systemctl status, ...) doğrudan subprocess ile çalıştırılır.
"""

from __future__ import annotations

import re
import subprocess

_MAX_TIMEOUT = 3600
_SAFE_PKG = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._+\-]*$")
# Çekirdek parametrelerinde izin verilen karakterler
_SAFE_KARGS = re.compile(r"^[A-Za-z0-9= _.,\-/]*$")


def valid_pkg_name(name: str) -> bool:
    return bool(_SAFE_PKG.match(name))


def safe_kernel_args(value: str) -> bool:
    return bool(_SAFE_KARGS.match(value))


def run_ro(args: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """Salt-okunur komut. (rc, stdout, stderr) döndürür."""
    try:
        p = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError:
        return 127, "", f"komut bulunamadı: {args[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", f"zaman aşımı ({timeout}s)"


def run_pkexec(args: list[str], timeout: int = _MAX_TIMEOUT) -> tuple[int, str, str]:
    """Yetkili komutu polkit penceresi ile çalıştırır. Görüntülenen pencereyi onaylamak kullanıcının işidir."""
    return run_ro(["pkexec"] + list(args), timeout=timeout)


def output_tail(text: str, max_lines: int = 12) -> str:
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n…\n".join(lines[-max_lines:])
