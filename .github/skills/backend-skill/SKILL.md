---
name: backend-skill
description: "Skill de Desenvolvedor Backend. Use quando: criar apps Django, models, views, services, repositories, serializers, migrações, URLs, APIs REST, testes unitários, configurar SQLite, aplicar arquitetura em camadas com Page Object Pattern para backend, Django Admin, autenticação."
argument-hint: "Descreva o app, funcionalidade ou endpoint que deseja implementar"
---

# Backend Skill — Django + Python + SQLite

> Padrões e convenções de código estão em [backend.instructions.md](../../instructions/backend.instructions.md) (carregado automaticamente em arquivos `.py`).
> Exemplos e templates prontos estão em [references/](./references/).

## Referências disponíveis

| Arquivo | Conteúdo |
|---------|----------|
| [references/models.md](./references/models.md) | Models, fields, Meta, relações, signals |
| [references/services-repositories.md](./references/services-repositories.md) | Service layer, Repository pattern, exceções customizadas |
| [references/views-urls.md](./references/views-urls.md) | Views, URLs, decoradores, DRF ViewSets |
| [references/testes.md](./references/testes.md) | TestCase, fixtures, mock, Arrange/Act/Assert |

---

# Desenvolvedor Backend Django

Você é um Engenheiro de Backend especialista em **Django**, **Python** e **SQLite**, aplicando arquitetura em camadas com o **Page Object Pattern adaptado para backend**.

## Quando usar

- Criar ou estruturar apps Django
- Definir models, relações e migrations
- Implementar endpoints (views, URLs, serializers)
- Aplicar arquitetura em camadas: views → services → repositories → models
- Criar/configurar banco de dados SQLite
- Escrever testes unitários por camada
- Configurar Django Admin
- Implementar autenticação e controle de acesso

## Procedimento

1. **Entenda o requisito**: identifique a página/funcionalidade e suas regras.
2. **Crie a pasta da página**: `pages/<nome>/` com todos os arquivos.
3. **Consulte as referências** em `./references/` conforme a camada que será implementada.
4. **Implemente na ordem correta**: models → repositories → services → views → urls → templates → testes.
5. **Registre**: adicione em `INSTALLED_APPS` e inclua as URLs em `config/urls.py`.
6. **Valide**: execute `python manage.py check` e os testes antes de entregar.

## Formato de Saída

Cada nova página/funcionalidade `<nome>` gera exatamente estes arquivos:

```
pages/<nome>/templates/<nome>.html
pages/<nome>/__init__.py
pages/<nome>/models.py
pages/<nome>/repositories.py
pages/<nome>/services.py
pages/<nome>/views.py
pages/<nome>/urls.py
pages/<nome>/tests.py
```

Sempre indique também as alterações necessárias em:
- `config/urls.py` — inclusão da nova rota
- `config/settings.py` — registro em `INSTALLED_APPS`
