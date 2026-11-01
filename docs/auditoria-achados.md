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
| 7 | Ações de dashboard com cookie não validam CSRF/origem | média | RESOLVIDO | `hermes_cli/dashboard_auth/cookies.py:59`; `hermes_cli/dashboard_auth/middleware.py:160`; `hermes_cli/web_routers/actions.py:160`; `hermes_cli/web_server.py:557`; Potencial — inspeção estática, sem exploração. |

Reverificações e decisões históricas: #1 — Correção Pillow preservada; #2 — Correção certifi preservada; #3 — Constraint aiohttp corrigida preservada; #4 — REABERTO/PARCIAL para advisories atuais; #5 — Correção do revert desktop presente. O relatório detalha alcance/evidência; provas operacionais antigas não foram repetidas.

## Resolução de 31/10/2026

Commits na branch `fix/auditoria-20261031` (base `01493e69a3`): `6db2779b61` (#6 e #4 Python), `d33189fae2` (#4 JS), `64416f43b8` (#7). Sem push nem deploy. Detalhes, decisões e falsificação no adendo do relatório da rodada.

| ID | Status | Resolução | Pendência / condição de fechamento |
|---|---|---|---|
| #6 | RESOLVIDO (31/10/2026) | `brotlicffi==1.2.1.0` no extra `messaging` e no `uv.lock`, alinhado ao upstream (#145147). Smoke Brotli benigno pelo leitor real do gateway: o httpx seleciona brotlicffi e envia `br`, o que confirma a cadeia | Produção com 1.2.1.0 desde 31/10 pela camada `deploy/security/` (ver implantação abaixo). Retirar a camada quando uma estável oficial trouxer ≥1.2.1.0 |
| #4 | PARCIAL (31/10/2026) | Python: pyasn1 0.6.5, tornado 6.6, msgpack 1.2.3, filelock 4.2.1, setuptools 84.1.0. JS: undici 6.29.1/7.30.1, zod 4.6.7 (raiz e Photon), fast-uri 3.1.9, body-parser 1.20.9 (bridge WhatsApp). Locks regenerados com uv 0.13.5 e npm 12.0.2 (versões do PM) | follow-redirects 1.16.2 e joi 18.3.1 (só via `wait-on`, dev) bloqueados pelo `min-release-age=14`; reabrir em 08/11 e 11/11. Produção: pyasn1, tornado e Photon corrigidos pela camada; bridge WhatsApp não instalado no volume. qs 6.16.0 no bridge não alcançável (sem `stringify` com `arrayFormat: 'comma'`). Tooling moderado sem correção não major. `braces` do website como antes |
| #7 | RESOLVIDO (01/11/2026; PARCIAL em 31/10) | `gated_auth_middleware` recusa (403) escrita com cookie quando `Sec-Fetch-Site` não é `same-origin`/`none`; sem o header, mantém o comportamento (compatível com proxy HTTP, motivo da reversão `22103f58a8` no upstream). Teste vermelho no código anterior | Sem defesa em HTTP comum fora do loopback (navegador não envia Fetch Metadata). Em produção desde 01/11 pela camada `0.22.5-security-20261101` (ver seção de 01/11) |

Validação (contêineres Linux descartáveis): `scripts/check` 12/12; `--check-lock` ok; `tests/hermes_cli`, `tests/gateway` e `tests/plugins` com os extras afetados: 30901 testes passando e 158 falhando, com 157 iguais no HEAD original (lock e ambiente do HEAD) e 1 de carga que passa isolado nas duas árvores. TUI 1880 testes passando com o undici novo; `npm ci` ok nos três locks.

**Camada de segurança (31/10/2026):** `deploy/security/` recriada sobre `nousresearch/hermes-agent:v0.22.5` (digest `sha256:9c5561579f3f…`), como solução temporária até uma release estável oficial trazer as correções. Ela reconstrói o ambiente Python pelo lock do fork (brotlicffi 1.2.1.0, pyasn1 0.6.5, tornado 6.6) e o `node_modules` do Photon (undici 7.30.1, zod 4.6.7), sem mudar o código da release. A imagem oficial tem brotlicffi 1.2.0.2, pyasn1 0.6.4, tornado 6.5.10, undici 7.30.0 e zod 4.5.4; msgpack, filelock e setuptools não estão instalados nela. Build amd64 validado numa candidata `--network none` com o endurecimento de produção: versões corrigidas, decoder Brotli ok, `auth_required` com 401 sem login, login 200, Photon carrega, 0 restarts. O #7 não está na camada (ela não altera o código da release). O bridge do WhatsApp é instalado no volume e não é coberto pela imagem.

## Implantação da camada (31/10/2026)

Produção (servidor próprio, arm64) passou de `nousresearch/hermes-agent:v0.22.5@sha256:9c5561579f3f…` para `hermes-agent:0.22.5-security-20261031@sha256:9b81db29f5e4…`, construída no servidor a partir do commit `cc33165dfb`. Procedimento de 23/10:
- Backup do volume com o serviço parado (45 s), cifrado com `age` e decifrado fora do servidor, com hashes iguais ao manifesto e gzip íntegro.
- Candidata `--network none` sobre um clone do volume, com o endurecimento de produção. Estado idêntico à linha de base: config 51, hashes de `.env`/auth/SOUL e 6 bancos com integrity ok e as mesmas contagens.
- Troca só da linha `image:` do compose, após `config -q` e `up -d --dry-run`. Parada de 10 s.

Verificação pós-troca:
- Dependências: brotlicffi 1.2.1.0, pyasn1 0.6.5, tornado 6.6, Photon undici 7.30.1 e zod 4.6.7.
- Serviço: `overall ok`, gateway running, 3/3 plataformas conectadas.
- Dashboard: `auth_required` com login 200, `/api/config` autenticado 200 e 401 sem sessão e com bearer inválido.
- Endurecimento mantido (cap_drop ALL + 6 caps, no-new-privileges, pids 512, rede própria, porta só em loopback), 0 restarts e nenhum traceback.

Nenhum segredo foi impresso. Rollback: restaurar o backup do compose de 31/10 e o volume `hermes-rollback-20261031T114834Z`. A imagem oficial v0.22.5 continua no servidor. Gate H1 (brotlicffi) reexecutado: PASS em produção.

## #7 — análise da parte restante (31/10/2026)

Status continua **PARCIAL**. O fork já recusa a escrita com cookie vinda de outra origem do mesmo site (`64416f43b8`). O que falta é a correção chegar à produção, que roda a imagem oficial v0.22.5 com a camada `deploy/security/`, e a camada não altera código.

- **A lacuna "HTTP comum fora do loopback" não alcança esta implantação.** O compose publica o dashboard só em `127.0.0.1:9119`, e o PC o acessa por túnel SSH em `http://127.0.0.1:9119`. `127.0.0.1` é origem confiável para o navegador: Fetch Metadata é enviado mesmo em HTTP. Prova local (Chromium do Playwright, servidores descartáveis só em loopback): um formulário em `http://127.0.0.1:A` com POST para `http://127.0.0.1:B` chegou com o cookie `SameSite=Lax`, `Sec-Fetch-Site: same-site` e `Origin: http://127.0.0.1:A`. Ou seja, o ataque é real nesse acesso, e a recusa do fork o bloqueia.
- **Decisão: não ampliar o código do fork para o HTTP fora do loopback.** Isso exigiria um cabeçalho anti-CSRF nos wrappers do SPA (`web/src/lib/api.ts`: `fetchJSON` e `authedFetch`), nos demais pontos de escrita e nos plugins do dashboard, ou uma allowlist de origens configurável. A allowlist seria extensão especulativa sem chamador, vedada pelo AGENTS.md. O §3.2 do `SECURITY.md` põe o bind fora do loopback sob responsabilidade do operador, e o compose já proíbe expor na LAN sem proxy autenticado. Reabrir se o dashboard passar a ser publicado fora do loopback sem HTTPS.
- **Caminho para a produção:** o `SECURITY.md` classifica o caso no §3.1 (alguém fora do conjunto autorizado faz o dashboard executar trabalho), cujo canal é o reporte privado (GitHub Security Advisory ou security@nousresearch.com). O rascunho está em `C:\Codes\relatorios\hermes-agent\rascunho-reporte-upstream-achado-7.md`, **não enviado** e aguardando o titular. A alternativa, aplicar o patch na camada, contraria o desenho dela, que só reconstrói dependências, e fica para decisão do titular.
- Sem mudança de código nesta rodada. A tentativa de rodar `scripts/run_tests.sh` sem bootstrap preparou um `HERMES_HOME` e ferramentas fora do repositório (`%LOCALAPPDATA%\hermes`, `~/.hermes`, 1,8 GB) e parou em "no bootstrap Python found". As três pastas foram criadas por essa execução e removidas em seguida. Para rodar a suíte sem gravar fora de `C:\Codes`, usar contêiner ou o ambiente descartável da rodada anterior.

**#7, estado do upstream em 01/11/2026:** a `main` do upstream ganhou em 22–25/10 a checagem de origem para escritas com cookie (`cookie_origin_is_allowed`), mas só no listener Webapp do gateway (`own_origin_cookie_writes=True`). O `hermes dashboard`, que é a superfície publicada em `127.0.0.1:9119` aqui, ficou de propósito com a regra antiga (`False`), porque o fallback Origin-vs-Host quebrava proxy HTTP sem Fetch Metadata. A v0.22.5 (23/10) é anterior. Não está corrigido para esta implantação; o rascunho do reporte foi atualizado com isso.

## #7 — correção em produção e reporte ao upstream (01/11/2026)

Status **RESOLVIDO** na implantação atual. Reabrir se o dashboard for publicado em HTTP comum fora do loopback, onde o navegador não envia Fetch Metadata.

- **Camada:** `deploy/security/apply_source_fixes.py` troca `hermes_cli/dashboard_auth/middleware.py` pela cópia do fork (`64416f43b8`). Só troca se o arquivo da imagem tiver o sha256 da v0.22.5 e a cópia o da correção revisada; senão o build falha. Commit `3832f88de1`; tag `hermes-agent:0.22.5-security-20261101`.
- **Prova (contêiner descartável, sem rede, auth_required, login por senha, POST com cookie numa rota de escrita inexistente):**
  - v0.22.5 e camada de 31/10: `same-site` e `cross-site` passam pelo gate (405 da rota);
  - camada de 01/11: 403;
  - `same-origin`, sem o header e leitura iguais nas duas;
  - cópia adulterada do middleware faz o build falhar.
- **Produção (Orange Pi, 01/11 ~12:20Z):** build arm64 no Pi (47 s, cache), mesma prova na candidata, troca só da linha `image:` do compose, parada de 13 s, 0 restarts. Pós: `overall ok`, 3/3 plataformas, login 200, 401 sem sessão e com bearer inválido, `same-site`/`cross-site` 403, porta só em `127.0.0.1:9119`, endurecimento igual. Comprovantes em `/srv/containers/hermes/security-20261101/receipts/`. Rollback: `compose.yml.bak-<TS>-hermes-security-20261101` e volume `hermes-rollback-<TS>`.
- **Upstream:** reporte privado enviado em 01/11 pelo GitHub Security Advisory (`GHSA-4w4r-jmvh-vcv9`, estado triage). Texto em `C:Codeselatorioshermes-agenteporte-upstream-achado-7-final.md`. Quando uma estável trouxer a correção (ou equivalente), retirar `apply_source_fixes.py` junto com a camada.
