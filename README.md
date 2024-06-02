# acr-cpp-member-order

Arquivo config.json

- comment
    - Comentario que sera adicionado
        - Possui variaveis dinamicas, ORDERED_ATTRS e PATH
- ignoreList
    - Lista de regex referentes atributos que devem ser ignorados, ou seja, ira manter na ordem que estiver
- orderList
    - List de lista de regex, referente a ordem de atributos
    - Deve atender todos os regex de uma posicao, para ficar naquela posicao

```json
{
    "stage": "static",
    "comment": "${ORDERED_ATTRS} - ${PATH}",
    "ignoreList": [],
    "orderList": [
        []
    ]
}
```
