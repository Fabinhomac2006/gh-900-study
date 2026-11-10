"""Resumo dos domínios do GH-900 (GitHub Foundations).

Material autoral para estudo. Para a lista oficial e atual de habilidades
avaliadas, consulte o guia de estudo da Microsoft Learn.
"""

OFFICIAL_STUDY_GUIDE = "https://learn.microsoft.com/credentials/certifications/resources/study-guides/gh-900"

TOPICS = [
    {
        "slug": "git-e-github",
        "title": "Introdução ao Git e ao GitHub",
        "icon": "🌱",
        "summary": "Conceitos de controle de versão, o fluxo básico do Git e as ofertas do GitHub.",
        "sections": [
            {
                "heading": "Git x GitHub",
                "points": [
                    "**Git** é um sistema de controle de versão **distribuído**: cada clone tem o histórico completo.",
                    "**GitHub** é a plataforma que hospeda repositórios Git e adiciona colaboração (issues, pull requests, Actions, segurança etc.).",
                    "Um **commit** é um instantâneo do projeto; **branches** permitem trabalhar em paralelo sem afetar a linha principal.",
                ],
            },
            {
                "heading": "Comandos essenciais",
                "points": [
                    "`git init` cria um repositório; `git clone` copia um repositório remoto (com histórico).",
                    "`git add` move alterações para a **staging area**; `git commit` grava o instantâneo; `git push` envia commits ao remoto.",
                    "`git fetch` baixa novidades **sem mesclar**; `git pull` = fetch + merge (ou rebase).",
                    "`git status`, `git log` e `git diff` inspecionam o estado, o histórico e as diferenças.",
                    "`git branch`, `git switch`/`git checkout` e `git merge` gerenciam branches.",
                ],
            },
            {
                "heading": "GitHub flow",
                "points": [
                    "Fluxo leve baseado em branches: **criar branch → commitar → abrir pull request → revisar → mesclar → apagar a branch**.",
                    "A branch padrão (geralmente `main`) deve permanecer sempre em estado implantável.",
                ],
            },
            {
                "heading": "Planos e formas de uso",
                "points": [
                    "Planos: **Free**, **Team** e **Enterprise**; empresas podem usar GitHub Enterprise Cloud (hospedado) ou GitHub Enterprise Server (autogerenciado).",
                    "Interfaces: web, **GitHub Desktop**, **GitHub CLI** (`gh`), editor web (`github.dev`), extensões de IDE e GitHub Mobile.",
                ],
            },
        ],
        "links": [
            ("Hello World (GitHub Docs)", "https://docs.github.com/get-started/start-your-journey/hello-world"),
            ("GitHub flow", "https://docs.github.com/get-started/using-github/github-flow"),
            ("Planos do GitHub", "https://docs.github.com/get-started/learning-about-github/githubs-plans"),
        ],
    },
    {
        "slug": "repositorios",
        "title": "Trabalhando com repositórios",
        "icon": "📦",
        "summary": "Visibilidade, arquivos de saúde da comunidade, forks, releases e outros recursos do repositório.",
        "sections": [
            {
                "heading": "Visibilidade",
                "points": [
                    "**Public**: qualquer pessoa vê. **Private**: apenas quem recebeu acesso.",
                    "**Internal**: visível a todos os membros da **empresa (enterprise)**; disponível só em contas Enterprise.",
                ],
            },
            {
                "heading": "Arquivos importantes",
                "points": [
                    "`README.md` apresenta o projeto; `LICENSE` define os termos de uso; `.gitignore` lista o que o Git não deve rastrear.",
                    "`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` e `SECURITY.md` são **community health files**.",
                    "Um repositório chamado **`.github`** (na conta ou organização) fornece versões padrão desses arquivos e templates a repositórios sem os seus.",
                    "**Profile README**: repositório público com o mesmo nome do seu usuário e um `README.md`.",
                ],
            },
            {
                "heading": "Fork, clone e outros recursos",
                "points": [
                    "**Fork** é uma cópia do repositório na **sua conta no GitHub**, mantendo vínculo com o original (upstream); usado para contribuir sem acesso de escrita.",
                    "**Clone** é uma cópia **local** do repositório.",
                    "**Releases** são baseadas em **tags** do Git e podem anexar binários e notas de versão.",
                    "**Arquivar** um repositório o torna somente leitura; ele pode ser desarquivado depois.",
                    "**Wikis**, **GitHub Pages**, **Gists** (trechos de código) e **Packages** complementam o repositório.",
                ],
            },
        ],
        "links": [
            ("Sobre repositórios", "https://docs.github.com/repositories/creating-and-managing-repositories/about-repositories"),
            ("Arquivo de saúde da comunidade padrão", "https://docs.github.com/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file"),
            ("Sobre releases", "https://docs.github.com/repositories/releasing-projects-on-github/about-releases"),
        ],
    },
    {
        "slug": "colaboracao",
        "title": "Recursos de colaboração",
        "icon": "🤝",
        "summary": "Issues, pull requests, revisões, CODEOWNERS, proteção de branches e Discussions.",
        "sections": [
            {
                "heading": "Issues e Discussions",
                "points": [
                    "**Issues** rastreiam tarefas, bugs e ideias; aceitam labels, assignees, milestones e projects.",
                    "**Issue templates** ficam em `.github/ISSUE_TEMPLATE/` (Markdown ou formulários YAML).",
                    "**Discussions** servem a conversas abertas, perguntas e respostas e anúncios, sem virar tarefa.",
                    "Palavras-chave como `closes #42` / `fixes #42` na descrição de um PR fecham a issue quando o PR é mesclado na branch padrão.",
                ],
            },
            {
                "heading": "Pull requests",
                "points": [
                    "Um **pull request (PR)** propõe mesclar uma branch em outra e concentra discussão, revisão e checagens.",
                    "**Draft PR** sinaliza trabalho em andamento; não pode ser mesclado até ser marcado como pronto.",
                    "Revisões podem ser **Comment**, **Approve** ou **Request changes**.",
                    "Estratégias de merge: **merge commit**, **squash and merge** (um único commit) e **rebase and merge** (histórico linear).",
                    "Conflitos de merge ocorrem quando as mesmas linhas foram alteradas em ambas as branches e precisam de resolução manual.",
                ],
            },
            {
                "heading": "Governança",
                "points": [
                    "**CODEOWNERS** (em `.github/`, raiz ou `docs/`) define responsáveis por caminhos e solicita sua revisão automaticamente.",
                    "**Branch protection rules** e **rulesets** podem exigir revisões, checagens de status, histórico linear e bloquear force push.",
                    "**Merge queue** serializa merges para garantir que a branch continue passando nos testes.",
                    "`@menções` notificam pessoas e times; as **notificações** podem ser ajustadas por repositório.",
                ],
            },
        ],
        "links": [
            ("Sobre pull requests", "https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests"),
            ("Sobre CODEOWNERS", "https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners"),
            ("Branches protegidas", "https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches"),
        ],
    },
    {
        "slug": "desenvolvimento-moderno",
        "title": "Desenvolvimento moderno",
        "icon": "⚙️",
        "summary": "GitHub Actions, Codespaces, Copilot, Packages e Pages.",
        "sections": [
            {
                "heading": "GitHub Actions",
                "points": [
                    "Automação de CI/CD definida em arquivos **YAML** em `.github/workflows/`.",
                    "Hierarquia: **workflow → jobs → steps**. Jobs rodam em **runners**; steps executam comandos ou **actions** reutilizáveis (Marketplace).",
                    "Eventos disparadores: `push`, `pull_request`, `schedule` (cron), `workflow_dispatch` (manual), entre outros.",
                    "Runners **GitHub-hosted** (Ubuntu, Windows, macOS) ou **self-hosted** (sua infraestrutura).",
                    "Credenciais ficam em **secrets** (repositório, ambiente ou organização), nunca no YAML.",
                ],
            },
            {
                "heading": "Ambientes e IA",
                "points": [
                    "**Codespaces**: ambiente de desenvolvimento na nuvem, configurável com `devcontainer.json`.",
                    "**GitHub Copilot**: assistente de IA com sugestões de código, chat e modo agente; disponível em planos Free, Pro, Business e Enterprise.",
                    "O desenvolvedor continua responsável por revisar o código sugerido.",
                ],
            },
            {
                "heading": "Publicação",
                "points": [
                    "**GitHub Pages** publica sites **estáticos** diretamente de um repositório.",
                    "**GitHub Packages** hospeda pacotes (npm, Maven, NuGet, RubyGems, contêineres etc.) junto ao código.",
                ],
            },
        ],
        "links": [
            ("Entendendo o GitHub Actions", "https://docs.github.com/actions/get-started/understand-github-actions"),
            ("Sobre Codespaces", "https://docs.github.com/codespaces/about-codespaces/what-are-codespaces"),
            ("Sobre GitHub Copilot", "https://docs.github.com/copilot/about-github-copilot/what-is-github-copilot"),
        ],
    },
    {
        "slug": "gerenciamento-de-projetos",
        "title": "Gerenciamento de projetos",
        "icon": "🗂️",
        "summary": "GitHub Projects, milestones, labels e acompanhamento do trabalho.",
        "sections": [
            {
                "heading": "GitHub Projects",
                "points": [
                    "Ferramenta flexível para planejar e acompanhar trabalho com issues, pull requests e **draft issues**.",
                    "Três layouts: **Table** (planilha), **Board** (kanban) e **Roadmap** (linha do tempo).",
                    "Suporta **campos personalizados** (texto, número, data, seleção única, iteração) e **visões** salvas com filtros, agrupamento e ordenação.",
                    "**Automações** embutidas: por exemplo, adicionar itens automaticamente ou mudar o status ao fechar uma issue.",
                ],
            },
            {
                "heading": "Organização do trabalho",
                "points": [
                    "**Labels** categorizam issues e PRs (bug, documentation, good first issue...).",
                    "**Milestones** agrupam issues e PRs em torno de um objetivo com data limite e barra de progresso.",
                    "**Task lists** e **sub-issues** quebram um trabalho grande em partes rastreáveis.",
                    "**Assignees** indicam responsáveis; **issue forms** padronizam o que é informado ao abrir uma issue.",
                ],
            },
        ],
        "links": [
            ("Sobre Projects", "https://docs.github.com/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects"),
            ("Sobre milestones", "https://docs.github.com/issues/using-labels-and-milestones-to-track-work/about-milestones"),
            ("Gerenciando labels", "https://docs.github.com/issues/using-labels-and-milestones-to-track-work/managing-labels"),
        ],
    },
    {
        "slug": "seguranca-e-administracao",
        "title": "Privacidade, segurança e administração",
        "icon": "🔐",
        "summary": "Autenticação, funções de acesso, Dependabot, secret scanning, code scanning e governança.",
        "sections": [
            {
                "heading": "Autenticação",
                "points": [
                    "**2FA** (autenticação em dois fatores) protege a conta; **passkeys**, apps autenticadores e chaves de segurança são opções.",
                    "**SSH keys** e **personal access tokens (PAT)** autenticam operações Git/API; prefira **fine-grained PATs** com o menor escopo possível.",
                    "**SAML SSO** integra o login ao provedor de identidade da organização.",
                ],
            },
            {
                "heading": "Funções em repositórios de organização",
                "points": [
                    "Da menor para a maior permissão: **Read → Triage → Write → Maintain → Admin**.",
                    "**Triage** gerencia issues e PRs sem acesso de escrita ao código; **Write** pode fazer push; **Maintain** gerencia o repositório sem ações sensíveis; **Admin** tem controle total.",
                    "**Teams** agrupam membros para conceder permissões em lote; **owners** administram a organização.",
                ],
            },
            {
                "heading": "Recursos de segurança",
                "points": [
                    "**Dependency graph**: mostra as dependências do projeto.",
                    "**Dependabot alerts** avisam sobre dependências vulneráveis; **security updates** abrem PRs de correção; **version updates** (configurados em `.github/dependabot.yml`) mantêm dependências atualizadas.",
                    "**Secret scanning** detecta credenciais expostas; **push protection** bloqueia o push que as contém.",
                    "**Code scanning** (ex.: **CodeQL**) encontra vulnerabilidades no código.",
                    "`SECURITY.md` orienta como relatar vulnerabilidades; **security advisories** e **private vulnerability reporting** permitem tratá-las de forma privada.",
                    "Os recursos de segurança avançada são oferecidos como **GitHub Secret Protection** e **GitHub Code Security** (antes agrupados como GitHub Advanced Security).",
                ],
            },
            {
                "heading": "Administração",
                "points": [
                    "O **audit log** registra ações na organização/empresa.",
                    "**Enterprise accounts** centralizam políticas e faturamento de várias organizações.",
                    "**Enterprise Managed Users (EMU)** são contas controladas pelo provedor de identidade da empresa.",
                ],
            },
        ],
        "links": [
            ("Funções de repositório em organizações", "https://docs.github.com/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization"),
            ("Sobre os alertas do Dependabot", "https://docs.github.com/code-security/dependabot/dependabot-alerts/about-dependabot-alerts"),
            ("Sobre secret scanning", "https://docs.github.com/code-security/secret-scanning/introduction/about-secret-scanning"),
        ],
    },
    {
        "slug": "comunidade",
        "title": "Benefícios da comunidade GitHub",
        "icon": "🌍",
        "summary": "Open source, licenças, stars, forks, Sponsors, Skills e inner source.",
        "sections": [
            {
                "heading": "Open source",
                "points": [
                    "Sem uma **licença**, o código segue sob copyright padrão e outras pessoas **não** têm permissão para reutilizá-lo.",
                    "Licenças comuns: **MIT** e **Apache 2.0** (permissivas) e **GPL** (copyleft).",
                    "`CONTRIBUTING.md` explica como contribuir; `CODE_OF_CONDUCT.md` define o comportamento esperado.",
                    "**Good first issue** e **help wanted** são labels que ajudam novos colaboradores.",
                ],
            },
            {
                "heading": "Interação",
                "points": [
                    "**Star** marca um repositório como favorito/reconhece o projeto; **Watch** controla as notificações; **Follow** acompanha pessoas.",
                    "**GitHub Sponsors** permite financiar desenvolvedores e projetos open source.",
                    "**Discussions** e **GitHub Community** facilitam perguntas, ajuda e troca de ideias.",
                    "**Inner source** aplica práticas de open source dentro da empresa.",
                ],
            },
            {
                "heading": "Aprendizado",
                "points": [
                    "**GitHub Skills** oferece cursos interativos executados em repositórios com Actions.",
                    "**GitHub Docs** é a fonte oficial de documentação; o **Marketplace** reúne actions e apps.",
                ],
            },
        ],
        "links": [
            ("GitHub Skills", "https://skills.github.com/"),
            ("Guias de código aberto", "https://opensource.guide/"),
            ("Sobre GitHub Sponsors", "https://docs.github.com/sponsors/getting-started-with-github-sponsors/about-github-sponsors"),
        ],
    },
]

TOPICS_BY_SLUG = {topic["slug"]: topic for topic in TOPICS}
