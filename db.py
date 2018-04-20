import postgresql

connection_iri = 'pq://test_ruki_manager:100500@localhost:5432/test_ruki'


class DataBase():
    def __init__(self) -> None:
        super().__init__()
        self.db = postgresql.open(connection_iri)

    def save_order(self, phones, details):
        q = "SELECT * FROM phones WHERE phone_number IN (%s)" % (','.join(map(lambda x: str(x), phones)))

        raw_result = self.db.query(q)
        stored_phones = set(map(lambda x: x['phone_number'], raw_result))
        if stored_phones:
            not_stored_phones = stored_phones.symmetric_difference(set(phones))
            for_user = raw_result[0]['user_id']

            if not_stored_phones:
                ph_ins = self.db.prepare('INSERT INTO phones VALUES ($1, $2)')
                for ns_phone in not_stored_phones:
                    ph_ins(ns_phone, for_user)

        else:
            insert_q = '''
            WITH user_ins AS (
                    INSERT INTO users VALUES (nextval('users_sequence')) RETURNING user_id
            ), 
                 phones_ins (phone) AS (
                    VALUES %(phones)s
            )
            INSERT INTO phones (user_id, phone_number) 
                SELECT user_id, phone FROM user_ins 
                JOIN phones_ins ON true 
                RETURNING user_id;
            
            ''' % {'phones': ",".join(["(%s)" % phone for phone in phones])}
            for_user = self.db.query(insert_q)

        ord_ind = self.db.prepare('INSERT INTO orders (details, user_id) VALUES ($1, $2)')
        ord_ind(details, for_user)

    def get_orders_by_phone(self, phone_number):
        q_result = self.db.query('''
            SELECT DISTINCT o.details FROM orders o 
            JOIN phones p ON p.user_id = o.user_id 
            WHERE o.user_id = 
                (SELECT user_id FROM phones WHERE phone_number = %s) 
        ''' % phone_number)
        return list(map(lambda x: x[0], q_result))

    def __del__(self):
        self.db.close()
