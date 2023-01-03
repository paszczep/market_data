-- GENERAL
CREATE TABLE IF NOT EXISTS process_statuses (
    process VARCHAR ( 255 ) NOT NULL,
    status_history JSONB,
    PRIMARY KEY (process)
);

-- SECURITIES

CREATE TABLE IF NOT EXISTS exchanges (
    code VARCHAR ( 255 ) NOT NULL,
    name VARCHAR ( 255 ) NOT NULL,
    timezone VARCHAR ( 255 ),
    properties JSONB,
    trading_session JSONB,
    PRIMARY KEY (code)
);

CREATE TABLE IF NOT EXISTS securities (
    ticker VARCHAR ( 255 ) NOT NULL,
    symbol VARCHAR ( 255 ),
    name VARCHAR ( 255 ),
    isin VARCHAR ( 255 ),
    conid VARCHAR ( 255 ),
    exchange VARCHAR ( 255 ),
    last_record TIMESTAMP,
    listed BOOLEAN NOT NULL DEFAULT TRUE,
    status_history JSONB,
    updated TIMESTAMP,
    transfer_algotrader BOOLEAN NOT NULL DEFAULT FALSE,
    ohlcv JSONB,
    PRIMARY KEY (ticker),
    FOREIGN KEY (exchange)
        REFERENCES exchanges (code) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS holidays (
    id INT NOT NULL,
    exchange VARCHAR ( 255 ) NOT NULL,
    holiday DATE NOT NULL,
    open TIME,
    close TIME,
    PRIMARY KEY (id),
    FOREIGN KEY (exchange)
        REFERENCES exchanges (code) ON UPDATE CASCADE
);

-- MIXES

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS mix_configurations (
    id INT NOT NULL,
    config JSONB,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mixes (
    id uuid NOT NULL DEFAULT uuid_generate_v4 (),
    mix_type VARCHAR ( 255 ),
    snapshot_date DATE NOT NULL,
    ticker VARCHAR ( 255 ) NOT NULL,
    exchange VARCHAR ( 255 ) NOT NULL,
    config_id INT NOT NULL,
    status_history JSONB,
    transfer_algotrader BOOLEAN NOT NULL DEFAULT FALSE,
    recalculate BOOLEAN NOT NULL DEFAULT FALSE,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    legacy JSONB,
    latest_ohlcv DATE,
    created timestamp NOT NULL DEFAULT NOW(),
    updated timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (ticker)
        REFERENCES securities (ticker) ON UPDATE CASCADE,
    FOREIGN KEY (exchange)
        REFERENCES exchanges (code) ON UPDATE CASCADE,
    FOREIGN KEY (config_id)
        REFERENCES mix_configurations (id)
);

CREATE TABLE IF NOT EXISTS models (
    id uuid DEFAULT uuid_generate_v4 (),
    mix_id uuid NOT NULL,
    controlled VARCHAR ( 255 ) NOT NULL,
    driver VARCHAR ( 255 ) NOT NULL,
    config JSONB,
    status_history JSONB,
    latest_driver_ohlcv DATE,
    created timestamp NOT NULL DEFAULT NOW(),
    updated timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, mix_id),
    FOREIGN KEY (mix_id)
        REFERENCES mixes (id) ON UPDATE CASCADE,
    FOREIGN KEY (controlled)
        REFERENCES securities (ticker) ON UPDATE CASCADE,
    FOREIGN KEY (driver)
        REFERENCES securities (ticker) ON UPDATE CASCADE
);

-- PORTFOLIO

CREATE TABLE IF NOT EXISTS portfolios (
    id uuid DEFAULT uuid_generate_v4 () NOT NULL,
    config JSONB,
    mixes JSONB,
    mixes_hash VARCHAR ( 255 ) NOT NULL,
    mixes_hash_prev VARCHAR ( 255 ) NOT NULL,
    status_history JSONB,
    trade BOOLEAN NOT NULL DEFAULT FALSE,
    created timestamp NOT NULL DEFAULT NOW(),
    updated timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mix_stats (
    mix_id uuid NOT NULL,
    historical_stats JSONB,
    cumulative_stats JSONB,
    created timestamp NOT NULL DEFAULT NOW(),
    updated timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (mix_id),
    FOREIGN KEY (mix_id)
        REFERENCES mixes (id)
);

CREATE TABLE IF NOT EXISTS portfolio_results (
    portfolio_id uuid NOT NULL,
    date DATE NOT NULL,
    included JSONB,
    netted JSONB,
    created timestamp NOT NULL DEFAULT NOW(),
    updated timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (portfolio_id, date),
    FOREIGN KEY (portfolio_id)
        REFERENCES portfolios (id)
);

-- TRADING

CREATE TABLE IF NOT EXISTS trading_signals (
    id uuid DEFAULT uuid_generate_v4 (),
    portfolio_id uuid NOT NULL,
    signal NUMERIC(3,2) NOT NULL,
    date DATE NOT NULL,
    latest_ohlcv DATE,
    mix_type VARCHAR ( 255 ),
    ticker VARCHAR ( 255 ) NOT NULL,
    exchange VARCHAR ( 255 ),
    mix_id uuid,
    netted BOOLEAN NOT NULL DEFAULT FALSE,
    created timestamp NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, portfolio_id),
    FOREIGN KEY (portfolio_id)
        REFERENCES portfolios (id),
    FOREIGN KEY (mix_id)
        REFERENCES mixes (id),
    FOREIGN KEY (exchange)
        REFERENCES exchanges (code) ON UPDATE CASCADE,
    FOREIGN KEY (ticker)
        REFERENCES securities (ticker) ON UPDATE CASCADE
);

-- SECOND

--CREATE TABLE IF NOT EXISTS batch_configurations (
--    id INT NOT NULL,
--    config JSONB,
--    PRIMARY KEY (id)
--);
--
--CREATE TABLE IF NOT EXISTS batches (
--    id uuid NOT NULL DEFAULT uuid_generate_v4 (),
--    snapshot timestamp NOT NULL,
--    controlled VARCHAR ( 255 ) NOT NULL,
--    drivers JSONB NOT NULL, --['BTC/USDT', 'AAPL_EQUITY', ]
--    config_id INT NOT NULL,
--    created timestamp NOT NULL DEFAULT NOW(),
--    PRIMARY KEY (id),
--    FOREIGN KEY (controlled)
--        REFERENCES securities (ticker) ON UPDATE CASCADE,
--    FOREIGN KEY (config_id)
--        REFERENCES batch_configurations (id)
--);
--
--CREATE TABLE IF NOT EXISTS models (
--    id uuid DEFAULT uuid_generate_v4 (),
--    batch_id uuid NOT NULL,
--    controlled VARCHAR ( 255 ) NOT NULL,
--    driver VARCHAR ( 255 ) NOT NULL,
--    config JSONB,
--    pnls JSONB,
--    created timestamp NOT NULL DEFAULT NOW()
--    PRIMARY KEY (id, mix_id),
--    FOREIGN KEY (batch_id)
--        REFERENCES batches (id) ON UPDATE CASCADE,
--    FOREIGN KEY (controlled)
--        REFERENCES securities (ticker) ON UPDATE CASCADE,
--    FOREIGN KEY (driver)
--        REFERENCES securities (ticker) ON UPDATE CASCADE
--);

-- INSERT

INSERT INTO exchanges
    (code, name, timezone, properties, trading_session)
    VALUES
    ('finnhub', 'finnhub', 'UTC', '""', '""');

INSERT INTO exchanges
    (code, name, timezone, properties, trading_session)
    VALUES
    ('binance', 'binance', 'UTC', '""', '""');