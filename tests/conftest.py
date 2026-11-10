
import pytest
from unittest.mock import MagicMock

from src.gerenciador_recursos import GerenciadorRecursosMarte


# Fixture global de parâmetros iniciais do habitat
@pytest.fixture(scope="module")
def parametros_habitat():
    parametros = {
        "estoque_oxigenio": 100,
        "estoque_agua": 500,
        "numero_astronautas": 4
    }

    return parametros


# Fixture de função: cria um gerenciador novo para cada teste
@pytest.fixture(scope="function")
def gerenciador_recursos(parametros_habitat):

    # PREPARAÇÃO
    mock_telemetria = MagicMock()

    gerenciador = GerenciadorRecursosMarte(
        estoque_oxigenio=parametros_habitat["estoque_oxigenio"],
        estoque_agua=parametros_habitat["estoque_agua"],
        numero_astronautas=parametros_habitat["numero_astronautas"],
        telemetria=mock_telemetria
    )

    # ENTREGA DO OBJETO PARA O TESTE
    yield gerenciador

    # LIMPEZA
    gerenciador.telemetria = None
    mock_telemetria.reset_mock()


import re
from pathlib import Path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    resultado = outcome.get_result()

    # Captura a tela somente quando a execução do teste falhar
    if resultado.when == "call" and resultado.failed:
        navegador = getattr(item, "driver", None)

        if navegador is not None:
            pasta = Path("screenshots")
            pasta.mkdir(exist_ok=True)

            nome = re.sub(r"[^a-zA-Z0-9_-]", "_", item.name)
            arquivo = pasta / f"{nome}.png"

            navegador.save_screenshot(str(arquivo))
            print(f"\nScreenshot salvo em: {arquivo}")
