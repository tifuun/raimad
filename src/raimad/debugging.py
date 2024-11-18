import gc
import sys

def insane_variable_name_scanner(obj):
    result = []
    for ref in gc.get_objects():
        #if ref is obj:
        #    print(f'----{ref}')
        #    result.append(ref)
        if isinstance(ref, dict):
            for k, v in ref.items():
                if v is obj:
                    result.append(f"dict key: {k}")
        elif hasattr(ref, '__dict__'):
            for k, v in ref.__dict__.items():
                if v is obj:
                    result.append(f"{ref.__class__.__name__} attribute: {k}")
    return result

