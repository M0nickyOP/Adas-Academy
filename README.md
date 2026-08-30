# Adas-Academy

## Diferença entre lista e dicionário
Listas são um conjunto de elementos ordenados, já os dicionários são listas não ordenadas organizadas em chave-valor

## Diferença entre NoSQL e SQL
SQL é um banco de dados relacional, utilizando estruturas de tabelas. NoSQL é um banco não relacional, ou seja não utiliza estruturas de tabela tradicionais

| Método | Caminho | O que envio | Sucesso | Erros possíveis |
| --- | --- | --- | --- | ---|
| POST| /contatos/|nome, telefone, email|201 + usuário criado| 409 - Email repetido|
|GET | /contatos/ | None | 200 | ---|
|GET | /contatos/{id} | id | 200 | 404 - id não encontrado|
|DELETE |/contato/{id}/| id |204| 404 - id não encontrado|
|PATCH| /contatos/{id}/|id, telefone,email| 201 + usuário alterado | 409 - Email repetido |
