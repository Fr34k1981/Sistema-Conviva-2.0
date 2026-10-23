$ErrorActionPreference = "Stop"

$psql = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
$db = "sistema_escolar"
$user = "escola_admin"
$pasta = "C:\SistemaConviva\migracao_neon"

$ordem = @(
    "alunos",
    "professores",
    "responsaveis",
    "agendamentos",
    "eletivas",
    "ocorrencias",
    "cadernos_tutoria",
    "conselho_turmas",
    "mapao_resultados",
    "prova_paulista_resultados",
    "rendimento_bimestral",
    "tutoria",
    "tutoria_backup_antes_cache",
    "tutoria_backup_antes_restauracao_manual",
    "tutoria_backups_json",
    "perfil_tutorado",
    "tutoria_coletiva",
    "tutoria_individual",
    "aluno_tutor",
    "caderno_tutoria",
    "encontros_tutoria",
    "usuarios"
)

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " IMPORTACAO DO NEON -> POSTGRESQL LOCAL" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($tabela in $ordem) {

    $arquivo = Join-Path $pasta "$tabela.csv"

    if (!(Test-Path $arquivo)) {
        Write-Host "ERRO: arquivo nao encontrado: $arquivo" -ForegroundColor Red
        exit 1
    }

    Write-Host "Importando $tabela ..." -ForegroundColor Cyan

    $comando = "\copy public.$tabela FROM '$arquivo' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')"

    & $psql -U $user -d $db -v ON_ERROR_STOP=1 -c $comando

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "==========================================" -ForegroundColor Red
        Write-Host " ERRO AO IMPORTAR: $tabela" -ForegroundColor Red
        Write-Host "==========================================" -ForegroundColor Red
        exit 1
    }

    Write-Host "OK: $tabela" -ForegroundColor Green
}

Write-Host ""
Write-Host "Ajustando sequencias..." -ForegroundColor Cyan

$ajustes = @(
    "SELECT setval('agendamentos_id_seq', COALESCE((SELECT MAX(id) FROM agendamentos), 1), true);",
    "SELECT setval('cadernos_tutoria_id_seq', COALESCE((SELECT MAX(id) FROM cadernos_tutoria), 1), true);",
    "SELECT setval('mapao_resultados_id_seq', COALESCE((SELECT MAX(id) FROM mapao_resultados), 1), true);",
    "SELECT setval('perfil_tutorado_id_seq', COALESCE((SELECT MAX(id) FROM perfil_tutorado), 1), true);",
    "SELECT setval('prova_paulista_resultados_id_seq', COALESCE((SELECT MAX(id) FROM prova_paulista_resultados), 1), true);",
    "SELECT setval('rendimento_bimestral_id_seq', COALESCE((SELECT MAX(id) FROM rendimento_bimestral), 1), true);",
    "SELECT setval('tutoria_backups_json_id_seq', COALESCE((SELECT MAX(id) FROM tutoria_backups_json), 1), true);",
    "SELECT setval('tutoria_coletiva_id_seq', COALESCE((SELECT MAX(id) FROM tutoria_coletiva), 1), true);",
    "SELECT setval('tutoria_individual_id_seq', COALESCE((SELECT MAX(id) FROM tutoria_individual), 1), true);"
)

foreach ($sql in $ajustes) {
    & $psql -U $user -d $db -v ON_ERROR_STOP=1 -c $sql

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO ao ajustar sequencia." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host " IMPORTACAO CONCLUIDA COM SUCESSO" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
