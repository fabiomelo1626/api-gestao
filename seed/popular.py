'''from seed.tabelasAuxiliaresSeed import seed_tabelas_auxiliares
from seed.unidadeGestoraSeed import seed_unidades_gestoras
from conexao.conect_db import SessionLocal

def popular():
    db = SessionLocal()
    try:
      
        seed_unidades_gestoras_joaquim_gomes(db)
        print("Seed da tabela unidades gestoras de Joaquim gomes executado com Sucesso!")
        
        seed_tabelas_auxiliares(db)
        print("Seed das tabelas auxiliares executado com sucesso!")

        
        

    except Exception as e:
        print(f"Erro ao executar o seed: {e}")
    finally:
        db.close() 

if __name__ == "__main__":
    popular()
'''