import json
import random


class UserData:
    def __init__(self):
        self.friends = ""
        self.users = ""

        # Specify encoding as 'utf-8' while opening the files
        try:
            with open("friends.json", "r", encoding="utf-8") as file:
                self.friends = json.load(file)

            with open("users.json", "r", encoding="utf-8") as file:
                self.users = json.load(file)
        except UnicodeDecodeError as e:
            print("Error decoding file:", e)
        except FileNotFoundError as e:
            print("File not found:", e)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)

    def save_to_file(self, friends):
        with open("friends.json", "w") as file2:
            json.dump(friends, file2, indent=2)


# IncomingRequestsLogic and OutgoingRequestsLogic remain unchanged



class IncomingRequestsLogic(UserData):
    def __init__(self, mail):
        self.mail = mail
        super().__init__()

    def collect_incoming_requests_data(self):
        user_inc_req = self.friends[self.mail]["friend requests"]["received"]
        inc_data = []
        for mail in user_inc_req:
            rand_inx = random.randint(4, 8)
            user = self.users[mail]
            name = f"{user['f name']} {user['l name']}"
            rand_prop = list(user.values())[rand_inx]
            prof_ph = user["profile photo"]
            user_d = {"name": name, "profile photo": prof_ph, "random parameter": rand_prop, "fr mail": mail}
            inc_data.append(user_d)
        return inc_data

    def accept_fr_req(self, fr_mail):
        user = self.friends[self.mail]
        user["friends"].append(fr_mail)
        user["friend requests"]["received"].remove(fr_mail)

        self.friends[fr_mail]["friend requests"]["sent"][self.mail] = "accepted"

        self.save_to_file(self.friends)

    def decline_fr_req(self, fr_mail):
        user = self.friends[self.mail]
        user["friend requests"]["received"].remove(fr_mail)

        self.friends[fr_mail]["friend requests"]["sent"][self.mail] = "declined"

        self.save_to_file(self.friends)


class OutgoingRequestsLogic(UserData):
    def __init__(self, mail):
        self.mail = mail
        super().__init__()

    def collect_outgoing_requests_data(self):
        user_outg_req = self.friends[self.mail]["friend requests"]["sent"]
        outg_data = []
        for mail in user_outg_req:
            rand_inx = random.randint(4, 8)
            req_stat = user_outg_req[mail]
            user = self.users[mail]
            name = f"{user["f name"]} {user["l name"]}"
            rand_prop = list(user.values())[rand_inx]
            prof_ph = user["profile photo"]
            user_d = {"name": name, "profile photo": prof_ph, "random parameter": rand_prop, "fr mail": mail, "request status": req_stat}
            outg_data.append(user_d)
        return outg_data

    def sent_ok(self, fr_mail):
        del self.friends[self.mail]["friend requests"]["sent"][fr_mail]
        self.save_to_file(self.friends)
