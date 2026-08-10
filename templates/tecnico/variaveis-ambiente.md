# Variáveis de ambiente

## Inventário

| Variável | Exposição | Obrigatória | Finalidade | Ambientes |
| --- | --- | --- | --- | --- |
| TBD | Server/public conforme contrato | TBD | TBD | TBD |

## Regras

- Versionar apenas `.env.example`, sempre sem valores reais.
- Ignorar `.env`, `.env.local` e equivalentes com secrets.
- Qualquer prefixo público da stack expõe o valor ao cliente; usar apenas para configuração não sensível.
- Validar variáveis no arranque com schema tipado quando a stack permitir.
- Separar chaves e providers por ambiente.
- Não reutilizar secrets entre development, staging e production.
- Adicionar uma variável ao inventário, `.env.example`, validação e deploy configuration na mesma mudança.
- Exposição acidental exige revogação/rotação e avaliação de Git, logs, bundles, URLs, analytics e backups.

## Setup

Documentar os comandos reais da plataforma escolhida após verificação. Não colocar URLs com passwords, tokens, exemplos `live`, ou strings que pareçam credenciais reais.
