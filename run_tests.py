"""Test runner script for Space Pong AI test suite.
Discovers and executes all unit and integration tests under the tests/ directory.
"""
import os
import sys
import time
import unittest
from pathlib import Path

# Configurar entorno headless
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"

for path in (PROJECT_ROOT, SRC_ROOT):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


def main():
    print("=" * 70)
    print(" EJECUTANDO SUITE COMPLETA DE TESTS - SPACE PONG AI")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TESTS_DIR), pattern="test_*.py")

    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    elapsed = time.time() - start_time

    total_tests = result.testsRun
    failed = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    passed = total_tests - failed - errors - skipped

    print("=" * 70)
    print(f" RESUMEN DE PRUEBAS ({elapsed:.2f}s)")
    print(f" Total:     {total_tests}")
    print(f" Pasados:   {passed}")
    print(f" Fallidos:  {failed}")
    print(f" Errores:   {errors}")
    print(f" Omitidos:  {skipped}")
    print("=" * 70)

    if result.wasSuccessful():
        print("[+] TODOS LOS TESTS PASARON EXITOSAMENTE.")
        sys.exit(0)
    else:
        print("[-] SE ENCONTRARON FALLOS EN LA SUITE DE TESTS.")
        sys.exit(1)


if __name__ == "__main__":
    main()
