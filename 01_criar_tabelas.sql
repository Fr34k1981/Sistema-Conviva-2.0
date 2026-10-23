-- Sistema Conviva 2.0
-- 01_criar_tabelas.sql
-- Reconstrução baseada no schema levantado do Neon.
-- PostgreSQL local 17.x
-- NÃO apaga tabelas existentes.

BEGIN;

CREATE SCHEMA IF NOT EXISTS extensions;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA extensions;

-- Sequences devem existir antes das tabelas que usam nextval().
CREATE SEQUENCE IF NOT EXISTS public.agendamentos_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.cadernos_tutoria_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.grade_janelas_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.mapao_resultados_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.perfil_tutorado_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.prova_paulista_resultados_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.rendimento_bimestral_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.tutoria_backups_json_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.tutoria_coletiva_id_seq;
CREATE SEQUENCE IF NOT EXISTS public.tutoria_individual_id_seq;

CREATE TABLE IF NOT EXISTS public.agendamentos (
 id integer NOT NULL DEFAULT nextval('public.agendamentos_id_seq'::regclass), data_agendamento date NOT NULL, horario varchar(20) NOT NULL, espaco varchar(100) NOT NULL, turma varchar(50) NOT NULL, disciplina varchar(100), prioridade varchar(50) DEFAULT 'NORMAL'::character varying, semanas integer DEFAULT 0, professor_nome varchar(200) NOT NULL, professor_email varchar(200), status varchar(50) DEFAULT 'ATIVO'::character varying, created_at timestamp without time zone DEFAULT now(), CONSTRAINT agendamentos_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.aluno_tutor (
 id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(), aluno_id uuid, professor_id uuid, created_at timestamp without time zone DEFAULT now(), CONSTRAINT aluno_tutor_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.alunos (
 id bigint NOT NULL, created_at timestamp with time zone NOT NULL DEFAULT now(), ra text, nome text, data_nascimento text, situacao text, turma text, foto text, CONSTRAINT alunos_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.caderno_tutoria (
 id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(), aluno_id uuid, professor_id uuid, tipo text, pontos_positivos text, pontos_atencao text, destaques text, estudantes_atencao text, acoes_gerais text, acoes_individuais text, observacoes text, assinatura_professor text, assinatura_gestao text, created_at timestamp without time zone DEFAULT now(), CONSTRAINT caderno_tutoria_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.cadernos_tutoria (
 id bigint NOT NULL DEFAULT nextval('public.cadernos_tutoria_id_seq'::regclass), chave text NOT NULL, professor text NOT NULL, estudante text NOT NULL, turma text, ano_letivo integer NOT NULL DEFAULT 2026, dados jsonb NOT NULL DEFAULT '{}'::jsonb, criado_em timestamp with time zone NOT NULL DEFAULT now(), atualizado_em timestamp with time zone NOT NULL DEFAULT now(), CONSTRAINT cadernos_tutoria_pkey PRIMARY KEY (id), CONSTRAINT cadernos_tutoria_chave_key UNIQUE (chave));
CREATE TABLE IF NOT EXISTS public.conselho_turmas (
 id uuid NOT NULL DEFAULT gen_random_uuid(), chave text NOT NULL, turma text, ano_letivo text, bimestre text, dados_json jsonb NOT NULL DEFAULT '{}'::jsonb, criado_em timestamp with time zone DEFAULT now(), atualizado_em timestamp with time zone DEFAULT now(), CONSTRAINT conselho_turmas_pkey PRIMARY KEY (id), CONSTRAINT conselho_turmas_chave_key UNIQUE (chave));
CREATE TABLE IF NOT EXISTS public.eletivas (
 id bigint NOT NULL, professora text NOT NULL, nome_aluno text NOT NULL, serie text NOT NULL, origem text DEFAULT 'planilha'::text, created_at timestamp with time zone DEFAULT now(), CONSTRAINT eletivas_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.grade_janelas (
 id bigint NOT NULL DEFAULT nextval('public.grade_janelas_id_seq'::regclass), professor text NOT NULL, dia_semana text NOT NULL, aula integer NOT NULL, tipo text NOT NULL, ano_letivo integer NOT NULL DEFAULT 2026, created_at timestamp with time zone NOT NULL DEFAULT now(), CONSTRAINT grade_janelas_pkey PRIMARY KEY (id), CONSTRAINT grade_janelas_professor_dia_aula_ano_key UNIQUE (professor,dia_semana,aula,ano_letivo));
CREATE TABLE IF NOT EXISTS public.encontros_tutoria (
 id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(), aluno_id uuid, professor_id uuid, numero_encontro integer, data date, created_at timestamp without time zone DEFAULT now(), CONSTRAINT encontros_tutoria_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.mapao_resultados (
 id bigint NOT NULL DEFAULT nextval('public.mapao_resultados_id_seq'::regclass), ano_letivo text NOT NULL, bimestre text NOT NULL, turma text NOT NULL, ciclo text, turno text, estudante text NOT NULL, situacao text, frequencia_percentual numeric, faltas numeric, faltas_anuais numeric, total_aulas numeric, componentes jsonb DEFAULT '{}'::jsonb, notas_abaixo_cinco jsonb DEFAULT '[]'::jsonb, arquivo_origem text, created_at timestamp with time zone DEFAULT now(), updated_at timestamp with time zone DEFAULT now(), CONSTRAINT mapao_resultados_pkey PRIMARY KEY (id), CONSTRAINT mapao_resultados_ano_letivo_bimestre_turma_estudante_key UNIQUE (ano_letivo,bimestre,turma,estudante));
CREATE TABLE IF NOT EXISTS public.ocorrencias (
 id bigint NOT NULL, created_at timestamp with time zone NOT NULL DEFAULT now(), data text, aluno text, ra text, turma text, categoria text, gravidade text, relato text, encaminhamento text, professor text, medidas_aplicadas text, medidas_obs text, envolvidos text DEFAULT ''::text, horario_chegada text, horario_permitido text, justificativa text, CONSTRAINT ocorrencias_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.perfil_tutorado (
 id bigint NOT NULL DEFAULT nextval('public.perfil_tutorado_id_seq'::regclass), chave_caderno text NOT NULL, professor text NOT NULL, estudante text NOT NULL, turma text, dados jsonb NOT NULL DEFAULT '{}'::jsonb, atualizado_em timestamp with time zone NOT NULL DEFAULT now(), CONSTRAINT perfil_tutorado_pkey PRIMARY KEY (id), CONSTRAINT perfil_tutorado_chave_caderno_key UNIQUE (chave_caderno));
CREATE TABLE IF NOT EXISTS public.professores (
 id bigint NOT NULL, created_at timestamp with time zone NOT NULL DEFAULT now(), nome text, email text, foto text, cargo text, CONSTRAINT professores_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.prova_paulista_resultados (
 id bigint NOT NULL DEFAULT nextval('public.prova_paulista_resultados_id_seq'::regclass), ano_letivo text NOT NULL, bimestre text NOT NULL, turma text NOT NULL, ciclo text, turno text, ra text NOT NULL, estudante text, participacao numeric, acertos_percentual numeric, componentes jsonb DEFAULT '{}'::jsonb, arquivo_origem text, created_at timestamp with time zone DEFAULT now(), updated_at timestamp with time zone DEFAULT now(), CONSTRAINT prova_paulista_resultados_pkey PRIMARY KEY (id), CONSTRAINT prova_paulista_resultados_ano_letivo_bimestre_turma_ra_key UNIQUE (ano_letivo,bimestre,turma,ra));
CREATE TABLE IF NOT EXISTS public.rendimento_bimestral (
 id bigint NOT NULL DEFAULT nextval('public.rendimento_bimestral_id_seq'::regclass), chave_caderno text NOT NULL, professor text NOT NULL, estudante text NOT NULL, turma text, componente_curricular text NOT NULL, primeiro_bimestre text, segundo_bimestre text, terceiro_bimestre text, quarto_bimestre text, resultado_final text, atualizado_em timestamp with time zone NOT NULL DEFAULT now(), CONSTRAINT rendimento_bimestral_pkey PRIMARY KEY (id), CONSTRAINT rendimento_bimestral_chave_caderno_componente_curricular_key UNIQUE (chave_caderno,componente_curricular));
CREATE TABLE IF NOT EXISTS public.responsaveis (
 id bigint NOT NULL, created_at timestamp with time zone NOT NULL DEFAULT now(), cargo text, nome text, ativo boolean, CONSTRAINT responsaveis_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.tutoria (
 id uuid NOT NULL DEFAULT gen_random_uuid(), professora text NOT NULL, nome_aluno text NOT NULL, serie text DEFAULT ''::text, origem text DEFAULT 'manual'::text, tipo text DEFAULT 'Professor(a)'::text, espaco text DEFAULT ''::text, horario text DEFAULT ''::text, dia text DEFAULT ''::text, created_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text,now()), updated_at timestamp with time zone NOT NULL DEFAULT timezone('utc'::text,now()), ra text, turno text, CONSTRAINT tutoria_pkey PRIMARY KEY (id), CONSTRAINT tutoria_unq_professora_nome_serie UNIQUE (professora,nome_aluno,serie));
CREATE TABLE IF NOT EXISTS public.tutoria_backup_antes_cache (
 id uuid, professora text, nome_aluno text, serie text, origem text, tipo text, espaco text, horario text, dia text, created_at timestamp with time zone, updated_at timestamp with time zone);
CREATE TABLE IF NOT EXISTS public.tutoria_backup_antes_restauracao_manual (
 id uuid, professora text, nome_aluno text, serie text, origem text, tipo text, espaco text, horario text, dia text, created_at timestamp with time zone, updated_at timestamp with time zone);
CREATE TABLE IF NOT EXISTS public.tutoria_backups_json (
 id bigint NOT NULL DEFAULT nextval('public.tutoria_backups_json_id_seq'::regclass), criado_em timestamp with time zone DEFAULT now(), motivo text, total_registros integer, dados jsonb NOT NULL DEFAULT '[]'::jsonb, CONSTRAINT tutoria_backups_json_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.tutoria_coletiva (
 id bigint NOT NULL DEFAULT nextval('public.tutoria_coletiva_id_seq'::regclass), chave_caderno text NOT NULL, professor text NOT NULL, estudante text NOT NULL, turma text, data_encontro text, numero_encontro text, objetivo_encontro text, campos jsonb NOT NULL DEFAULT '{}'::jsonb, observacoes text, criado_em timestamp with time zone NOT NULL DEFAULT now(), CONSTRAINT tutoria_coletiva_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.tutoria_individual (
 id bigint NOT NULL DEFAULT nextval('public.tutoria_individual_id_seq'::regclass), chave_caderno text NOT NULL, professor text NOT NULL, estudante text NOT NULL, turma text, data_encontro text, objetivo text, pontos_positivos text, pontos_atencao text, acoes_encaminhamentos text, criado_em timestamp with time zone NOT NULL DEFAULT now(), CONSTRAINT tutoria_individual_pkey PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS public.usuarios (
 id uuid NOT NULL DEFAULT extensions.uuid_generate_v4(), nome text, email text, senha text, tipo text, created_at timestamp without time zone DEFAULT now(), CONSTRAINT usuarios_pkey PRIMARY KEY (id), CONSTRAINT usuarios_email_key UNIQUE (email));

ALTER SEQUENCE public.agendamentos_id_seq OWNED BY public.agendamentos.id;
ALTER SEQUENCE public.cadernos_tutoria_id_seq OWNED BY public.cadernos_tutoria.id;
ALTER SEQUENCE public.grade_janelas_id_seq OWNED BY public.grade_janelas.id;
ALTER SEQUENCE public.mapao_resultados_id_seq OWNED BY public.mapao_resultados.id;
ALTER SEQUENCE public.perfil_tutorado_id_seq OWNED BY public.perfil_tutorado.id;
ALTER SEQUENCE public.prova_paulista_resultados_id_seq OWNED BY public.prova_paulista_resultados.id;
ALTER SEQUENCE public.rendimento_bimestral_id_seq OWNED BY public.rendimento_bimestral.id;
ALTER SEQUENCE public.tutoria_backups_json_id_seq OWNED BY public.tutoria_backups_json.id;
ALTER SEQUENCE public.tutoria_coletiva_id_seq OWNED BY public.tutoria_coletiva.id;
ALTER SEQUENCE public.tutoria_individual_id_seq OWNED BY public.tutoria_individual.id;

CREATE INDEX IF NOT EXISTS idx_cadernos_tutoria_ano ON public.cadernos_tutoria USING btree (ano_letivo);
CREATE INDEX IF NOT EXISTS idx_cadernos_tutoria_estudante ON public.cadernos_tutoria USING btree (estudante);
CREATE INDEX IF NOT EXISTS idx_cadernos_tutoria_professor ON public.cadernos_tutoria USING btree (professor);
CREATE INDEX IF NOT EXISTS idx_cadernos_tutoria_turma ON public.cadernos_tutoria USING btree (turma);
CREATE INDEX IF NOT EXISTS idx_conselho_turmas_chave ON public.conselho_turmas USING btree (chave);
CREATE INDEX IF NOT EXISTS idx_conselho_turmas_turma ON public.conselho_turmas USING btree (turma);
CREATE INDEX IF NOT EXISTS tutoria_idx_professora ON public.tutoria USING btree (professora);

ALTER TABLE public.perfil_tutorado ADD CONSTRAINT perfil_tutorado_chave_caderno_fkey FOREIGN KEY (chave_caderno) REFERENCES public.cadernos_tutoria (chave);
ALTER TABLE public.rendimento_bimestral ADD CONSTRAINT rendimento_bimestral_chave_caderno_fkey FOREIGN KEY (chave_caderno) REFERENCES public.cadernos_tutoria (chave);
ALTER TABLE public.tutoria_coletiva ADD CONSTRAINT tutoria_coletiva_chave_caderno_fkey FOREIGN KEY (chave_caderno) REFERENCES public.cadernos_tutoria (chave);
ALTER TABLE public.tutoria_individual ADD CONSTRAINT tutoria_individual_chave_caderno_fkey FOREIGN KEY (chave_caderno) REFERENCES public.cadernos_tutoria (chave);

CREATE OR REPLACE VIEW public.v_tutoria_estudantes_duplicados AS
SELECT nome_aluno AS estudante, ra, serie AS turma, string_agg(DISTINCT professora, ', '::text ORDER BY professora) AS aparece_em, count(*) AS quantidade_de_vinculos
FROM public.tutoria
WHERE nome_aluno IS NOT NULL AND TRIM(BOTH FROM nome_aluno) <> ''::text
GROUP BY nome_aluno, ra, serie HAVING count(*) > 1 ORDER BY count(*) DESC, nome_aluno;

CREATE OR REPLACE VIEW public.v_tutoria_exportar_por_turma AS
SELECT serie AS turma, nome_aluno AS estudante, ra, professora AS tutor, tipo, origem, created_at, updated_at,
CASE WHEN professora IS NULL OR TRIM(BOTH FROM professora) = ''::text THEN 'SEM TUTOR'::text WHEN array_length(regexp_split_to_array(TRIM(BOTH FROM professora), '\s+'::text),1) < 2 THEN 'TUTOR COM NOME INCOMPLETO'::text ELSE 'OK'::text END AS status_tutor
FROM public.tutoria WHERE nome_aluno IS NOT NULL AND TRIM(BOTH FROM nome_aluno) <> ''::text
ORDER BY serie, nome_aluno, professora;

CREATE OR REPLACE VIEW public.v_tutoria_exportar_por_tutor AS
SELECT professora AS tutor, serie AS turma, nome_aluno AS estudante, ra, tipo, origem, created_at, updated_at,
CASE WHEN professora IS NULL OR TRIM(BOTH FROM professora) = ''::text THEN 'SEM TUTOR'::text WHEN array_length(regexp_split_to_array(TRIM(BOTH FROM professora), '\s+'::text),1) < 2 THEN 'TUTOR COM NOME INCOMPLETO'::text ELSE 'OK'::text END AS status_tutor
FROM public.tutoria WHERE nome_aluno IS NOT NULL AND TRIM(BOTH FROM nome_aluno) <> ''::text
ORDER BY professora, serie, nome_aluno;

CREATE OR REPLACE VIEW public.v_tutoria_tutores_incompletos AS
SELECT professora AS tutor_incompleto, serie AS turma, nome_aluno AS estudante, ra, created_at, updated_at
FROM public.tutoria
WHERE professora IS NOT NULL AND TRIM(BOTH FROM professora) <> ''::text AND array_length(regexp_split_to_array(TRIM(BOTH FROM professora), '\s+'::text),1) < 2
ORDER BY professora, serie, nome_aluno;

COMMIT;
