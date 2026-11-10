
import json
from urllib.request import Request, urlopen


class ServicoTelemetriaEspacial:

    def __init__(self, endereco_estacao, timeout=10):
        self.endereco_estacao = endereco_estacao.rstrip("/")
        self.timeout = timeout

    def _enviar_dados(self, endpoint, dados):
        url = f"{self.endereco_estacao}/{endpoint}"

        requisicao = Request(
            url,
            data=json.dumps(dados).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urlopen(requisicao, timeout=self.timeout) as resposta:
            conteudo = resposta.read().decode("utf-8")

            if conteudo:
                return json.loads(conteudo)

            return {"status": "enviado"}

    def enviar_relatorio(self, status_recursos):
        dados = {
            "tipo": "relatorio_recursos",
            "recursos": status_recursos
        }

        return self._enviar_dados("relatorios", dados)

    def disparar_alerta(self, nivel, mensagem):
        dados = {
            "tipo": "alerta_emergencia",
            "nivel": nivel,
            "mensagem": mensagem
        }

        return self._enviar_dados("alertas", dados)
