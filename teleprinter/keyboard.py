import sys

"""

This file is made with ai, the ai used was copilot with smart mode.

"""

class Key:
    def __init__(self):
        self.platform = sys.platform

    # -----------------------------
    # Public API
    # -----------------------------
    def wait_for_key(self):
        raw = self._read_blocking()
        return self._normalize(raw)

    def get_key(self):import sys

class Key:
    def __init__(self):
        self.platform = sys.platform

    # -----------------------------
    # Public API
    # -----------------------------
    
    def wait_for_key(self):
        raw = self._read_blocking()
        return self._normalize(raw)

    def get_key(self):
        raw = self._read_nonblocking()
        if raw is None:
            return None
        return self._normalize(raw)

    def is_pressed(self, key):
        raw = self._read_nonblocking()
        if raw is None:
            return False
        return self._normalize(raw) == key

    # -----------------------------
    # Normalization
    # -----------------------------
    def _normalize(self, raw):
        ctrl_map = {
            '\r': "ENTER",
            '\n': "ENTER",
            '\t': "TAB",
            '\x7f': "BACKSPACE",
            '\x08': "BACKSPACE",
            '\x1b': "ESCAPE",
        }

        if raw in ctrl_map:
            return ctrl_map[raw]

        # Ctrl+A..Ctrl+Z
        if len(raw) == 1 and 1 <= ord(raw) <= 26:
            letter = chr(ord('A') + ord(raw) - 1)
            return f"Ctrl-{letter}"

        # Escape sequences
        esc_map = {
            '\x1b[A': "ArrowUp",
            '\x1b[B': "ArrowDown",
            '\x1b[C': "ArrowRight",
            '\x1b[D': "ArrowLeft",
            '\x1b[H': "Home",
            '\x1b[F': "End",
            '\x1b[5~': "PageUp",
            '\x1b[6~': "PageDown",
            '\x1b[2~': "Insert",
            '\x1b[3~': "Delete",
        }
        if raw in esc_map:
            return esc_map[raw]

        # Alt-x
        if raw.startswith('\x1b') and len(raw) == 2:
            return f"Alt-{raw[1]}"

        return raw

    # -----------------------------
    # Windows backend
    # -----------------------------
    def _read_blocking(self):
        if self.platform == "win32":
            import msvcrt
            ch = msvcrt.getwch()
            if ch in ('\x00', '\xe0'):
                ch2 = msvcrt.getwch()
                return self._win_special(ch2)
            return ch
        else:
            return self._posix_read_blocking()

    def _read_nonblocking(self):
        if self.platform == "win32":
            import msvcrt
            if not msvcrt.kbhit():
                return None
            ch = msvcrt.getwch()
            if ch in ('\x00', '\xe0'):
                ch2 = msvcrt.getwch()
                return self._win_special(ch2)
            return ch
        else:
            return self._posix_read_nonblocking()

    def _win_special(self, code):
        mapping = {
            'H': '\x1b[A',
            'P': '\x1b[B',
            'K': '\x1b[D',
            'M': '\x1b[C',
            'G': '\x1b[H',
            'O': '\x1b[F',
            'R': '\x1b[2~',
            'S': '\x1b[3~',
        }
        return mapping.get(code, f"<WIN_{ord(code):02X}>")

    # -----------------------------
    # POSIX backend
    # -----------------------------
    def _posix_read_blocking(self):
        import tty, termios, select
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                seq = ch
                dr, _, _ = select.select([sys.stdin], [], [], 0.02)
                while dr:
                    seq += sys.stdin.read(1)
                    dr, _, _ = select.select([sys.stdin], [], [], 0.01)
                return seq
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def _posix_read_nonblocking(self):
        import tty, termios, select
        fd = sys.stdin.fileno()
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if not dr:
            return None
        return self._posix_read_blocking()

        raw = self._read_nonblocking()
        if raw is None:
            return None
        return self._normalize(raw)

    def is_pressed(self, key):
        raw = self._read_nonblocking()
        if raw is None:
            return False
        return self._normalize(raw) == key

    # -----------------------------
    # Normalization
    # -----------------------------
    def _normalize(self, raw):
        ctrl_map = {
            '\r': "ENTER",
            '\n': "ENTER",
            '\t': "TAB",
            '\x7f': "BACKSPACE",
            '\x08': "BACKSPACE",
            '\x1b': "ESCAPE",
        }

        if raw in ctrl_map:
            return ctrl_map[raw]

        # Ctrl+A..Ctrl+Z
        if len(raw) == 1 and 1 <= ord(raw) <= 26:
            letter = chr(ord('A') + ord(raw) - 1)
            return f"Ctrl-{letter}"

        # Escape sequences
        esc_map = {
            '\x1b[A': "ArrowUp",
            '\x1b[B': "ArrowDown",
            '\x1b[C': "ArrowRight",
            '\x1b[D': "ArrowLeft",
            '\x1b[H': "Home",
            '\x1b[F': "End",
            '\x1b[5~': "PageUp",
            '\x1b[6~': "PageDown",
            '\x1b[2~': "Insert",
            '\x1b[3~': "Delete",
        }
        if raw in esc_map:
            return esc_map[raw]

        # Alt-x
        if raw.startswith('\x1b') and len(raw) == 2:
            return f"Alt-{raw[1]}"

        return raw

    # -----------------------------
    # Windows backend
    # -----------------------------
    def _read_blocking(self):
        if self.platform == "win32":
            import msvcrt
            ch = msvcrt.getwch()
            if ch in ('\x00', '\xe0'):
                ch2 = msvcrt.getwch()
                return self._win_special(ch2)
            return ch
        else:
            return self._posix_read_blocking()

    def _read_nonblocking(self):
        if self.platform == "win32":
            import msvcrt
            if not msvcrt.kbhit():
                return None
            ch = msvcrt.getwch()
            if ch in ('\x00', '\xe0'):
                ch2 = msvcrt.getwch()
                return self._win_special(ch2)
            return ch
        else:
            return self._posix_read_nonblocking()

    def _win_special(self, code):
        mapping = {
            'H': '\x1b[A',
            'P': '\x1b[B',
            'K': '\x1b[D',
            'M': '\x1b[C',
            'G': '\x1b[H',
            'O': '\x1b[F',
            'R': '\x1b[2~',
            'S': '\x1b[3~',
        }
        return mapping.get(code, f"<WIN_{ord(code):02X}>")

    # -----------------------------
    # POSIX backend
    # -----------------------------
    def _posix_read_blocking(self):
        import tty, termios, select
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                seq = ch
                dr, _, _ = select.select([sys.stdin], [], [], 0.02)
                while dr:
                    seq += sys.stdin.read(1)
                    dr, _, _ = select.select([sys.stdin], [], [], 0.01)
                return seq
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def _posix_read_nonblocking(self):
        import tty, termios, select
        fd = sys.stdin.fileno()
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if not dr:
            return None
        return self._posix_read_blocking()
