# Pokémon API – Treinadores e Pokémons

Projeto desenvolvido para a disciplina de **Projeto de Cloud** (AP1), com **Django REST Framework** e deploy na **AWS Elastic Beanstalk**.

## Tema

O tema é o mundo Pokémon. A API permite cadastrar **treinadores** e os **pokémons** que pertencem a cada um deles.

## API publicada (AWS Elastic Beanstalk)

- **API:** http://pokemonbm-env.eba-bmr2eiwv.us-east-1.elasticbeanstalk.com/api/
- **Treinadores:** http://pokemonbm-env.eba-bmr2eiwv.us-east-1.elasticbeanstalk.com/api/treinadores/
- **Pokémons:** http://pokemonbm-env.eba-bmr2eiwv.us-east-1.elasticbeanstalk.com/api/pokemons/
- **Django Admin:** http://pokemonbm-env.eba-bmr2eiwv.us-east-1.elasticbeanstalk.com/admin/

### Acesso ao Django Admin

| Campo   | Valor    |
|---------|----------|
| Usuário | `admin`  |
| Senha   | `123456` |

O superusuário é criado automaticamente durante o deploy (veja a seção de deploy).

## Estrutura do projeto

- **Projeto Django:** `pokemon`
- **App:** `treinadores` (contém as duas classes)

```
DeployEB/
├── .ebextensions/
│   ├── detection.config
│   └── django.config
├── pokemon/              # projeto Django (settings, urls, wsgi)
├── treinadores/          # app com models, serializers, views, urls e admin
├── manage.py
├── Procfile
├── requirements.txt
└── app.zip               # pacote usado no deploy
```

## Classes desenvolvidas

### Treinador

| Campo           | Tipo                    |
|-----------------|-------------------------|
| `nome`          | texto (até 100)         |
| `cidade_origem` | texto (até 100)         |
| `idade`         | inteiro positivo        |

### Pokemon

| Campo       | Tipo                                   |
|-------------|----------------------------------------|
| `nome`      | texto (até 100)                        |
| `tipo`      | texto (até 50)                         |
| `nivel`     | inteiro positivo                       |
| `treinador` | chave estrangeira (`ForeignKey`) para `Treinador` |

### Relacionamento

Um **Treinador** pode ter vários **Pokémons** (1 para N). Ao cadastrar um pokémon, é necessário escolher o treinador dono dele. Ao apagar um treinador, seus pokémons também são apagados (`on_delete=CASCADE`).

## Endpoints da API

| Método                    | Endpoint                | Descrição                       |
|---------------------------|-------------------------|---------------------------------|
| GET, POST                 | `/api/treinadores/`     | Lista e cadastra treinadores    |
| GET, PUT, PATCH, DELETE   | `/api/treinadores/{id}/`| Consulta, altera e remove       |
| GET, POST                 | `/api/pokemons/`        | Lista e cadastra pokémons       |
| GET, PUT, PATCH, DELETE   | `/api/pokemons/{id}/`   | Consulta, altera e remove       |

### Exemplo de treinador

```json
{
  "nome": "Ash",
  "cidade_origem": "Pallet",
  "idade": 10
}
```

### Exemplo de pokémon

```json
{
  "nome": "Pikachu",
  "tipo": "Elétrico",
  "nivel": 50,
  "treinador": 1
}
```

## Como executar localmente

Pré-requisito: Python 3 instalado.

1. Clone o repositório e entre na pasta do projeto (a que contém o `manage.py`):
   ```
   git clone <URL-DO-REPOSITORIO>
   cd <PASTA-DO-PROJETO>
   ```
2. Crie e ative o ambiente virtual (Windows):
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Crie as tabelas do banco (SQLite):
   ```
   python manage.py migrate
   ```
5. Crie o superusuário para acessar o Django Admin:
   ```
   python manage.py createsuperuser
   ```
6. Inicie o servidor:
   ```
   python manage.py runserver
   ```
7. Acesse no navegador:
   - API: http://127.0.0.1:8000/api/
   - Admin: http://127.0.0.1:8000/admin/

## Alterações realizadas

- Removidos o app `produtos`, a classe `Produto` e a pasta `media/produtos`.
- Projeto Django renomeado de `catalogo` para `pokemon`, para ficar no contexto do tema. Foram atualizados `manage.py`, `settings.py`, `wsgi.py`, `asgi.py` e o `Procfile`.
- Criado o app `treinadores` com as classes `Treinador` e `Pokemon` e o relacionamento entre elas.
- Criados `serializers.py`, `views.py` (com `ModelViewSet`) e `urls.py` (com `DefaultRouter`), além do registro dos models no `admin.py`.
- `settings.py`: adicionados `rest_framework` e `treinadores` em `INSTALLED_APPS`, e configurados `ALLOWED_HOSTS` e `STATIC_ROOT`.
- Banco de dados: SQLite.
- Configurado o `.ebextensions/django.config` para o deploy, incluindo a criação do superusuário.

## Deploy na AWS Elastic Beanstalk

### 1. Preparar o `app.zip`

O `manage.py` precisa ficar na **raiz** do zip. O pacote não inclui `.venv`, `__pycache__` nem o `db.sqlite3` local. Na pasta do projeto:

```
tar -a -c -f app.zip --exclude=.venv --exclude=__pycache__ --exclude=db.sqlite3 .ebextensions pokemon treinadores manage.py Procfile requirements.txt
```

Conteúdo conferido com `tar -tf app.zip`.

### 2. Arquivos de configuração

**Procfile**
```
web: gunicorn pokemon.wsgi:application --bind 127.0.0.1:8000
```

**`.ebextensions/django.config`**: define o `WSGIPath` (`pokemon/wsgi.py`), o `DJANGO_SETTINGS_MODULE` (`pokemon.settings`), a pasta de arquivos estáticos e os comandos executados a cada deploy:

- `migrate`: cria as tabelas no banco
- `collectstatic`: reúne os arquivos estáticos (necessário para o Django Admin)
- ajuste de permissões do `db.sqlite3` e da pasta do projeto
- `createsuperuser --noinput`: cria o usuário `admin` a partir das variáveis `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` e `DJANGO_SUPERUSER_PASSWORD`. O `|| true` evita falha em novos deploys, quando o usuário já existe.

### 3. Criação do ambiente no console da AWS

1. Acessar o serviço **Elastic Beanstalk** e clicar em **Create application**.
2. Escolher **Web server environment** e dar o nome à aplicação (`pokemon_BM`).
3. Em **Platform**, escolher **Python 3.12** (Amazon Linux 2023).
4. Em **Application code**, escolher **Upload your code** e enviar o `app.zip`.
5. Escolher o preset **Single instance** e concluir com **Submit**.
6. Aguardar o ambiente `PokemonBM-env` ficar com a integridade **Ok**.

### 4. Verificação

Após o deploy, foram testados no ambiente publicado:

- `/api/` listando os endpoints `treinadores` e `pokemons`
- cadastro e listagem de treinadores e pokémons, com o relacionamento funcionando
- login no `/admin/` com o superusuário criado no deploy

## Tecnologias

- Python 3.12
- Django
- Django REST Framework
- Gunicorn
- SQLite
- AWS Elastic Beanstalk
