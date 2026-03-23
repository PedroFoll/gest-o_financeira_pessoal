---
name: exemplo-skill
description: "Skill de exemplo. Use para entender como criar suas próprias skills com workflows, scripts e recursos empacotados."
argument-hint: "Descreva o que você quer fazer"
---
# Skill de Exemplo

Esta skill demonstra a estrutura básica de uma skill para GitHub Copilot.

## Quando usar

- Entender a estrutura de uma skill.
- Como base para criar novas skills especializadas.

## Procedimento

1. Leia os requisitos da tarefa fornecida pelo usuário.
2. Consulte os recursos em `./references/` se necessário.
3. Execute o script em `./scripts/` se aplicável.
4. Retorne o resultado em formato claro e organizado.

## Estrutura da pasta

```
exemplo-skill/
├── SKILL.md          ← Este arquivo (instruções principais)
├── scripts/          ← Scripts executáveis
├── references/       ← Documentação de referência
└── assets/           ← Templates e boilerplates
```

## Como criar sua própria skill

1. Crie uma pasta em `.github/skills/<nome-da-skill>/`.
2. Crie o arquivo `SKILL.md` com o frontmatter obrigatório (`name` deve coincidir com o nome da pasta).
3. Adicione subpastas conforme necessário (`scripts/`, `references/`, `assets/`).
4. Use caminhos relativos (`./`) para referenciar recursos da skill.
