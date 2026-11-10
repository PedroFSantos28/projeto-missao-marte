
class OxigenioInsuficienteError(Exception):
    pass


class AguaInsuficienteError(Exception):
    pass


class NivelEmergenciaInvalidoError(Exception):
    pass


class GerenciadorRecursosMarte:

    CONSUMO_OXIGENIO = 0.84
    CONSUMO_AGUA = 3.0

    def __init__(
        self,
        estoque_oxigenio,
        estoque_agua,
        numero_astronautas,
        telemetria=None
    ):
        self.estoque_oxigenio = estoque_oxigenio
        self.estoque_agua = estoque_agua
        self.numero_astronautas = numero_astronautas
        self.cota_racionamento = 1.0
        self.telemetria = telemetria

        self._validar_dados_iniciais()

    def _validar_dados_iniciais(self):
        if self.estoque_oxigenio < 0:
            raise ValueError("Estoque de oxigênio não pode ser negativo.")

        if self.estoque_agua < 0:
            raise ValueError("Estoque de água não pode ser negativo.")

        if self.numero_astronautas <= 0:
            raise ValueError("Deve existir pelo menos um astronauta.")

    def calcular_consumo_diario(self):
        oxigenio = (
            self.numero_astronautas
            * self.CONSUMO_OXIGENIO
            * self.cota_racionamento
        )

        agua = (
            self.numero_astronautas
            * self.CONSUMO_AGUA
            * self.cota_racionamento
        )

        return {
            "oxigenio": oxigenio,
            "agua": agua
        }

    def calcular_dias_autonomia(self):
        consumo = self.calcular_consumo_diario()

        return {
            "oxigenio": self.estoque_oxigenio / consumo["oxigenio"],
            "agua": self.estoque_agua / consumo["agua"]
        }

    def calcular_taxa_emergencia(self, nivel):
        taxas = {
            "baixo": 1.10,
            "medio": 1.25,
            "alto": 1.50
        }

        if nivel not in taxas:
            raise NivelEmergenciaInvalidoError(
                f"Nível de emergência inválido: {nivel}"
            )

        return taxas[nivel]

    def aplicar_cota_racionamento(self, percentual):
        if not 0 < percentual <= 100:
            raise ValueError(
                "O percentual deve estar entre 0 e 100."
            )

        self.cota_racionamento = percentual / 100

        return self.cota_racionamento

    def consumir_recursos(self, oxigenio, agua):

        if oxigenio < 0 or agua < 0:
            raise ValueError("O consumo não pode ser negativo.")

        if self.estoque_oxigenio < oxigenio:
            raise OxigenioInsuficienteError(
                "Estoque de oxigênio insuficiente!"
            )

        if self.estoque_agua < agua:
            raise AguaInsuficienteError(
                "Estoque de água insuficiente!"
            )

        self.estoque_oxigenio -= oxigenio
        self.estoque_agua -= agua

        return {
            "oxigenio": self.estoque_oxigenio,
            "agua": self.estoque_agua
        }

    def solicitar_oxigenio_extra(self, quantidade):
        if quantidade <= 0:
            raise ValueError(
                "A quantidade solicitada deve ser positiva."
            )

        self.estoque_oxigenio += quantidade

        return self.estoque_oxigenio

    # INTEGRAÇÃO COM A TELEMETRIA

    def reportar_status(self):
        if self.telemetria is None:
            raise RuntimeError("Serviço de telemetria não configurado.")

        status = {
            "estoque_oxigenio": self.estoque_oxigenio,
            "estoque_agua": self.estoque_agua,
            "numero_astronautas": self.numero_astronautas,
            "consumo_diario": self.calcular_consumo_diario()
        }

        return self.telemetria.enviar_relatorio(status)

    def notificar_emergencia(self, nivel, mensagem):
        if self.telemetria is None:
            raise RuntimeError("Serviço de telemetria não configurado.")

        taxa = self.calcular_taxa_emergencia(nivel)

        resposta = self.telemetria.disparar_alerta(
            nivel,
            mensagem
        )

        return {
            "nivel": nivel,
            "taxa_emergencia": taxa,
            "resposta_estacao": resposta
        }
