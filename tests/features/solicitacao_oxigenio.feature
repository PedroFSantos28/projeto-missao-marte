
# language: pt

Funcionalidade: Gerenciamento de recursos do habitat
  Como responsável pelo habitat de Marte
  Quero controlar o consumo de recursos
  Para garantir a sobrevivência dos astronautas

  Cenário: Consumo de oxigênio e água com estoque suficiente
    Dado que o habitat possui 100 unidades de oxigênio e 500 de água
    Quando forem consumidas 10 unidades de oxigênio e 20 de água
    Então o estoque de oxigênio deve ser 90
    E o estoque de água deve ser 480
