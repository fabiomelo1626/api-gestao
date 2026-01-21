from seed.tabelasAuxiliaresSeed import seed_tabelas_auxiliares

from conexao.conect_db import SessionLocal

def popular():
    db = SessionLocal()
    try:
      
        seed_tabelas_auxiliares(db)
        print("Seed das tabelas auxiliares executado com sucesso!")

        
        

    except Exception as e:
        print(f"Erro ao executar o seed: {e}")
    finally:
        db.close() 

if __name__ == "__main__":
    popular()
