CREATE TABLE Medico
(
    ID_Medico INT PRIMARY KEY IDENTITY(1,1),
    ID_Funcionario INT NOT NULL,
	ID_Especialidade INT NOT NULL,
	CRM VARCHAR(13) NOT NULL
)

ALTER TABLE Medico
ADD CONSTRAINT fk_Funcionario FOREIGN KEY (ID_Funcionario) REFERENCES Funcionario(ID_Funcionario)
ALTER TABLE Medico
ADD CONSTRAINT fk_Medico FOREIGN KEY (ID_Especialidade) REFERENCES Especialidade(ID_Especialidade)