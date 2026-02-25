### v1.0

# Plano completo — Testes backend FastAPI

## Objetivo

Adicionar uma suíte de testes automatizados para o backend FastAPI do projeto, cobrindo endpoints principais (`/activities`, signup, remoção de participantes e redirect `/`). Os testes devem ser confiáveis, isolados e fáceis de executar localmente e em CI.

## Escopo

- Testes focados apenas no backend (API em `src/app.py`).
- Uso do padrão AAA (Arrange-Act-Assert) em todos os testes.
- Testes síncronos usando `fastapi.testclient.TestClient` e `pytest`.

## Tarefas

1. Atualizar dependências
   - Adicionar `pytest` e `requests` em `requirements.txt`.

2. Preparar fixture de teste
   - Criar `tests/conftest.py` com fixture `client` que fornece `TestClient(app)`.
   - Isolar estado global `activities`: snapshot por `deepcopy` antes do teste e restauração após (para evitar efeitos colaterais entre testes).

3. Escrever testes (AAA)
   - `tests/test_activities_api.py`:
     - `test_get_activities_returns_known_activity`
     - `test_signup_for_activity_success`
     - `test_signup_duplicate_returns_400`
     - `test_signup_nonexistent_activity_returns_404`
     - `test_remove_participant_success`
     - `test_remove_nonexistent_participant_returns_404`
     - `test_remove_nonexistent_activity_returns_404`
   - `tests/test_root_redirect.py`:
     - `test_root_redirects_to_static_index`

4. Convenções e estilo
   - Cada teste deve seguir claramente Arrange / Act / Assert com comentários.
   - Manter testes curtos e determinísticos.

5. Execução de testes
   - Instalar dependências: `pip install -r requirements.txt`.
   - Rodar: `pytest -q`.

6. Integração contínua (opcional)
   - Adicionar job no CI para executar `pytest` (por exemplo GitHub Actions).

## Arquivos a criar/modificar

- `requirements.txt` — adicionar `pytest` e `requests`.
- `tests/conftest.py` — fixture `client` com snapshot/restore de `activities`.
- `tests/test_activities_api.py` — testes AAA para endpoints principais.
- `tests/test_root_redirect.py` — teste para redirect da raiz.

## Isolamento de estado

Porque `activities` é um dicionário em memória no módulo `src.app`, os testes devem garantir isolamento:

- Antes de cada teste: copiar o estado com `copy.deepcopy(app_module.activities)`.
- Após cada teste: restaurar o estado original.

Alternativas (menos preferidas): endpoint de reset para testes ou recarregar módulo.

## Critérios de aceitação

- Todos os testes passam (`pytest -q`).
- Testes são independentes e repetíveis em qualquer ordem.
- Código de produção não precisa ser modificado apenas para habilitar testes (fixture faz isolamento).

## Comandos úteis

```bash
pip install -r requirements.txt
pytest -q
```

## Próximos passos (opcionais)

- Adicionar testes para a camada front-end (end-to-end) usando `playwright` ou `selenium`.
- Refatorar `activities` para uma camada injetável (dependência) para facilitar testes futuros.

---

Arquivo gerado automaticamente: `planos/PLANO.md` — descreve o plano completo para os testes backend.
