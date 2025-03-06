

from models.database import session_maker

def get_db():
    '''
     This Function returns the session(connection) to the database.
    '''
    try:
        db =  session_maker()
        yield db
    #except:
    #    db.rollback()
    finally:
        db.close()