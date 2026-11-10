
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Caminho do painel HTML
PAINEL_HTML = Path(__file__).resolve().parents[1] / "web" / "painel.html"


@pytest.fixture
def navegador(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1365,768")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # Disponibiliza o navegador para a captura de tela em caso de falha
    request.node.driver = driver

    driver.get(PAINEL_HTML.as_uri())

    yield driver

    driver.quit()


def test_solicitacao_valida(navegador):
    espera = WebDriverWait(navegador, 10)

    campo = espera.until(
        EC.visibility_of_element_located(
            (By.ID, "quantidadeOxigenio")
        )
    )
    campo.send_keys("10")

    botao = espera.until(
        EC.element_to_be_clickable((By.ID, "btnSolicitar"))
    )
    botao.click()

    mensagem = espera.until(
        EC.visibility_of_element_located((By.ID, "resultado"))
    )

    assert "Solicitação realizada com sucesso" in mensagem.text
    assert "10" in mensagem.text


def test_quantidade_invalida(navegador):
    espera = WebDriverWait(navegador, 10)

    campo = espera.until(
        EC.visibility_of_element_located(
            (By.ID, "quantidadeOxigenio")
        )
    )
    campo.send_keys("0")

    navegador.find_element(By.ID, "btnSolicitar").click()

    mensagem = espera.until(
        EC.visibility_of_element_located((By.ID, "resultado"))
    )

    assert "Informe uma quantidade válida" in mensagem.text


def test_oxigenio_insuficiente(navegador):
    espera = WebDriverWait(navegador, 10)

    campo = espera.until(
        EC.visibility_of_element_located(
            (By.ID, "quantidadeOxigenio")
        )
    )
    campo.send_keys("150")

    navegador.find_element(By.ID, "btnSolicitar").click()

    mensagem = espera.until(
        EC.visibility_of_element_located((By.ID, "resultado"))
    )

    assert "oxigênio insuficiente" in mensagem.text
