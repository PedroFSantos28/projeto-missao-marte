
import json
from unittest.mock import MagicMock, patch

from src.servicos_telemetria import ServicoTelemetriaEspacial


def criar_resposta_mock(conteudo):
    resposta = MagicMock()
    resposta.__enter__.return_value = resposta
    resposta.read.return_value = conteudo.encode("utf-8")
    return resposta


def test_enviar_dados_com_resposta_json():
    resposta = criar_resposta_mock('{"status": "recebido"}')

    with patch(
        "src.servicos_telemetria.urlopen",
        return_value=resposta
    ) as mock_urlopen:

        servico = ServicoTelemetriaEspacial(
            "http://estacao-marte.com/"
        )

        resultado = servico._enviar_dados(
            "relatorios",
            {"oxigenio": 90}
        )

        assert resultado == {"status": "recebido"}

        requisicao = mock_urlopen.call_args[0][0]

        assert requisicao.full_url == (
            "http://estacao-marte.com/relatorios"
        )
        assert requisicao.get_method() == "POST"
        assert json.loads(requisicao.data.decode("utf-8")) == {
            "oxigenio": 90
        }

        mock_urlopen.assert_called_once_with(
            requisicao,
            timeout=10
        )


def test_enviar_dados_com_resposta_vazia():
    resposta = criar_resposta_mock("")

    with patch(
        "src.servicos_telemetria.urlopen",
        return_value=resposta
    ):
        servico = ServicoTelemetriaEspacial(
            "http://estacao-marte.com",
            timeout=5
        )

        resultado = servico._enviar_dados(
            "alertas",
            {"nivel": 2}
        )

        assert resultado == {"status": "enviado"}


def test_enviar_relatorio():
    resposta = criar_resposta_mock('{"status": "ok"}')

    with patch(
        "src.servicos_telemetria.urlopen",
        return_value=resposta
    ) as mock_urlopen:

        servico = ServicoTelemetriaEspacial(
            "http://estacao-marte.com"
        )

        recursos = {
            "oxigenio": 90,
            "agua": 480
        }

        resultado = servico.enviar_relatorio(recursos)

        assert resultado == {"status": "ok"}

        requisicao = mock_urlopen.call_args[0][0]
        dados = json.loads(requisicao.data.decode("utf-8"))

        assert requisicao.full_url.endswith("/relatorios")
        assert dados["tipo"] == "relatorio_recursos"
        assert dados["recursos"] == recursos


def test_disparar_alerta():
    resposta = criar_resposta_mock('{"status": "alerta enviado"}')

    with patch(
        "src.servicos_telemetria.urlopen",
        return_value=resposta
    ) as mock_urlopen:

        servico = ServicoTelemetriaEspacial(
            "http://estacao-marte.com"
        )

        resultado = servico.disparar_alerta(
            3,
            "Nível crítico de oxigênio"
        )

        assert resultado == {"status": "alerta enviado"}

        requisicao = mock_urlopen.call_args[0][0]
        dados = json.loads(requisicao.data.decode("utf-8"))

        assert requisicao.full_url.endswith("/alertas")
        assert dados["tipo"] == "alerta_emergencia"
        assert dados["nivel"] == 3
        assert dados["mensagem"] == (
            "Nível crítico de oxigênio"
        )
