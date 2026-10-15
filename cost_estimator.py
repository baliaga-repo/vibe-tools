"""
[ID]: Modul Estimasi Biaya & Pemilih Model Cerdas (Cost Estimator & Model Selector)
Digunakan untuk menghitung estimasi penggunaan token (in/out) serta biaya USD
berdasarkan tarif resmi OpenRouter sebelum tugas penalaran mendalam dieksekusi.

[EN]: Cost Estimation & Intelligent Model Selector Module
Used to calculate token usage estimates (in/out) and USD costs
based on official OpenRouter rates before executing deep reasoning tasks.
"""
from dataclasses import dataclass
from typing import Dict, List, Tuple
import sys

# Konfigurasi encoding UTF-8 untuk terminal Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

@dataclass
class ModelTariff:
    """
[ID]: Struktur data tarif model per 1 juta token.
[EN]: Data structure for pricing model per 1 million tokens.
"""
    key: str
    display_name: str
    alias: str
    input_usd_per_1m: float
    output_usd_per_1m: float
    tier: str  # 'reasoning', 'premium', 'economy', 'free', 'worker'
    emoji: str
    deskripsi: str

# Katalog tarif model (harga OpenRouter per 1M token)
MODEL_REGISTRY: Dict[str, ModelTariff] = {
    "deepseek-r1": ModelTariff(
        key="deepseek-r1",
        display_name="DeepSeek-R1 (Reasoning)",
        alias="r1",
        input_usd_per_1m=0.55,
        output_usd_per_1m=2.19,
        tier="reasoning",
        emoji="🧠",
        deskripsi="Penalaran logika murni, debugging rumit & matematika"
    ),
    "claude-sonnet": ModelTariff(
        key="claude-sonnet",
        display_name="Claude Sonnet 4.5 (Arsitektur)",
        alias="claude",
        input_usd_per_1m=3.00,
        output_usd_per_1m=15.00,
        tier="premium",
        emoji="👑",
        deskripsi="Standar emas arsitektur, refactoring sistem & desain modular"
    ),
    "deepseek-v3": ModelTariff(
        key="deepseek-v3",
        display_name="DeepSeek-V3 (Super Hemat)",
        alias="deepseek",
        input_usd_per_1m=0.27,
        output_usd_per_1m=1.10,
        tier="economy",
        emoji="⚡",
        deskripsi="Cepat, cerdas, dan sangat hemat untuk koding harian"
    ),
    "qwen-coder": ModelTariff(
        key="qwen-coder",
        display_name="Qwen 2.5 Coder 32B",
        alias="qwen",
        input_usd_per_1m=0.30,
        output_usd_per_1m=0.30,
        tier="economy",
        emoji="💻",
        deskripsi="Spesialis sintaks Python/JS ringan & cepat"
    ),
    "gemini-flash": ModelTariff(
        key="gemini-flash",
        display_name="Gemini Flash (Model Bawaan IDE)",
        alias="gemini",
        input_usd_per_1m=0.00,
        output_usd_per_1m=0.00,
        tier="free",
        emoji="🆓",
        deskripsi="Gratis di IDE, tanpa memotong saldo OpenRouter"
    ),
    "hermes": ModelTariff(
        key="hermes",
        display_name="Hermes Agent (Worker CLI)",
        alias="hermes",
        input_usd_per_1m=0.00,
        output_usd_per_1m=0.00,
        tier="worker",
        emoji="🛠️",
        deskripsi="Eksplorasi mandiri di background terminal tanpa membebani context"
    )
}

def estimate_tokens(text: str, file_count: int = 0, is_reasoning: bool = True) -> Tuple[int, int]:
    """
[ID]: Menghitung estimasi token input dan output secara heuristik.
    Rule of thumb:
    - Bahasa Indonesia / Kode: ~3.5 karakter per token.
    - Konteks file ringkasan: ~250 token per file.
    - Output: ~800 token untuk kode standar, ~1.500 - 2.500 token untuk penalaran arsitektur/deep reasoning.

[EN]: Estimates input and output tokens heuristically.
    Rule of thumb:
    - Indonesian / Code: ~3.5 characters per token.
    - Summary file context: ~250 tokens per file.
    - Output: ~800 tokens for standard code, ~1,500 - 2,500 tokens for architectural reasoning/deep reasoning.
"""
    base_input = len(text) // 3.5
    context_input = file_count * 250
    input_tokens = max(100, int(base_input + context_input))
    
    if is_reasoning:
        output_tokens = 1500
    else:
        output_tokens = 800
        
    return input_tokens, output_tokens

def calculate_cost(tariff: ModelTariff, input_tokens: int, output_tokens: int) -> Tuple[float, str]:
    """
[ID]: Menghitung estimasi biaya dalam USD dan mengembalikan string berformat.
[EN]: Calculates the cost estimate in USD and returns a formatted string.
"""
    if tariff.input_usd_per_1m == 0.0 and tariff.output_usd_per_1m == 0.0:
        return 0.0, "GRATIS ($0.00)"
        
    cost = (input_tokens / 1_000_000 * tariff.input_usd_per_1m) + (output_tokens / 1_000_000 * tariff.output_usd_per_1m)
    if cost < 0.005:
        return cost, f"~${cost:.4f}"
    return cost, f"~${cost:.3f}"

def format_ask_question_options(prompt_text: str, file_count: int = 0) -> List[str]:
    """
[ID]: Menghasilkan daftar string opsi yang siap disajikan ke modal ask_question Antigravity IDE.
[EN]: Generates a list of option strings ready to be presented in the Antigravity IDE ask_question modal.
"""
    input_tok, output_tok = estimate_tokens(prompt_text, file_count=file_count, is_reasoning=True)
    options = []
    
    # Rekomendasi urutan opsi
    ordered_keys = ["deepseek-r1", "claude-sonnet", "deepseek-v3", "gemini-flash", "hermes"]
    
    for key in ordered_keys:
        tariff = MODEL_REGISTRY[key]
        _, cost_str = calculate_cost(tariff, input_tok, output_tok)
        
        prefix = "(Recommended) " if key == "deepseek-r1" else ""
        opt_text = (
            f"{prefix}{tariff.emoji} {tariff.display_name} : {cost_str} "
            f"({input_tok:,} in / {output_tok:,} out) — {tariff.deskripsi}"
        )
        options.append(opt_text)
        
    return options

if __name__ == "__main__":
    # Pengujian cepat via CLI
    sample_prompt = "Rancang sistem sinkronisasi download multi-threading dengan locking protocol dan anti-race condition."
    print("Contoh Opsi Modal ask_question:")
    for opt in format_ask_question_options(sample_prompt, file_count=2):
        print(" -", opt)
