CREATE TABLE Prontuario(
	ID_Prontuario INT PRIMARY KEY IDENTITY(1,1),
	ID_Paciente INT NOT NULL,
	Nome VARCHAR(50) NOT NULL,
	Tamanho FLOAT NOT NULL,
	Alergia TEXT,
	Doenca TEXT,
	Fuma BIT,
	Bebe BIT,
	Usa_Drogas BIT,
	Observacoes TEXT
)

ALTER TABLE Prontuario
ADD CONSTRAINT fk_Prontuario FOREIGN KEY (ID_Paciente) REFERENCES Paciente(ID_Paciente)