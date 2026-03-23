# Andromeda — Controle Financeiro Pessoal

Aplicação web para gestão de finanças pessoais: cadastro de receitas, despesas, lançamentos recorrentes e dashboard com resumo mensal.

---

## Funcionalidades

- **Dashboard** — saldo do mês, total de receitas e despesas, gráfico dos últimos 6 meses e últimos lançamentos
- **Lançamentos** — CRUD completo com filtros por tipo, categoria e período
- **Lançamentos Recorrentes** — configure salários, aluguéis e assinaturas; os lançamentos são gerados automaticamente ao acessar a listagem
- **Categorias** — CRUD com cor personalizada e ícone Bootstrap Icons

---

## Stack

| Tecnologia | Versão |
|---|---|
| Python | 3.12+ |
| Django | 6.0.3 |
| Bootstrap | 5.3.3 (CDN) |
| Bootstrap Icons | 1.11.3 (CDN) |
| SQLite | (padrão, WAL mode) |
| Whitenoise | 6.12.0 |
| python-decouple | 3.8 |

---

## Estrutura do Projeto

```
.
├── config/               # Configurações Django (settings, urls, wsgi, asgi)
├── pages/
│   ├── home/             # Dashboard
│   ├── categorias/       # CRUD de categorias
│   └── lancamentos/      # CRUD de lançamentos e recorrentes
├── templates/
│   ├── base.html         # Layout raiz
│   └── partials/         # Componentes: sidebar, header, footer (cada um com CSS/JS próprio)
├── static/               # CSS e JS globais
├── db.sqlite3
├── manage.py
└── requirements.txt
```

### Arquitetura por app

Cada app em `pages/` segue a arquitetura em camadas:

```
View → Service → Repository → Model (ORM)
```

| Arquivo | Responsabilidade |
|---|---|
| `models.py` | Definição das entidades e campos |
| `repositories.py` | Acesso ao banco via ORM |
| `services.py` | Regras de negócio |
| `views.py` | Coordena request/response, delega ao service |
| `forms.py` | Validação de entrada (ModelForm) |

---

## Instalação e Execução

### Pré-requisitos

- Python 3.12+
- Git

### Passos

```powershell
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd <pasta>

# 2. Criar e ativar o virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar o arquivo de variáveis de ambiente
# Crie um arquivo .env na raiz com o conteúdo abaixo
```

**Conteúdo do `.env`:**

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

```powershell
# 5. Aplicar as migrações
python manage.py migrate

# 6. (Opcional) Criar superusuário para acessar o admin
python manage.py createsuperuser

# 7. Iniciar o servidor de desenvolvimento
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## URLs disponíveis

| URL | Descrição |
|---|---|
| `/` | Dashboard |
| `/lancamentos/` | Lista de lançamentos |
| `/lancamentos/novo/` | Criar lançamento |
| `/lancamentos/recorrentes/` | Lista de recorrentes |
| `/categorias/` | Lista de categorias |
| `/admin/` | Django Admin |

---

## Modelos de Dados

### `Categoria`

| Campo | Tipo | Descrição |
|---|---|---|
| `nome` | CharField(100) | Nome da categoria |
| `cor` | CharField(7) | Cor hexadecimal (ex: `#FF66B2`) |
| `icone` | CharField(50) | Classe Bootstrap Icons (ex: `bi-tag`) |
| `ativo` | BooleanField | Se a categoria está ativa |

### `Lancamento`

| Campo | Tipo | Descrição |
|---|---|---|
| `descricao` | CharField(200) | Descrição do lançamento |
| `valor` | DecimalField(12,2) | Valor monetário |
| `tipo` | choices | `RECEITA` ou `DESPESA` |
| `data` | DateField | Data do lançamento |
| `categoria` | FK → Categoria | Categoria associada (opcional) |
| `observacao` | TextField | Observação livre |
| `recorrente` | FK → LancamentoRecorrente | Origem recorrente (se houver) |

### `LancamentoRecorrente`

| Campo | Tipo | Descrição |
|---|---|---|
| `descricao` | CharField(200) | Descrição |
| `valor` | DecimalField(12,2) | Valor |
| `tipo` | choices | `RECEITA` ou `DESPESA` |
| `frequencia` | choices | `SEMANAL`, `QUINZENAL`, `MENSAL` ou `ANUAL` |
| `dia_vencimento` | IntegerField(1–28) | Dia do mês para geração |
| `data_inicio` | DateField | Início da recorrência |
| `data_fim` | DateField | Fim da recorrência (opcional) |
| `categoria` | FK → Categoria | Categoria (opcional) |
| `ativo` | BooleanField | Se está ativo |

---

## Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|---|---|---|
| `SECRET_KEY` | Chave secreta do Django | `django-insecure-...` |
| `DEBUG` | Modo debug | `True` / `False` |
| `ALLOWED_HOSTS` | Hosts permitidos | `127.0.0.1,localhost` |
