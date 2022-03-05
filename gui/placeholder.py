

class Placeholder:

    def __init__(self):
        pass


    def ph_user_exists(self, user_id):
        return True

    def ph_get_chats(self, user_id):
        chat_dict = [{
            'chat_id': '167831c0-be28-4689-b040-49048118956e',
            'chat_name': None
             },
             {
                'chat_id': 'e6070836-3b69-4da1-b6ef-7dfabcda5d14',  
                'chat_name': None}]
        return chat_dict