-- Script de inicialização do banco de dados PostGIS
-- Executa automaticamente quando o container inicia pela primeira vez

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;

-- Criar schema para dados geográficos
CREATE SCHEMA IF NOT EXISTS geo;

-- Tabela de municípios de Rondônia
CREATE TABLE IF NOT EXISTS geo.municipios_ro (
    gid SERIAL PRIMARY KEY,
    cod_ibge VARCHAR(10),
    nome VARCHAR(100),
    uf VARCHAR(2) DEFAULT 'RO',
    area_km2 DECIMAL(12,2),
    populacao INTEGER,
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Tabela de bairros de Porto Velho
CREATE TABLE IF NOT EXISTS geo.bairros_pvh (
    gid SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    zona VARCHAR(50),
    area_km2 DECIMAL(10,4),
    populacao INTEGER,
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Tabela de dados de desmatamento (PRODES)
CREATE TABLE IF NOT EXISTS geo.desmatamento_pvh (
    gid SERIAL PRIMARY KEY,
    ano INTEGER NOT NULL,
    classe VARCHAR(50),
    area_ha DECIMAL(12,4),
    data_deteccao DATE,
    fonte VARCHAR(50) DEFAULT 'PRODES/INPE',
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Tabela de alertas DETER
CREATE TABLE IF NOT EXISTS geo.alertas_deter (
    gid SERIAL PRIMARY KEY,
    data_alerta DATE,
    classe VARCHAR(50),
    area_ha DECIMAL(10,4),
    satelite VARCHAR(50),
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Tabela de focos de calor
CREATE TABLE IF NOT EXISTS geo.focos_calor (
    gid SERIAL PRIMARY KEY,
    data_hora TIMESTAMP,
    satelite VARCHAR(50),
    temperatura_k DECIMAL(6,2),
    frp DECIMAL(10,2),
    geom GEOMETRY(Point, 4326)
);

-- Tabela de áreas protegidas
CREATE TABLE IF NOT EXISTS geo.areas_protegidas (
    gid SERIAL PRIMARY KEY,
    nome VARCHAR(200),
    categoria VARCHAR(100),
    esfera VARCHAR(50),
    area_ha DECIMAL(14,4),
    ato_legal VARCHAR(255),
    ano_criacao INTEGER,
    geom GEOMETRY(MultiPolygon, 4326)
);

-- Criar índices espaciais
CREATE INDEX IF NOT EXISTS idx_municipios_geom ON geo.municipios_ro USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_bairros_geom ON geo.bairros_pvh USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_desmatamento_geom ON geo.desmatamento_pvh USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_alertas_geom ON geo.alertas_deter USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_focos_geom ON geo.focos_calor USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_areas_protegidas_geom ON geo.areas_protegidas USING GIST(geom);

-- Índices para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_desmatamento_ano ON geo.desmatamento_pvh(ano);
CREATE INDEX IF NOT EXISTS idx_alertas_data ON geo.alertas_deter(data_alerta);
CREATE INDEX IF NOT EXISTS idx_focos_data ON geo.focos_calor(data_hora);

-- Inserir dados de exemplo para Porto Velho
INSERT INTO geo.municipios_ro (cod_ibge, nome, area_km2, populacao, geom)
VALUES (
    '1100205',
    'Porto Velho',
    34090.95,
    548952,
    ST_GeomFromText('MULTIPOLYGON(((-63.5 -8.3, -63.5 -9.2, -64.5 -9.2, -64.5 -8.3, -63.5 -8.3)))', 4326)
) ON CONFLICT DO NOTHING;

-- Inserir dados de exemplo de desmatamento
INSERT INTO geo.desmatamento_pvh (ano, classe, area_ha, data_deteccao, geom) VALUES
(2019, 'DESMATAMENTO', 15234.5, '2019-12-31', ST_GeomFromText('MULTIPOLYGON(((-63.85 -8.72, -63.85 -8.78, -63.92 -8.78, -63.92 -8.72, -63.85 -8.72)))', 4326)),
(2020, 'DESMATAMENTO', 18456.2, '2020-12-31', ST_GeomFromText('MULTIPOLYGON(((-63.80 -8.65, -63.80 -8.70, -63.88 -8.70, -63.88 -8.65, -63.80 -8.65)))', 4326)),
(2021, 'DESMATAMENTO', 12789.8, '2021-12-31', ST_GeomFromText('MULTIPOLYGON(((-63.75 -8.60, -63.75 -8.68, -63.82 -8.68, -63.82 -8.60, -63.75 -8.60)))', 4326)),
(2022, 'DESMATAMENTO', 14567.3, '2022-12-31', ST_GeomFromText('MULTIPOLYGON(((-63.90 -8.80, -63.90 -8.88, -63.98 -8.88, -63.98 -8.80, -63.90 -8.80)))', 4326)),
(2023, 'DESMATAMENTO', 11234.6, '2023-12-31', ST_GeomFromText('MULTIPOLYGON(((-63.70 -8.55, -63.70 -8.62, -63.78 -8.62, -63.78 -8.55, -63.70 -8.55)))', 4326)),
(2024, 'DESMATAMENTO', 9876.4, '2024-12-31', ST_GeomFromText('MULTIPOLYGON(((-63.65 -8.50, -63.65 -8.58, -63.72 -8.58, -63.72 -8.50, -63.65 -8.50)))', 4326));

-- Inserir bairros de exemplo
INSERT INTO geo.bairros_pvh (nome, zona, area_km2, populacao, geom) VALUES
('Centro', 'Central', 2.5, 15000, ST_GeomFromText('MULTIPOLYGON(((-63.89 -8.75, -63.89 -8.77, -63.91 -8.77, -63.91 -8.75, -63.89 -8.75)))', 4326)),
('Caiari', 'Norte', 4.2, 25000, ST_GeomFromText('MULTIPOLYGON(((-63.88 -8.73, -63.88 -8.75, -63.90 -8.75, -63.90 -8.73, -63.88 -8.73)))', 4326)),
('Embratel', 'Sul', 3.8, 18000, ST_GeomFromText('MULTIPOLYGON(((-63.90 -8.78, -63.90 -8.80, -63.92 -8.80, -63.92 -8.78, -63.90 -8.78)))', 4326)),
('Nacional', 'Leste', 5.1, 32000, ST_GeomFromText('MULTIPOLYGON(((-63.86 -8.76, -63.86 -8.78, -63.88 -8.78, -63.88 -8.76, -63.86 -8.76)))', 4326)),
('Nova Porto Velho', 'Oeste', 6.3, 28000, ST_GeomFromText('MULTIPOLYGON(((-63.92 -8.74, -63.92 -8.76, -63.94 -8.76, -63.94 -8.74, -63.92 -8.74)))', 4326));

-- Inserir alertas DETER de exemplo
INSERT INTO geo.alertas_deter (data_alerta, classe, area_ha, satelite, geom) VALUES
('2024-01-15', 'DESMATAMENTO_CR', 45.6, 'AMAZONIA-1', ST_GeomFromText('MULTIPOLYGON(((-63.82 -8.68, -63.82 -8.69, -63.83 -8.69, -63.83 -8.68, -63.82 -8.68)))', 4326)),
('2024-02-20', 'DEGRADACAO', 32.1, 'CBERS-4A', ST_GeomFromText('MULTIPOLYGON(((-63.78 -8.65, -63.78 -8.66, -63.79 -8.66, -63.79 -8.65, -63.78 -8.65)))', 4326)),
('2024-03-10', 'MINERACAO', 18.4, 'AMAZONIA-1', ST_GeomFromText('MULTIPOLYGON(((-63.95 -8.82, -63.95 -8.83, -63.96 -8.83, -63.96 -8.82, -63.95 -8.82)))', 4326));

-- Inserir focos de calor de exemplo
INSERT INTO geo.focos_calor (data_hora, satelite, temperatura_k, frp, geom) VALUES
('2024-08-15 14:30:00', 'AQUA_M-T', 342.5, 25.6, ST_GeomFromText('POINT(-63.85 -8.72)', 4326)),
('2024-08-15 15:45:00', 'TERRA_M-T', 338.2, 18.3, ST_GeomFromText('POINT(-63.78 -8.68)', 4326)),
('2024-08-16 13:20:00', 'NPP-375', 345.8, 32.1, ST_GeomFromText('POINT(-63.92 -8.81)', 4326)),
('2024-09-01 16:00:00', 'GOES-16', 340.1, 22.4, ST_GeomFromText('POINT(-63.88 -8.75)', 4326));

-- Garantir permissões
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA geo TO geouser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA geo TO geouser;
GRANT USAGE ON SCHEMA geo TO geouser;

-- Mensagem de confirmação
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully with sample data for Porto Velho!';
END $$;
