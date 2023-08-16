def clean_null_terms(d):
    return {k: v for k, v in d.items() if v is not None}
