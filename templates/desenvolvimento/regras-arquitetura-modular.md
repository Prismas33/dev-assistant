# Regras de arquitetura modular

## Princípio

Cada responsabilidade independente deve ter o seu próprio componente ou módulo. Não usar limites arbitrários de linhas; tamanho é um sinal, enquanto responsabilidade, acoplamento, testabilidade e evolução isolada determinam a separação.

## Entry files

`page`, `layout`, `App`, `main`, `index` e outros entrypoints devem limitar-se a rotas, metadata, wiring e composição importada.

Não concentrar num entrypoint várias secções completas, estado complexo, fetch/SDKs, persistência, validação e regras de negócio.

## Fronteiras

| Responsabilidade | Módulo esperado |
| --- | --- |
| Secção visual independente | component da feature |
| UI transversal | `components/ui/` |
| Estado/interação | hook ou store |
| Operação da UI | action/mutation |
| Leitura de dados | query |
| Regra de negócio | service/use-case |
| Persistência/provider | repository/client |
| Validação | schema/validator |
| Contrato | type/interface |
| Transformação | helper próprio |
| Configuração | ficheiro explícito |

Nem todas as features precisam de todas as camadas. Não criar pastas vazias nem dividir markup trivial sem uma fronteira real.

## Gate

- [ ] O ficheiro tem uma responsabilidade principal?
- [ ] A página/layout apenas compõe e orquestra levemente?
- [ ] Secções independentes são componentes?
- [ ] Estado, dados, validação e negócio estão fora da UI de apresentação?
- [ ] Persistência e SDKs externos estão isolados?
- [ ] Cada responsabilidade pode ser testada e alterada isoladamente?
