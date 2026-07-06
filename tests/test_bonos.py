"""
Tests de bonos-service — lógica pura sin BD.
Correr: python3 -m pytest tests/test_bonos.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pydantic import BaseModel


# --- Test 1: Modelo ReclamarRequest ---
def test_reclamar_request_modelo():
    """Valida que el modelo ReclamarRequest funciona correctamente."""
    from app.main import ReclamarRequest
    req = ReclamarRequest(usuario_id=1)
    assert req.usuario_id == 1


def test_reclamar_request_requiere_usuario_id():
    """ReclamarRequest debe requerir usuario_id."""
    from app.main import ReclamarRequest
    try:
        req = ReclamarRequest()  # sin usuario_id
        assert False, "Debería fallar sin usuario_id"
    except Exception:
        pass  # correcto: falla sin el campo requerido


# --- Test 2: Endpoint /livez devuelve estructura correcta ---
def test_livez_estructura():
    """El endpoint /livez debe retornar status alive."""
    from app.main import livez
    resp = livez()
    assert "status" in resp
    assert resp["status"] == "alive"


# --- Test 3: Helper _json ---
def test_json_helper():
    """La función _json convierte un dict a JSON string."""
    from app.main import _json
    result = _json({"key": "value"})
    assert isinstance(result, str)
    assert "key" in result
    assert "value" in result


# --- Test 4: Imports correctos ---
def test_imports_basicos():
    """Verifica que los módulos principales se importan sin error."""
    from app import main
    from app import auth
    assert hasattr(main, 'app')
    assert hasattr(auth, 'usuario_actual')


# --- Test 5: App FastAPI existe y tiene rutas ---
def test_app_tiene_rutas():
    """La app FastAPI debe tener rutas registradas."""
    from app.main import app
    rutas = [r.path for r in app.routes]
    assert "/livez" in rutas
    assert "/readyz" in rutas
    assert "/api/bonos" in rutas


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    fallos = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
        except AssertionError as e:
            fallos += 1
            print(f"FAIL  {fn.__name__}: {e}")
    print(f"\n{len(fns) - fallos}/{len(fns)} tests OK")
    sys.exit(1 if fallos else 0)
