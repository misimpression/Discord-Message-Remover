"""
 Copyright 2024 misimpression

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

from os import system

from json import load
from time import sleep

from colorama import Fore
from tls_client import Session

class Base:
    messages: list
    session: Session

    def __init__(self):
        self.session  = Session(client_identifier="chrome_112")

        self.config   = load( open("config.json", "r") )
        self.channel  = self.config.get("channel_id", "")
        self.token    = self.config.get("token", "")

        self.getMessages()

    def getMessages(self) -> None:
        message_list = []
        request_url  = f"https://discord.com/api/v10/channels/{self.channel}/messages?limit=100"

        while True:
            response = self.session.get(
                request_url,
                headers={"Authorization": str(self.token)}
            )

            if response.status_code not in (200, 201, 204):
                break

            message_list.append(response)
            request_url = f"https://discord.com/api/v10/channels/{self.channel}/messages?limit=100&before={response[-1]["id"]}" # type: ignore
        
        if message_list:
            self.messages = message_list
            print(Fore.RED + f"[ {Fore.WHITE}+{Fore.RED} ] Got {Fore.WHITE}{len(message_list)} messages{Fore.RED}...")

    def deleteMessage(self, message_id) -> None:
        response = self.session.delete(
            f"https://discord.com/api/v10/channels/{self.channel}/messages/{message_id}",
            headers={"Authorization": str(self.token)}
        )

        if response.status_code in (200, 201, 204):
            print(Fore.RED + f"[ {Fore.WHITE}+{Fore.RED} ] Deleted {Fore.WHITE}{message_id}{Fore.RED}...")

    def deleteMessages(self) -> None:
        for message in self.messages:
            message_id = message.get("id", "")

            self.deleteMessage(message_id=message_id)
            sleep(0.075)

if __name__ == "__main__":
    system("cls||clear")

    base = Base()
    base.deleteMessages()