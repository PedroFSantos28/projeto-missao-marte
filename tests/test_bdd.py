
import pytest

from pytest_bdd import scenarios, given, when, then, parsers

# Carrega os cenários Gherkin
scenarios("features/solicitacao_oxigenio.feature")


@given(
    parsers.parse(
        "que o habitat possui {oxigenio:d} unidades de oxigênio e {agua:d} de água"
    ),
    target_fixture="estoque_inicial"
)
def habitat_com_recursos(gerenciador_recursos, oxigenio, agua):
    assert gerenciador_recursos.estoque_oxigenio == oxigenio
    assert gerenciador_recursos.estoque_agua == agua

    return gerenciador_recursos


@when(
    parsers.parse(
        "forem consumidas {oxigenio:d} unidades de oxigênio e {agua:d} de água"
    )
)
def consumir_recursos(estoque_inicial, oxigenio, agua):
    estoque_inicial.consumir_recursos(
        oxigenio=oxigenio,
        agua=agua
    )


@then(parsers.parse("o estoque de oxigênio deve ser {quantidade:d}"))
def verificar_estoque_oxigenio(estoque_inicial, quantidade):
    assert estoque_inicial.estoque_oxigenio == quantidade


@then(parsers.parse("o estoque de água deve ser {quantidade:d}"))
def verificar_estoque_agua(estoque_inicial, quantidade):
    assert estoque_inicial.estoque_agua == quantidade
