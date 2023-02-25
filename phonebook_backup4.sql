--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.3 в Ср фев 22 04:18:52 2023
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: names
CREATE TABLE IF NOT EXISTS names (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE);
INSERT INTO names (name) VALUES ('Леонид Петрович ГСК');
INSERT INTO names (name) VALUES ('Оля Риэлтор');
INSERT INTO names (name) VALUES ('Любимая Тёща');

-- Таблица: phones
CREATE TABLE IF NOT EXISTS phones (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    phone TEXT NOT NULL UNIQUE,
                    name_id INTEGER NOT NULL,
                    CONSTRAINT fk_names
                    	FOREIGN KEY (name_id)
                    	REFERENCES names(id)
                    	ON UPDATE CASCADE
                    	ON DELETE CASCADE);
INSERT INTO phones (phone, name_id) VALUES ('72443351195', 1);
INSERT INTO phones (phone, name_id) VALUES ('72627397543', 1);
INSERT INTO phones (phone, name_id) VALUES ('78436840045', 2);
INSERT INTO phones (phone, name_id) VALUES ('77554802591', 3);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
