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
