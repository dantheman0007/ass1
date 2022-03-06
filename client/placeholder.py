import json

class Placeholder:

    def __init__(self):
        pass


    def ph_user_exists(self, user_id):
        return True

    def ph_get_chats(self, user_id):
        chat_dict = [{
            'chat_id': '167831c0-be28-4689-b040-49048118956e',
            'chat_name': "DNFHGR123"
             },
             {
                'chat_id': 'e6070836-3b69-4da1-b6ef-7dfabcda5d14',  
                'chat_name': "EHRGTY456"}]
        return chat_dict

    def get_messages(self, chat_id):
        messages = {
                "chat_id": "e6070836-3b69-4da1-b6ef-7dfabcda5d14",
                "chat_participants": [
                    {
                        "user_id": "LJNDAN001",
                        "user_name": "Daniel"
                    },
                    {
                        "user_id": "BHGLKS987",
                        "user_name": "Bob"
                    }
                ],

                "messages":[
                    {
                        "message_id": "abc",
                        "msg_content": "Hello",
                        "timestamp": "123",
                        "from_id": "LJNDAN001"
                    },
                    {
                        "message_id": "gjmh",
                        "msg_content": "Goodbye",
                        "timestamp": "123",
                        "from_id": "MRRJUL007"
                    },
                    {
                        "message_id": "abc",
                        "msg_content": "Hello",
                        "timestamp": "123",
                        "from_id": "LJNDAN001"
                    }
                ]
            }


        with open("chats/{}.json".format(chat_id), "w") as chat_file:
            json.dump(messages, chat_file)

        ## When new message arrives from the server, we'll need to have a method that is on the gui side that receives the messages, disaplys it and then writes it to the chat file

