-- Desafio da Montanha Russa --

Retirado do "Little Book of Semaphores":

"Suponha que haja n threads de passageiros e uma thread de carrinho.
Os passageiros esperam repetidamente para andar no carrinho, 
que suporta C passageiros, onde C < n. O carrinho pode andar apenas 
quando estiver cheio."

Escolhemos o problema pelo seu contexto incomum (embora o mesmo possa
ser dito de muitos dos problemas do livro). Nossa solucao gira em torno
de semaforos para a entrada e saida de passageiros no carro.

Parametros suportados:
- Quantidade de lugares no carrinho
- Quantidade de passageiros (podem ser adicionados a qualquer momento)
- Passageiros retornam para a fila ou nao

Desenvolvido por:
Gustavo de Mello Crivelli  - RA 136008
Vinicius Andrade Frederico - RA 139223