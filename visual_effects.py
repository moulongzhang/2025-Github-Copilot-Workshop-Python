"""
ビジュアルエフェクト - コンソール出力の視覚的強化
Visual Effects - Visual enhancements for console output
"""
import sys
import time
from enum import Enum
from typing import Optional


class Color(Enum):
    """ANSIカラーコード / ANSI color codes"""
    # 基本色 / Basic colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 明るい色 / Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # 背景色 / Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # スタイル / Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    
    # リセット / Reset
    RESET = "\033[0m"


class VisualEffects:
    """視覚効果クラス / Visual effects class"""
    
    @staticmethod
    def colorize(text: str, color: Color, bg_color: Optional[Color] = None, 
                 bold: bool = False, underline: bool = False) -> str:
        """テキストに色とスタイルを適用 / Apply color and style to text"""
        result = ""
        
        if bold:
            result += Color.BOLD.value
        if underline:
            result += Color.UNDERLINE.value
        if bg_color:
            result += bg_color.value
        
        result += color.value + text + Color.RESET.value
        return result
    
    @staticmethod
    def gradient_text(text: str, colors: list) -> str:
        """グラデーションテキストを作成 / Create gradient text"""
        if not text or not colors:
            return text
        
        result = ""
        color_count = len(colors)
        text_len = len(text)
        
        for i, char in enumerate(text):
            color_index = int((i / text_len) * (color_count - 1))
            result += VisualEffects.colorize(char, colors[color_index])
        
        return result
    
    @staticmethod
    def print_with_animation(text: str, delay: float = 0.05, color: Optional[Color] = None):
        """アニメーション付きでテキストを表示 / Print text with animation"""
        for char in text:
            if color:
                sys.stdout.write(VisualEffects.colorize(char, color))
            else:
                sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()  # 改行
    
    @staticmethod
    def print_box(text: str, color: Color = Color.WHITE, padding: int = 2):
        """テキストをボックスで囲んで表示 / Print text in a box"""
        lines = text.split('\n')
        max_len = max(len(line) for line in lines) if lines else 0
        box_width = max_len + padding * 2
        
        # 上部の境界線
        print(VisualEffects.colorize("╔" + "═" * box_width + "╗", color))
        
        # テキスト行
        for line in lines:
            padded_line = line.center(box_width)
            print(VisualEffects.colorize("║" + padded_line + "║", color))
        
        # 下部の境界線
        print(VisualEffects.colorize("╚" + "═" * box_width + "╝", color))
    
    @staticmethod
    def print_progress_bar(progress: float, width: int = 40, 
                          color: Color = Color.GREEN, label: str = ""):
        """プログレスバーを表示 / Display progress bar"""
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        percentage = int(progress * 100)
        
        bar_text = f"{label} [{bar}] {percentage}%"
        print(VisualEffects.colorize(bar_text, color), end='\r')
        
        if progress >= 1.0:
            print()  # 完了時に改行
    
    @staticmethod
    def print_spinner(message: str, duration: float = 2.0):
        """スピナーアニメーションを表示 / Display spinner animation"""
        spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            spinner = spinner_chars[i % len(spinner_chars)]
            sys.stdout.write(f"\r{spinner} {message}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        sys.stdout.write("\r" + " " * (len(message) + 3) + "\r")  # クリア
        sys.stdout.flush()
    
    @staticmethod
    def print_banner(text: str, char: str = "=", color: Color = Color.CYAN):
        """バナーを表示 / Display banner"""
        banner_width = len(text) + 4
        border = char * banner_width
        
        print(VisualEffects.colorize(border, color))
        print(VisualEffects.colorize(f"{char} {text} {char}", color, bold=True))
        print(VisualEffects.colorize(border, color))
    
    @staticmethod
    def print_success(message: str):
        """成功メッセージを表示 / Display success message"""
        print(VisualEffects.colorize("✓ " + message, Color.BRIGHT_GREEN, bold=True))
    
    @staticmethod
    def print_error(message: str):
        """エラーメッセージを表示 / Display error message"""
        print(VisualEffects.colorize("✗ " + message, Color.BRIGHT_RED, bold=True))
    
    @staticmethod
    def print_warning(message: str):
        """警告メッセージを表示 / Display warning message"""
        print(VisualEffects.colorize("⚠ " + message, Color.BRIGHT_YELLOW, bold=True))
    
    @staticmethod
    def print_info(message: str):
        """情報メッセージを表示 / Display info message"""
        print(VisualEffects.colorize("ℹ " + message, Color.BRIGHT_BLUE, bold=True))


# 使用例 / Usage example
if __name__ == "__main__":
    print("=== ビジュアルエフェクトのデモ / Visual Effects Demo ===\n")
    
    # カラーテキスト
    print("カラーテキスト / Colored Text:")
    print(VisualEffects.colorize("赤色のテキスト / Red text", Color.RED))
    print(VisualEffects.colorize("緑色のテキスト / Green text", Color.GREEN, bold=True))
    print(VisualEffects.colorize("青色のテキスト / Blue text", Color.BLUE, underline=True))
    print()
    
    # グラデーションテキスト
    print("グラデーションテキスト / Gradient Text:")
    gradient_colors = [Color.RED, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.MAGENTA]
    print(VisualEffects.gradient_text("★ キッチンカオスゲーム / Kitchen Chaos Game ★", gradient_colors))
    print()
    
    # ボックス
    VisualEffects.print_box("ゲーム開始！\nGame Start!", Color.BRIGHT_CYAN)
    print()
    
    # バナー
    VisualEffects.print_banner("レシピ配達システム / Recipe Delivery System", color=Color.MAGENTA)
    print()
    
    # ステータスメッセージ
    print("ステータスメッセージ / Status Messages:")
    VisualEffects.print_success("レシピを配達しました / Recipe delivered")
    VisualEffects.print_error("配達に失敗しました / Delivery failed")
    VisualEffects.print_warning("時間が残り少なくなっています / Time running out")
    VisualEffects.print_info("新しいレシピが生成されました / New recipe spawned")
    print()
    
    # プログレスバー
    print("プログレスバー / Progress Bar:")
    for i in range(11):
        VisualEffects.print_progress_bar(i / 10, label="料理中 / Cooking")
        time.sleep(0.2)
    print()
    
    # スピナー
    VisualEffects.print_spinner("レシピを準備中... / Preparing recipe...", duration=2.0)
    VisualEffects.print_success("準備完了！ / Ready!")
    print()
    
    # アニメーションテキスト
    print("アニメーションテキスト / Animated Text:")
    VisualEffects.print_with_animation("🍳 料理を楽しもう！ Enjoy Cooking! 🍕", delay=0.05, color=Color.BRIGHT_YELLOW)
