# -*- coding: utf-8 -*-
"""
[ID]: Wrapper Backward-Compatible untuk Installer Zoo Code / Roo Code Hybrid.
Seluruh logika inti telah dimutakhirkan ke vibe_tools/setup_zoo_hybrid.py.
Modul ini mempertahankan antarmuka lama agar skrip atau workflow yang ada tidak mengalami regresi.
"""

from vibe_tools.setup_zoo_hybrid import (
    MODEL_OLLAMA_TARGET,
    TEMPLATE_ATURAN_SPESIFIK_PROYEK,
    TEMPLATE_ROOT,
    VIBE_TOOLS_DIR,
    bangun_mcp_json_bebas_rahasia,
    cek_atau_pasang_ollama,
    main,
    pasang_roo_hybrid,
    pasang_zoo_hybrid,
    sinkronkan_template_universal,
    tentukan_target_proyek,
)

if __name__ == "__main__":
    main()
