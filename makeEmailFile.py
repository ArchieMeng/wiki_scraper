import pickle

def makeEmailFile():
    mail_data = {'mail_host': raw_input("Please input mail host domain name(the mail server):\t"),
                 'mail_port': raw_input("Please input mail port:\t"),
                 'mail_name': raw_input("Please input mail address:\t"),
                 'mail_pass': raw_input("Please input mail password:\t")}

    with open("mail_data.p",'w') as f:
        pickle.dump(mail_data, f)

if __name__ == "__main__":
    makeEmailFile()