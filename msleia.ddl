create table SWORDS (
    id SERIAL PRIMARY KEY,
    userid INTEGER,
    name TEXT,
    type TEXT,
    description TEXT
);

create table FC_MASTER (
    id SERIAL PRIMARY KEY,
    userid INTEGER,
    name TEXT,
    description TEXT
);

create table FC_WORDS (
    id SERIAL PRIMARY KEY,
    userid INTEGER,
    flash_card_id INTEGER,
    sw_id INTEGER
);

create table WORD_REPORT (
    id SERIAL PRIMARY KEY,
    userid INTEGER,
    sw_id INTEGER,
    is_identified INTEGER
);
create table USER_PROF (
    id SERIAL PRIMARY KEY,
    name TEXT
);
create table FC_REPORT (
    id SERIAL PRIMARY KEY,
    userid INTEGER,
    flash_card_id INTEGER,
    last_accessed TIMESTAMP,
    is_completed INTEGER
);