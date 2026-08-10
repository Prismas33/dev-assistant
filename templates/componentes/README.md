# Catálogo de componentes

Ainda não existem componentes documentados.

Criar um componente quando uma secção ou comportamento tiver responsabilidade, estado, teste ou evolução próprios, mesmo que seja usado inicialmente numa única página. Não extrair markup trivial apenas para aumentar o número de ficheiros.

## Fronteiras

- Componentes de página: composição leve.
- Componentes de feature: UI e interação do domínio.
- Componentes de UI: primitivas transversais sem conhecimento do domínio.
- Hooks/stores: estado e coordenação.
- Actions/queries/services/repositories: operações, dados e negócio fora da UI.

## Registo de componente

Para cada componente relevante, documentar:

- caminho e responsabilidade;
- props/contratos e variantes;
- estados loading, empty, error e disabled;
- comportamento responsivo e acessibilidade;
- dependências e limitações;
- exemplo de uso quando trouxer clareza.

Componentes visuais não acedem diretamente à base de dados, SDKs externos, secrets ou operações privilegiadas.
