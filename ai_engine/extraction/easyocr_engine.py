_reader = None

def get_reader():
    """
    Lazy load and initialize EasyOCR English Reader.
    Supports automatic CUDA/GPU checking and falls back to CPU if unavailable.
    """
    global _reader
    if _reader is None:
        import easyocr
        try:
            import torch
            use_gpu = bool(torch.cuda.is_available())
        except Exception:
            use_gpu = False
            
        print(f"[EasyOCR Engine] Initializing reader (GPU={use_gpu})")
        _reader = easyocr.Reader(["en"], gpu=use_gpu)
    return _reader
