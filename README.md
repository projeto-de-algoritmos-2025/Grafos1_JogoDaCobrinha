# Grafos1_JogoDaCobrinha

**Número da Lista**: X<br>
**Conteúdo da Disciplina**: XXXXXXXXXX<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/2006196  |  Wallyson Paulo Costa Souza |
| 22/2006893  |  Kaio Macedo Santana |

## Sobre 
Esta é uma implementação do jogo da cobrinha que demonstra algoritmos de busca em grafos (Busca em Largura - BFS e Busca em Profundidade - DFS) para busca de caminho.


## Instalação 
**Linguagem**: xxxxxx<br>
**Framework**: (caso exista)<br>
Descreva os pré-requisitos para rodar o seu projeto e os comandos necessários.

## Uso 
Teclas de seta: Controlam a cobrinha (modo manual)

1: Muda para o modo manual

2: Muda para o modo de algoritmo BFS (a cobrinha encontra automaticamente o caminho mais curto até a comida)

3: Muda para o modo de algoritmo DFS (a cobrinha usa busca em profundidade para encontrar a comida)

R: Reinicia o jogo

+/=: Aumenta a velocidade do jogo

-: Diminui a velocidade do jogo

## Outros 
Características

    Jogabilidade clássica de cobrinha

    Representação do grid do jogo como grafo

    Algoritmo BFS (Busca em Largura) para encontrar o caminho mais curto até a comida

    Algoritmo DFS (Busca em Profundidade) para encontrar um caminho até a comida

    Representação visual do grid

    Controle de velocidade

    Acompanhamento da pontuação

Como Funciona

O jogo implementa os seguintes componentes principais:

    Cobrinha: Gerencia os segmentos e o movimento da cobrinha

    Comida: Coloca comida aleatoriamente no grid

    Grafo: Representa o grid do jogo como um grafo para os algoritmos de busca de caminho

    BFS/DFS: Implementa os algoritmos de busca para encontrar caminhos da cabeça da cobrinha até a comida

Os algoritmos de grafo tratam cada célula no grid como um nó, com arestas conectando células adjacentes. O algoritmo BFS encontra o caminho mais curto até a comida, enquanto o DFS encontra qualquer caminho até a comida.

Ambos os algoritmos evitam caminhos que causariam colisões com a própria cobrinha.




