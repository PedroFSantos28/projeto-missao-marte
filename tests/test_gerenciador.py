

import pytest

from src.gerenciador_recursos import (
    GerenciadorRecursosMarte,
    OxigenioInsuficienteError,
    AguaInsuficienteError,
    NivelEmergenciaInvalidoError
)


# 1. TESTES DE CONSUMO DIÁRIO

@pytest.mark.parametrize(
    "astronautas, oxigenio_esperado, agua_esperada",
    [
        (1, 0.84, 3.0),
        (2, 1.68, 6.0),
        (4, 3.36, 12.0),
        (6, 5.04, 18.0)
    ]
)
def test_calcular_consumo_diario(
    astronautas, oxigenio_esperado, agua_esperada
):
    gerenciador = GerenciadorRecursosMarte(
        estoque_oxigenio=100,
        estoque_agua=500,
        numero_astronautas=astronautas
    )

    consumo = gerenciador.calcular_consumo_diario()

    assert consumo["oxigenio"] == pytest.approx(oxigenio_esperado)
    assert consumo["agua"] == pytest.approx(agua_esperada)


# 2. TESTE DE RACIONAMENTO

def test_aplicar_cota_racionamento(gerenciador_recursos):
    gerenciador_recursos.aplicar_cota_racionamento(50)

    consumo = gerenciador_recursos.calcular_consumo_diario()

    assert consumo["oxigenio"] == pytest.approx(1.68)
    assert consumo["agua"] == pytest.approx(6.0)


def test_racionamento_invalido(gerenciador_recursos):
    with pytest.raises(ValueError):
        gerenciador_recursos.aplicar_cota_racionamento(0)


# 3. TESTES DE TAXA DE EMERGÊNCIA

@pytest.mark.parametrize(
    "nivel, taxa_esperada",
    [
        ("baixo", 1.10),
        ("medio", 1.25),
        ("alto", 1.50)
    ]
)
def test_calcular_taxa_emergencia(
    gerenciador_recursos, nivel, taxa_esperada
):
    taxa = gerenciador_recursos.calcular_taxa_emergencia(nivel)

    assert taxa == pytest.approx(taxa_esperada)


def test_nivel_emergencia_invalido(gerenciador_recursos):
    with pytest.raises(NivelEmergenciaInvalidoError):
        gerenciador_recursos.calcular_taxa_emergencia("extremo")


# 4. TESTES DE CONSUMO DOS RECURSOS

def test_consumir_recursos(gerenciador_recursos):
    resultado = gerenciador_recursos.consumir_recursos(
        oxigenio=10,
        agua=20
    )

    assert resultado["oxigenio"] == pytest.approx(90)
    assert resultado["agua"] == pytest.approx(480)


def test_oxigenio_insuficiente(gerenciador_recursos):
    with pytest.raises(OxigenioInsuficienteError):
        gerenciador_recursos.consumir_recursos(
            oxigenio=200,
            agua=20
        )


def test_agua_insuficiente(gerenciador_recursos):
    estoque_oxigenio_original = gerenciador_recursos.estoque_oxigenio

    with pytest.raises(AguaInsuficienteError):
        gerenciador_recursos.consumir_recursos(
            oxigenio=10,
            agua=600
        )

    # Confirma que o oxigênio não foi descontado parcialmente
    assert gerenciador_recursos.estoque_oxigenio == estoque_oxigenio_original


# 5. TESTE DE SOLICITAÇÃO DE OXIGÊNIO EXTRA

def test_solicitar_oxigenio_extra(gerenciador_recursos):
    novo_estoque = gerenciador_recursos.solicitar_oxigenio_extra(50)

    assert novo_estoque == pytest.approx(150)


# 6. TESTES DE TELEMETRIA COM MOCK

def test_reportar_status(gerenciador_recursos):
    gerenciador_recursos.reportar_status()

    gerenciador_recursos.telemetria.enviar_relatorio.assert_called_once()


def test_notificar_emergencia(gerenciador_recursos):
    gerenciador_recursos.notificar_emergencia(
        "alto",
        "Oxigênio em nível crítico"
    )

    gerenciador_recursos.telemetria.disparar_alerta.assert_called_once_with(
        "alto",
        "Oxigênio em nível crítico"
    )
