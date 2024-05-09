CREATE SCHEMA moodle;  
  
CREATE TABLE moodle.user (  
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,  
    nombre TEXT NOT NULL  
);  
  
CREATE TABLE moodle.curso (  
    id_curso INTEGER PRIMARY KEY AUTOINCREMENT,  
    nombre_curso TEXT NOT NULL  
);  
  
CREATE TABLE moodle.foro (  
    id_foro INTEGER PRIMARY KEY AUTOINCREMENT,  
    tema TEXT NOT NULL,  
    descripcion TEXT,  
    id_curso INTEGER,  
    FOREIGN KEY (id_curso) REFERENCES moodle.curso(id_curso)  
);  
  
CREATE TABLE moodle.debate (  
    id_debate INTEGER PRIMARY KEY AUTOINCREMENT,  
    nombre_debate TEXT NOT NULL,  
    id_curso INTEGER,  
    id_foro INTEGER,  
    FOREIGN KEY (id_curso) REFERENCES moodle.curso(id_curso),  
    FOREIGN KEY (id_foro) REFERENCES moodle.foro(id_foro)  
);  
  
CREATE TABLE moodle.post (  
    id_post INTEGER PRIMARY KEY AUTOINCREMENT,  
    descripcion TEXT NOT NULL,  
    id_user INTEGER,  
    id_debate INTEGER,  
    FOREIGN KEY (id_user) REFERENCES moodle.user(id_user),  
    FOREIGN KEY (id_debate) REFERENCES moodle.debate(id_debate)  
);  