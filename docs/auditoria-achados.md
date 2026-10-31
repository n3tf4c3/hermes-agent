# Ledger de auditoria técnica

Numeração deste repositório. Criado em 21/10/2026 após verificar ausência de ledger e de IDs `achado N` no histórico pesquisado. Relatório externo: `C:\Codes\relatorios\hermes-agent\auditoria-2026-10-21.md`. Snapshot: `4db18eab4036c5c320f8f48e6c29b58b9ed637ff`.

| ID | Severidade | Status | Causa / evidência | Resolução |
|---|---|---|---|---|
| #1 | Alta | RESOLVIDO (23/10/2026) | Pillow 12.3.0 afetado; transcode TIFF em `agent/image_routing.py:438–464`, pin `pyproject.toml:173` | Sincronização com o upstream: `Pillow==13.0.0` (pin e override do lock) |
| #2 | Alta | RESOLVIDO (23/10/2026) | certifi 2026.5.20 inclui raiz afetada; `pyproject.toml:41`, GHSA-6q48-6c7w-9gw2 | Sincronização com o upstream: `certifi==2026.10.19` |
| #3 | Média | RESOLVIDO (23/10/2026) | aiohttp 3.14.3 sem correção de timeout inicial; `gateway/platforms/api_server.py:4466–4470`, GHSA-5wr8-gcqf-gqf3 | Sincronização com o upstream: `aiohttp==3.14.5` em todos os extras |
| #4 | Média | RESOLVIDO com risco residual aceito (23/10/2026) | Locks JS com advisories no desktop/tooling/site/Photon; alcance contextual detalhado no relatório | Raiz + workspaces e sidecar Photon: `npm audit` zerado (electron 44.9.3, simple-git 4.0.2, shell-quote 1.12.0). Residual: `website/` tem 30 entradas com uma única causa, `braces` 3.0.3 (GHSA-vfj7-8cjw-p6xm, DoS por padrão aninhado), sem versão corrigida publicada; uso só no build do site estático, com padrões da própria configuração. Reavaliar quando houver correção |
| #5 | Média | RESOLVIDO (23/10/2026) | `git-review-ops.ts:479–491` retorna sucesso após rejeição de checkout e clean; reproduzido com dependências simuladas | `reviewRevert` classifica pelo `git diff HEAD`, usa `git restore --staged --worktree` (também descarta adição staged), para na primeira falha e rejeita dizendo se algo já foi descartado; a store re-sincroniza a lista mesmo com falha. Testes com repositório real e com git simulado, vermelhos no código anterior |

## Decisões da rodada

Capacidade intencional de executar ferramentas/terminal não é falha de isolamento por si no modelo single-tenant. Não duplicar alertas como exploração confirmada sem verificar pré-condições: DOMPurify `IN_PLACE`, Electron popup, MCP servidor versus cliente. `_check_auth` sem chave em wiring de testes é protegido pelo startup real. Detalhes e limitações constam no relatório.

## Resolução de 23/10/2026

#1–#3 e a maior parte do #4 vieram da sincronização do fork com `upstream/main` (`67491b50f7e`), em vez de pins locais, para não divergir do upstream. Nos conflitos, `pyproject.toml`/`uv.lock` seguiram o upstream, que já trazia os pisos de PyJWT/urllib3 do fork, e o bloco `constraint-dependencies` do fork foi mantido; `python -m pm.build_env --source . --check-lock` passou. Varredura OSV do `uv.lock` resultante: 324 pacotes, nenhum advisory (inclui `mcp` 2.3.0, citado no relatório sem virar achado). #5 não tinha correção no upstream e foi corrigido no fork.

Validação: `scripts/check` 12/12 ok contra base `upstream/main` (container Linux descartável); `tests/pm/` com o mesmo conjunto de falhas no fork e no `upstream/main` puro (44 testes em 16 arquivos, ambiente do container), sem falha própria do fork. Desktop: typecheck e lint limpos; testes do `reviewRevert` e da store passam e falham no código anterior. A suíte completa do desktop no Windows (sem binário Electron) teve falhas em 34 arquivos sem relação com a mudança; 30 se repetem no código anterior e as restantes passam isoladas, com e sem a correção. A CI oficial roda essa suíte em Linux.

## Implantação e evidência operacional (23/10/2026)

O deploy real passou para a imagem oficial `nousresearch/hermes-agent:v0.22.5` (digest `sha256:9c5561579f3f…`), que já contém as versões corrigidas de #1–#3 e os pisos de segurança do fork; a camada `deploy/security/` deixou de ser necessária e foi removida, e `deploy/docker-compose.yml` passou a espelhar a imagem por digest e o endurecimento do serviço em produção. Backup cifrado do volume verificado fora do host antes da troca; estado preservado (configuração, sessões, mensagens e integridade dos bancos).

**D5 — PASS com evidência operacional.** Ambiente: produção (servidor próprio), deploy na imagem acima, conferido em 23/10/2026 às 09:00 UTC, por requisições feitas de dentro do container em execução. Provedor de auth do dashboard: variáveis `HERMES_DASHBOARD_BASIC_AUTH_*` presentes no container que executa o código (só nomes conferidos); login por senha 200 e `/api/config` autenticado 200; sem sessão, `/api/config` e `/api/sessions` 401, e bearer inválido 401. API server: plataforma `api_server` conectada, o que só ocorre com chave utilizável (guarda de startup em `gateway/config_env.py::_api_server`). Status geral `ok`, com o gateway e as plataformas de mensagem conectados. Nenhum segredo foi impresso ou registrado.

**#4 residual:** `braces` reconferido em 23/10/2026; 3.0.3 continua a última versão publicada e o GHSA-vfj7-8cjw-p6xm segue sem versão corrigida.

Pendência: a cobertura dinâmica (teste de segurança ativo contra uma instância) não foi executada nesta rodada.


## Rodada transversal 2026-10-30 — 200000

HEAD auditado: `01493e69a38830433a2675947abb578ecf1c2673`. Relatório externo: `C:\Codes\relatorios\hermes-agent\auditoria-2026-10-30-200000.md`. Evidências: `C:\Codes\relatorios\hermes-agent\evidencias-2026-10-30-200000.json`.

Auditoria estática e validações selecionadas; sem correção de código, commit, push ou deploy. Falta de prova operacional não foi convertida em vulnerabilidade presumida.

| ID | Achado | Severidade | Status nesta rodada | Evidência |
|---|---|---|---|---|
| 6 | Decoder Brotli vulnerável pode processar mídia externa | alta | ABERTO | `pyproject.toml:274`; `uv.lock:650`; `gateway/platforms/base.py:524`; `gateway/platforms/base.py:635`; Potencial — versão e caminho confirmados; seleção do codec e exploração não reproduzidas. |
| 4 | Advisories atuais permanecem em extras e bridges | média | PARCIAL | `uv.lock:1781`; `uv.lock:3586`; `pyproject.toml:482`; `pyproject.toml:613`; `package-lock.json:19014`; `scripts/whatsapp-bridge/package-lock.json:881`; Versões com advisory confirmadas; alcance de cada função parcialmente verificado. |
| 7 | Ações de dashboard com cookie não validam CSRF/origem | média | ABERTO | `hermes_cli/dashboard_auth/cookies.py:59`; `hermes_cli/dashboard_auth/middleware.py:160`; `hermes_cli/web_routers/actions.py:160`; `hermes_cli/web_server.py:557`; Potencial — inspeção estática, sem exploração. |

Reverificações e decisões históricas: #1 — Correção Pillow preservada; #2 — Correção certifi preservada; #3 — Constraint aiohttp corrigida preservada; #4 — REABERTO/PARCIAL para advisories atuais; #5 — Correção do revert desktop presente. O relatório detalha alcance/evidência; provas operacionais antigas não foram repetidas.

## Resolução de 31/10/2026

Commits na branch `fix/auditoria-20261031` (base `01493e69a3`): `6db2779b61` (#6 e #4 Python), `d33189fae2` (#4 JS), `64416f43b8` (#7). Sem push nem deploy. Detalhes, decisões e falsificação no adendo do relatório da rodada.

| ID | Status | Resolução | Pendência / condição de fechamento |
|---|---|---|---|
| #6 | PARCIAL (31/10/2026) | `brotlicffi==1.2.1.0` no extra `messaging` e no `uv.lock`, alinhado ao upstream (#145147). Smoke Brotli benigno pelo leitor real do gateway: o httpx seleciona brotlicffi e envia `br`, o que confirma a cadeia | Produção na imagem oficial `v0.22.5` ainda tem 1.2.0.2. Fecha com deploy de imagem com ≥1.2.1.0 (sem release estável do upstream até 31/10) |
| #4 | PARCIAL (31/10/2026) | Python: pyasn1 0.6.5, tornado 6.6, msgpack 1.2.3, filelock 4.2.1, setuptools 84.1.0. JS: undici 6.29.1/7.30.1, zod 4.6.7 (raiz e Photon), fast-uri 3.1.9, body-parser 1.20.9 (bridge WhatsApp). Locks regenerados com uv 0.13.5 e npm 12.0.2 (versões do PM) | follow-redirects 1.16.2 e joi 18.3.1 (só via `wait-on`, dev) bloqueados pelo `min-release-age=14`; reabrir em 08/11 e 11/11. qs 6.16.0 no bridge não alcançável (sem `stringify` com `arrayFormat: 'comma'`). Tooling moderado sem correção não major. `braces` do website como antes |
| #7 | PARCIAL (31/10/2026) | `gated_auth_middleware` recusa (403) escrita com cookie quando `Sec-Fetch-Site` não é `same-origin`/`none`; sem o header, mantém o comportamento (compatível com proxy HTTP, motivo da reversão `22103f58a8` no upstream). Teste vermelho no código anterior | Sem defesa em HTTP comum fora do loopback (navegador não envia Fetch Metadata). Produção (imagem oficial) sem a correção |

Validação (contêineres Linux descartáveis): `scripts/check` 12/12; `--check-lock` ok; `tests/hermes_cli`, `tests/gateway` e `tests/plugins` com os extras afetados: 30901 testes passando e 158 falhando, com 157 iguais no HEAD original (lock e ambiente do HEAD) e 1 de carga que passa isolado nas duas árvores. TUI 1880 testes passando com o undici novo; `npm ci` ok nos três locks.

**Camada de segurança (31/10/2026):** `deploy/security/` recriada sobre `nousresearch/hermes-agent:v0.22.5` (digest `sha256:9c5561579f3f…`), como solução temporária até uma release estável oficial trazer as correções. Ela reconstrói o ambiente Python pelo lock do fork (brotlicffi 1.2.1.0, pyasn1 0.6.5, tornado 6.6) e o `node_modules` do Photon (undici 7.30.1, zod 4.6.7), sem mudar o código da release. A imagem oficial tem brotlicffi 1.2.0.2, pyasn1 0.6.4, tornado 6.5.10, undici 7.30.0 e zod 4.5.4; msgpack, filelock e setuptools não estão instalados nela. Build amd64 validado numa candidata `--network none` com o endurecimento de produção: versões corrigidas, decoder Brotli ok, `auth_required` com 401 sem login, login 200, Photon carrega, 0 restarts. **Não implantada:** #6 e #4 continuam PARCIAL até o build arm64 no servidor e a troca da imagem, com backup do volume. O #7 não está na camada (ela não altera o código da release). O bridge do WhatsApp é instalado no volume e não é coberto pela imagem.
